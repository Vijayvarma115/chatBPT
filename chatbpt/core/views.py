from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
import markdown2
from bson import ObjectId
from collections import defaultdict
import datetime

from .services.llama_api import LlamaAPI
from .models import ChatHistory

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {'user': request.user})

@login_required
def chat(request):
    llama_api = LlamaAPI(api_key=settings.GROQ_API_KEY)
    chat_history_model = ChatHistory()
    chat_history = chat_history_model.get_chat_history(request.user.id)
    current_chat_id = request.GET.get('chat_id')
    new_chat = request.GET.get('new_chat')

    if new_chat:
        current_chat = []
    elif current_chat_id:
        current_chat = list(chat_history_model.collection.find({"_id": ObjectId(current_chat_id)}))
    else:
        current_chat = list(chat_history)

    if request.method == 'POST':
        message = request.POST['message']
        response = llama_api.send_message(message)
        
        # Render the response as markdown
        formatted_response = markdown2.markdown(response)
        
        # Save user message and formatted response to chat history
        chat_history_model.save_message(request.user.id, message, timezone.now())
        chat_history_model.save_message(request.user.id, formatted_response, timezone.now())
        
        current_chat = list(chat_history_model.get_chat_history(request.user.id))

    # Assign chat names and group by day
    chat_groups = defaultdict(list)
    for chat in chat_history:
        chat_id = str(chat['_id'])
        chat_date = chat['timestamp'].date()
        chat_name = f"Chat on {chat_date}"
        if chat_name not in [c['name'] for c in chat_groups[chat_date]]:
            chat_groups[chat_date].append({
                'id': chat_id,
                'name': chat_name,
                'timestamp': chat['timestamp'],
            })
    
    return render(request, 'core/chat.html', {'chat_groups': sorted(chat_groups.items(), reverse=True), 'current_chat': sorted(current_chat, key=lambda x: x['timestamp'])})