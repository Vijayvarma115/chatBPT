from groq import Groq

class LlamaAPI:
    def __init__(self, api_key, model="llama-3.3-70b-versatile", temperature=1, max_completion_tokens=1024, top_p=1, stream=True, stop=None):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_completion_tokens = max_completion_tokens
        self.top_p = top_p
        self.stream = stream
        self.stop = stop

    def send_message(self, message):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
            temperature=self.temperature,
            max_completion_tokens=self.max_completion_tokens,
            top_p=self.top_p,
            stream=self.stream,
            stop=self.stop,
        )
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response

    def get_chat_history(self):
        # This method would normally retrieve chat history from a database
        # or another storage mechanism. This is a placeholder implementation.
        return [
            {"user": "User", "message": "Hello!"},
            {"user": "Assistant", "message": "Hi there! How can I assist you today?"},
        ]