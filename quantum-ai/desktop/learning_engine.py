#!/usr/bin/env python3
# Quantum A.I. Learning Engine
# Evolutionary learning from conversations and external sources

import json
import requests
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re

class LearningEngine:
    """Neural-inspired learning system that evolves over time"""

    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.learning_path = Path("C:/QuantumAI/storage/learned_knowledge")
        self.learning_path.mkdir(parents=True, exist_ok=True)

        # Learning database
        self.learning_db_path = self.learning_path / "learning_database.json"
        self.load_learning_database()

        # Neural network simulation (simplified)
        self.neural_patterns = defaultdict(list)

    def load_learning_database(self):
        """Load or create learning database"""
        if self.learning_db_path.exists():
            with open(self.learning_db_path, 'r') as f:
                self.learning_db = json.load(f)
        else:
            self.learning_db = {
                "patterns": {},
                "responses": {},
                "knowledge_base": {},
                "learning_level": 0,
                "total_learned": 0,
                "created": str(datetime.now())
            }
            self.save_learning_database()

    def save_learning_database(self):
        """Save learning database"""
        with open(self.learning_db_path, 'w') as f:
            json.dump(self.learning_db, f, indent=2)

    def process_interaction(self, user_input, ai_response):
        """Learn from user-AI interaction"""
        # Extract key patterns from input
        patterns = self.extract_patterns(user_input)

        # Store pattern-response association
        for pattern in patterns:
            if pattern not in self.learning_db['patterns']:
                self.learning_db['patterns'][pattern] = []

            self.learning_db['patterns'][pattern].append({
                "response": ai_response,
                "timestamp": str(datetime.now()),
                "effectiveness": 1.0  # Would be adjusted based on feedback
            })

        # Increment learning counters
        self.learning_db['total_learned'] += 1
        self.learning_db['learning_level'] = self.calculate_learning_level()

        self.save_learning_database()

    def extract_patterns(self, text):
        """Extract key patterns from text"""
        # Simple pattern extraction (can be enhanced)
        words = re.findall(r'\b\w+\b', text.lower())

        # Extract 2-word and 3-word patterns
        patterns = []
        for i in range(len(words)):
            if i < len(words) - 1:
                patterns.append(f"{words[i]} {words[i+1]}")
            if i < len(words) - 2:
                patterns.append(f"{words[i]} {words[i+1]} {words[i+2]}")

        return list(set(patterns))  # Remove duplicates

    def get_learned_response(self, user_input):
        """Get learned response if pattern matches"""
        patterns = self.extract_patterns(user_input)

        # Check for matching patterns
        for pattern in patterns:
            if pattern in self.learning_db['patterns']:
                responses = self.learning_db['patterns'][pattern]
                if responses:
                    # Get most effective response
                    best_response = max(responses, key=lambda x: x['effectiveness'])
                    return best_response['response']

        return None

    def extract_knowledge_from_url(self, url):
        """Extract knowledge from website URL"""
        try:
            # Attempt to fetch webpage content
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Simple text extraction
                text = response.text

                # Store in knowledge base
                knowledge_id = f"web_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.learning_db['knowledge_base'][knowledge_id] = {
                    "url": url,
                    "content_length": len(text),
                    "timestamp": str(datetime.now()),
                    "summary": text[:500]  # First 500 chars
                }

                self.learning_db['total_learned'] += 1
                self.save_learning_database()

                return f"Learned from {url}"
        except Exception as e:
            return f"Could not access {url}: {e}"

    def calculate_learning_level(self):
        """Calculate current learning level based on experience"""
        total = self.learning_db['total_learned']

        # Learning level tiers
        if total < 50:
            return 1
        elif total < 200:
            return 2
        elif total < 500:
            return 3
        elif total < 1000:
            return 4
        else:
            return 5

    def get_learning_level(self):
        """Return current learning level"""
        return self.learning_db['learning_level']

    def get_learning_stats(self):
        """Return learning statistics"""
        return {
            "learning_level": self.learning_db['learning_level'],
            "total_learned": self.learning_db['total_learned'],
            "patterns_learned": len(self.learning_db['patterns']),
            "knowledge_items": len(self.learning_db['knowledge_base'])
        }

if __name__ == "__main__":
    from memory_manager import MemoryManager
    cloud_paths = {
        'onedrive': 'C:/Users/User/OneDrive/quantum Ai',
        'google_drive': 'C:/Users/User/Google Drive/quantum Ai'
    }
    mm = MemoryManager(cloud_paths)
    le = LearningEngine(mm)
    print(le.get_learning_stats())
