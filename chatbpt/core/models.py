from django.db import models
from django.conf import settings
from pymongo import MongoClient

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
    
    def get_chat_history(self, user_id):
        client = MongoClient(settings.MONGODB_SETTINGS['host'])
        db = client[settings.MONGODB_SETTINGS['db']]
        collection = db.chat_history
        return list(collection.find({'user_id': user_id}).sort('timestamp', -1))
    
    def save_message(self, user_id, message, timestamp):
        client = MongoClient(settings.MONGODB_SETTINGS['host'])
        db = client[settings.MONGODB_SETTINGS['db']]
        collection = db.chat_history
        collection.insert_one({
            'user_id': user_id,
            'message': message,
            'timestamp': timestamp,
            'name': message[:20]  # Use the first 20 characters of the message as the chat name
        })