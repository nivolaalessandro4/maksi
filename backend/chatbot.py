from nvidia_jarvis import JarvisAPI
import json
import os
import nltk
from nltk.tokenize import word_tokenize

# Ensure 'punkt' resource is downloaded
nltk.download('punkt')

class Chatbot:
    def __init__(self, knowledge_base_file='knowledge_base.json'):
        self.jarvis = JarvisAPI()  # Initialize Jarvis API
        self.context = {}  # Stores conversation history for each user
        self.feedback = {}  # Stores feedback for each user
        self.data_file = 'chat_data.json'  # File to store collected data
        self.knowledge_base_file = knowledge_base_file
        self.load_data()  # Load existing data if any
        self.load_knowledge_base()  # Load knowledge base

    def load_data(self):
        """Load existing data from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = []

    def save_data(self):
        """Save collected data to file"""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def collect_data(self, user_input, response, user_id):
        """Collect data for training"""
        self.data.append({
            'user_id': user_id,
            'user_input': user_input,
            'response': response
        })
        self.save_data()

    def load_knowledge_base(self):
        """Load the knowledge base from file"""
        try:
            with open(self.knowledge_base_file, 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = {}

    def save_knowledge_base(self):
        """Save the knowledge base to file"""
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=4)  # Indent for pretty formatting

    def find_response(self, user_input):
        """Find response from the knowledge base"""
        for question in self.knowledge_base.get('questions', []):
            if question['question'].lower() == user_input.lower():
                return question['response']
        return None

    def teach_response(self, user_input, response):
        """Teach the chatbot a new response"""
        new_question = {'question': user_input.lower(), 'response': response}
        if 'questions' not in self.knowledge_base:
            self.knowledge_base['questions'] = []
        self.knowledge_base['questions'].append(new_question)
        self.save_knowledge_base()

    def get_response(self, user_input, user_id=None):
        # Handle feedback
        if user_id and self.is_feedback_request(user_input):
            feedback = self.extract_feedback(user_input)
            self.record_feedback(user_id, feedback)
            return "Thank you for your feedback!"

        # Check knowledge base for response
        response = self.find_response(user_input)
        if response is None:
            
            response = self.jarvis.generate_response(user_input)
            
            self.collect_data(user_input, response, user_id)
        else:
            self.collect_data(user_input, response, user_id)

        # Update conversation context
        if user_id:
            self.update_context(user_id, user_input)

        
        formatted_response = self.format_response(response, user_id)
        
        return formatted_response

    def update_context(self, user_id, user_input):
        if user_id not in self.context:
            self.context[user_id] = []
        self.context[user_id].append(user_input)

    def format_response(self, response, user_id):
        if user_id in self.context:
            history = " ".join(self.context[user_id])
            return f"History: {history}\nResponse: {response}"
        return response

    def is_feedback_request(self, user_input):
       
        return "rate" in user_input.lower()

    def extract_feedback(self, user_input):
       
        try:
            feedback = int(user_input.split()[-1])
            return feedback
        except (IndexError, ValueError):
            return None

    def record_feedback(self, user_id, feedback):
        if user_id not in self.feedback:
            self.feedback[user_id] = []
        if feedback is not None:
            self.feedback[user_id].append(feedback)

