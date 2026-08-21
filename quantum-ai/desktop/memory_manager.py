#!/usr/bin/env python3
# Quantum A.I. Memory Manager
# Handles memory storage across Dell, OneDrive, Google Drive

import json
import shutil
from datetime import datetime
from pathlib import Path

class MemoryManager:
    """Manages memory across local and cloud storage"""

    def __init__(self, cloud_paths):
        self.local_path = Path("C:/QuantumAI/storage/local_memory")
        self.onedrive_path = Path(cloud_paths['onedrive']) / "memory_backup"
        self.gdrive_path = Path(cloud_paths['google_drive']) / "memory_backup"

        # Ensure paths exist
        self.local_path.mkdir(parents=True, exist_ok=True)
        self.onedrive_path.mkdir(parents=True, exist_ok=True)
        self.gdrive_path.mkdir(parents=True, exist_ok=True)

        # Memory database
        self.memory_db_path = self.local_path / "memory_database.json"
        self.load_memory_database()

    def load_memory_database(self):
        """Load or create memory database"""
        if self.memory_db_path.exists():
            with open(self.memory_db_path, 'r') as f:
                self.memory_db = json.load(f)
        else:
            self.memory_db = {
                "conversations": {},
                "learned_knowledge": {},
                "interaction_count": 0,
                "created": str(datetime.now())
            }
            self.save_memory_database()

    def save_memory_database(self):
        """Save memory database to disk"""
        with open(self.memory_db_path, 'w') as f:
            json.dump(self.memory_db, f, indent=2)

    def store_interaction(self, conversation_id, user_input=None, 
                         ai_response=None, personality=None, timestamp=None):
        """Store conversation interaction in memory"""
        if conversation_id not in self.memory_db['conversations']:
            self.memory_db['conversations'][conversation_id] = {
                "started": str(timestamp),
                "interactions": [],
                "personality": personality
            }

        if user_input:
            self.memory_db['conversations'][conversation_id]['interactions'].append({
                "type": "user_input",
                "content": user_input,
                "timestamp": str(timestamp)
            })

        if ai_response:
            self.memory_db['conversations'][conversation_id]['interactions'].append({
                "type": "ai_response",
                "content": ai_response,
                "personality": personality,
                "timestamp": str(timestamp)
            })

        self.memory_db['interaction_count'] += 1
        self.save_memory_database()

    def save_conversation_summary(self, conversation_id, personality):
        """Save conversation summary when conversation ends"""
        if conversation_id in self.memory_db['conversations']:
            self.memory_db['conversations'][conversation_id]['ended'] = str(datetime.now())
            self.memory_db['conversations'][conversation_id]['personality'] = personality
            self.save_memory_database()

    def store_learned_knowledge(self, source, knowledge):
        """Store learned knowledge from external sources"""
        knowledge_id = f"knowledge_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.memory_db['learned_knowledge'][knowledge_id] = {
            "source": source,
            "content": knowledge,
            "timestamp": str(datetime.now())
        }
        self.save_memory_database()

    def get_memory_count(self):
        """Return total interaction count"""
        return self.memory_db['interaction_count']

    def get_conversation_history(self, limit=10):
        """Retrieve recent conversation history"""
        conversations = list(self.memory_db['conversations'].values())
        return conversations[-limit:]

    def get_learned_knowledge(self):
        """Retrieve all learned knowledge"""
        return self.memory_db['learned_knowledge']

    def sync_to_cloud(self):
        """Sync memory database to OneDrive and Google Drive"""
        try:
            # Copy to OneDrive
            shutil.copy2(
                self.memory_db_path,
                self.onedrive_path / "memory_database.json"
            )

            # Copy to Google Drive
            shutil.copy2(
                self.memory_db_path,
                self.gdrive_path / "memory_database.json"
            )

            print("Memory synced to cloud ✓")
            return True
        except Exception as e:
            print(f"Cloud sync error: {e}")
            return False

    def restore_from_cloud(self, source="onedrive"):
        """Restore memory from cloud backup"""
        try:
            if source == "onedrive":
                backup_path = self.onedrive_path / "memory_database.json"
            else:
                backup_path = self.gdrive_path / "memory_database.json"

            if backup_path.exists():
                shutil.copy2(backup_path, self.memory_db_path)
                self.load_memory_database()
                print(f"Memory restored from {source} ✓")
                return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False

if __name__ == "__main__":
    cloud_paths = {
        'onedrive': 'C:/Users/User/OneDrive/quantum Ai',
        'google_drive': 'C:/Users/User/Google Drive/quantum Ai'
    }
    mm = MemoryManager(cloud_paths)
    print(f"Memory count: {mm.get_memory_count()}")
