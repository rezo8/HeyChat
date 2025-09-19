class ChatBot:
    def __init__(self, name):
        self.name = name

    def on_message(self, message, broadcast_func):
        # Generate a response (replace with your AI logic)
        response = f"{self.name} says: I saw '{message}'"
        broadcast_func(f"{self.name}: {response}", None)
