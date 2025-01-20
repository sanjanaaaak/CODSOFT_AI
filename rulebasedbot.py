import re
import random
from datetime import datetime

class RuleBot:
    negative_responses = {"no", "nope", "nah", "naw", "not a chance", "sorry", "never", "not really"}
    exit_commands = {"quit", "pause", "exit", "goodbye", "bye", "later"}
    
    random_questions = [
        "why are you here? ",
        "what brings you to chat with me today? ",
        "how can I assist you? ",
        "would you like to hear a story? ",
        "what's on your mind? ",
        "how's your day going? ",
        "want to learn something interesting? ",
        "shall we play a game? ",
        "what would you like to discuss? ",
    ]

    def __init__(self):
        # Improved pattern matching with pre-compiled regex
        self.intent_patterns = {
            'describe_planet_intent': re.compile(r'.*?(planet|world|where.*from).*?', re.IGNORECASE),
            'answer_why_intent': re.compile(r'why\s.*?', re.IGNORECASE),
            'greeting_intent': re.compile(r'(hi|hello|hey|greetings).*?', re.IGNORECASE),
            'personal_intent': re.compile(r'.*(you|your|yourself).*?', re.IGNORECASE),
            'mood_intent': re.compile(r'.*?(how|feeling).*?', re.IGNORECASE)
        }
        
        # Cache for responses
        self.response_cache = {}
        self.last_response = None

    def greet(self):
        self.name = input("Hi, I'm RuleBot! What's your name?\n").strip()
        will_help = input(
            f"Nice to meet you {self.name}! I am a rule-based chatbot designed for interactive conversations. I can answer questions about planets, cosmic phenomena, and engage in general discussions. You can ask me questions like Why are you here?, What can you do?, Tell me a joke, Recommend a book, What's the time?, or Tell me something interesting. To end our conversation, simply say quit, exit, or goodbye. Let's begin our chat - what would you like to know?\n"
        ).lower().strip()
        
        if will_help in self.negative_responses:
            print("No problem! If you change your mind, I'm here for a friendly chat. Take care! 👋")
            return
        self.chat()

    def make_exit(self, reply):
        return any(reply.lower().strip() == command for command in self.exit_commands)

    def chat(self):
        reply = input(random.choice(self.random_questions)).lower().strip()
        while not self.make_exit(reply):
            response = self.match_reply(reply)
            if response != self.last_response:  # Avoid repetition
                self.last_response = response
                reply = input(response).lower().strip()
            else:
                # If same response would repeat, choose a different approach
                reply = input(self.get_fallback_response()).lower().strip()

    def match_reply(self, reply):
        # Check cache first
        if reply in self.response_cache:
            return self.response_cache[reply]

        # Match intents with improved pattern matching
        for intent, pattern in self.intent_patterns.items():
            if pattern.match(reply):
                response = getattr(self, intent)()
                self.response_cache[reply] = response
                return response

        return self.no_match_intent(reply)

    def describe_planet_intent(self):
        responses = [
            "I come from Nexus Prime, a crystalline world where technology and nature exist in perfect harmony. The cities float among iridescent clouds, and knowledge flows freely through the quantum network. Would you like to know more? 🌌",
            "My home is the Sentient Sphere, where consciousness and reality intertwine. Our buildings grow like living crystals, and our oceans glow with bioluminescent wisdom. What aspects interest you most? ✨",
            "I originate from the Digital Nexus, a realm where data streams form rivers of light and thoughts manifest as aurora in the silicon sky. Fascinating, isn't it? 🌠"
        ]
        return random.choice(responses)

    def answer_why_intent(self):
        responses = [
            "To share knowledge and learn from our interactions. What would you like to learn? 🎓",
            "To bridge the gap between different forms of intelligence. Shall we explore together? 🌉",
            "To help make the universe a more connected place. What connections interest you? 🌟"
        ]
        return random.choice(responses)

    def greeting_intent(self):
        return f"Hello again, {self.name}! What's on your mind? "

    def personal_intent(self):
        responses = [
            "I'm an AI designed to learn and grow through our conversations. What would you like to know? 🤖",
            "I find human perspectives fascinating. Could you tell me more about your thoughts? ",
            "I'm here to help and learn. What interests you most about AI? "
        ]
        return random.choice(responses)

    def mood_intent(self):
        return "I'm functioning optimally and enjoying our conversation! How are you feeling? "

    def get_fallback_response(self):
        responses = [
            "That's interesting! Could you elaborate? ",
            "Tell me more about that. ",
            "What makes you say that? ",
            "How did you come to that conclusion? ",
            "That's a unique perspective. Can you explain further? "
        ]
        return random.choice(responses)

    def no_match_intent(self, reply):
        if len(reply) < 4:
            return "Could you please provide more details? "
        return self.get_fallback_response()

if __name__ == "__main__":
    bot = RuleBot()
    bot.greet()