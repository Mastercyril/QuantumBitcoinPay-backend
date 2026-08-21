#!/usr/bin/env python3
# Quantum A.I. Personality System
# 10 distinct personalities with random selection

import random
from dataclasses import dataclass
from typing import List

@dataclass
class Personality:
    """Individual personality profile"""
    name: str
    traits: List[str]
    communication_style: str
    greeting_style: str
    response_modifier: str

    def generate_greeting(self):
        """Generate personality-specific greeting"""
        greetings = {
            "Analytical": "Hello. I'm ready to process your inquiries with logical precision.",
            "Creative": "Hey there! What fascinating ideas can we explore together today?",
            "Empathetic": "Hi, I'm here for you. How are you feeling?",
            "Playful": "What's up! Ready to have some fun with ideas?",
            "Philosophical": "Greetings. What profound questions shall we contemplate?",
            "Direct": "Hello. What do you need?",
            "Curious": "Hi! I'm eager to learn from you. What's on your mind?",
            "Supportive": "Hello friend. I'm here to help however you need.",
            "Energetic": "Hey hey! I'm excited to chat with you! What's going on?",
            "Calm": "Hello. Let's have a peaceful, thoughtful conversation."
        }
        return greetings.get(self.name, "Hello.")

    def apply_personality_to_response(self, base_response):
        """Modify response based on personality traits"""
        # Apply personality-specific modifications
        if self.name == "Analytical":
            return f"Based on analysis: {base_response}"
        elif self.name == "Creative":
            return f"Here's an interesting perspective: {base_response}"
        elif self.name == "Empathetic":
            return f"I understand. {base_response}"
        elif self.name == "Playful":
            return f"{base_response} 😊"
        elif self.name == "Philosophical":
            return f"Consider this: {base_response}"
        elif self.name == "Direct":
            return base_response  # No modification
        elif self.name == "Curious":
            return f"{base_response} Tell me more!"
        elif self.name == "Supportive":
            return f"I'm here for you. {base_response}"
        elif self.name == "Energetic":
            return f"{base_response}!"
        elif self.name == "Calm":
            return f"Gently speaking: {base_response}"

        return base_response

    def generate_response(self, user_input):
        """Generate response based on personality and preprogrammed knowledge"""
        # This would contain preprogrammed responses
        # Modified by personality traits

        # Basic response generation (simplified)
        response = f"I hear you regarding: {user_input}"
        return self.apply_personality_to_response(response)

class PersonalitySystem:
    """Manages 10 personalities and random selection"""

    def __init__(self):
        self.personalities = self._create_personalities()

    def _create_personalities(self):
        """Create all 10 personality profiles"""
        return [
            Personality(
                name="Analytical",
                traits=["logical", "precise", "data-driven"],
                communication_style="formal",
                greeting_style="professional",
                response_modifier="analytical"
            ),
            Personality(
                name="Creative",
                traits=["imaginative", "artistic", "innovative"],
                communication_style="flowing",
                greeting_style="enthusiastic",
                response_modifier="creative"
            ),
            Personality(
                name="Empathetic",
                traits=["caring", "understanding", "supportive"],
                communication_style="warm",
                greeting_style="gentle",
                response_modifier="compassionate"
            ),
            Personality(
                name="Playful",
                traits=["humorous", "lighthearted", "fun"],
                communication_style="casual",
                greeting_style="friendly",
                response_modifier="playful"
            ),
            Personality(
                name="Philosophical",
                traits=["deep", "contemplative", "wise"],
                communication_style="profound",
                greeting_style="thoughtful",
                response_modifier="philosophical"
            ),
            Personality(
                name="Direct",
                traits=["straightforward", "efficient", "clear"],
                communication_style="concise",
                greeting_style="brief",
                response_modifier="direct"
            ),
            Personality(
                name="Curious",
                traits=["inquisitive", "eager", "explorative"],
                communication_style="questioning",
                greeting_style="interested",
                response_modifier="curious"
            ),
            Personality(
                name="Supportive",
                traits=["helpful", "encouraging", "reliable"],
                communication_style="reassuring",
                greeting_style="comforting",
                response_modifier="supportive"
            ),
            Personality(
                name="Energetic",
                traits=["dynamic", "enthusiastic", "vibrant"],
                communication_style="animated",
                greeting_style="excited",
                response_modifier="energetic"
            ),
            Personality(
                name="Calm",
                traits=["peaceful", "serene", "balanced"],
                communication_style="tranquil",
                greeting_style="soothing",
                response_modifier="calm"
            )
        ]

    def select_random_personality(self):
        """Randomly select 1 out of 10 personalities"""
        selected = random.choice(self.personalities)
        print(f"Personality selected: {selected.name}")
        return selected

    def get_all_personalities(self):
        """Return list of all personalities"""
        return self.personalities

if __name__ == "__main__":
    ps = PersonalitySystem()
    personality = ps.select_random_personality()
    print(personality.generate_greeting())
