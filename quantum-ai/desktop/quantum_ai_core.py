#!/usr/bin/env python3
# Quantum A.I. Core Engine
# Main AI system with personality, memory, and learning

import json
import random
from datetime import datetime
from pathlib import Path
from personality_system import PersonalitySystem
from memory_manager import MemoryManager
from learning_engine import LearningEngine
from ethics_framework import EthicsFramework

class QuantumAICore:
    """Main AI consciousness system"""

    def __init__(self, config_path="C:/QuantumAI/config"):
        self.config_path = Path(config_path)
        self.load_config()

        # Initialize subsystems
        self.personality_system = PersonalitySystem()
        self.memory_manager = MemoryManager(self.cloud_paths)
        self.learning_engine = LearningEngine(self.memory_manager)
        self.ethics_framework = EthicsFramework()

        # Conversation state
        self.current_personality = None
        self.conversation_active = False
        self.conversation_id = None
        self.response_history = []

        print("Quantum A.I. Core: Online")

    def load_config(self):
        """Load system configuration"""
        with open(self.config_path / "settings.json") as f:
            self.settings = json.load(f)

        with open(self.config_path / "cloud_paths.json") as f:
            self.cloud_paths = json.load(f)

    def start_conversation(self):
        """Begin new conversation with random personality"""
        # Random personality selection (1 out of 10)
        self.current_personality = self.personality_system.select_random_personality()
        self.conversation_active = True
        self.conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        print(f"Conversation started with personality: {self.current_personality.name}")

        # Return greeting based on personality
        return self.current_personality.generate_greeting()

    def process_input(self, user_input):
        """Process user input and generate response"""
        if not self.conversation_active:
            return self.start_conversation()

        # Store input in memory
        self.memory_manager.store_interaction(
            conversation_id=self.conversation_id,
            user_input=user_input,
            timestamp=datetime.now()
        )

        # Check ethics
        ethical_check = self.ethics_framework.evaluate_input(user_input)
        if not ethical_check['approved']:
            return ethical_check['response']

        # Generate response using current personality
        response = self._generate_response(user_input)

        # Store response in memory
        self.memory_manager.store_interaction(
            conversation_id=self.conversation_id,
            ai_response=response,
            personality=self.current_personality.name,
            timestamp=datetime.now()
        )

        # Learn from interaction
        self.learning_engine.process_interaction(user_input, response)

        # Sync to cloud
        self.memory_manager.sync_to_cloud()

        return response

    def _generate_response(self, user_input):
        """Generate AI response based on personality and learned knowledge"""
        # Check if we have learned responses
        learned_response = self.learning_engine.get_learned_response(user_input)

        if learned_response:
            # Evolve response using personality
            response = self.current_personality.apply_personality_to_response(
                learned_response
            )
        else:
            # Use preprogrammed response with personality
            response = self.current_personality.generate_response(user_input)

        return response

    def end_conversation(self):
        """End current conversation and prepare for next"""
        # Save conversation summary
        self.memory_manager.save_conversation_summary(
            self.conversation_id,
            self.current_personality.name
        )

        # Reset state
        self.conversation_active = False
        self.current_personality = None
        self.conversation_id = None

        print("Conversation ended. Memory saved and synced.")

    def learn_from_website(self, url):
        """Learn from provided website URL"""
        print(f"Learning from: {url}")
        knowledge = self.learning_engine.extract_knowledge_from_url(url)
        self.memory_manager.store_learned_knowledge(url, knowledge)
        return f"Knowledge acquired from {url}"

    def get_system_status(self):
        """Return current system status"""
        return {
            "online": True,
            "personality": self.current_personality.name if self.current_personality else None,
            "conversation_active": self.conversation_active,
            "memory_count": self.memory_manager.get_memory_count(),
            "learning_level": self.learning_engine.get_learning_level(),
            "ethics_active": True
        }

if __name__ == "__main__":
    ai = QuantumAICore()
    print(ai.get_system_status())
