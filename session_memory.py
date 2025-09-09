# session_memory.py
from collections import defaultdict

class SessionMemory:
    def __init__(self):
        self.sessions = defaultdict(list)

    def get_history(self, user_id: str) -> list[str]:
        return self.sessions[user_id]

    def append(self, user_id: str, user_message: str, bot_response: str):
        self.sessions[user_id].append(user_message)
        self.sessions[user_id].append(bot_response)

    def clear(self, user_id: str):
        self.sessions[user_id] = []
