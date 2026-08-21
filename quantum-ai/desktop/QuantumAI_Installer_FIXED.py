#!/usr/bin/env python3
# Quantum A.I. System Installer - FIXED VERSION
# Creator: Joseph Dougherty, 13th Chamber LLC

import os
import json
from pathlib import Path
from datetime import datetime  # <-- FIXED: Added this import

class QuantumAIInstaller:
    """Installer for Quantum A.I. System"""

    def __init__(self):
        self.base_dir = Path("C:/QuantumAI")
        self.onedrive_path = Path(f"C:/Users/{os.getlogin()}/OneDrive/quantum Ai")
        self.gdrive_path = Path(f"C:/Users/{os.getlogin()}/Google Drive/quantum Ai")

    def create_directories(self):
        """Create all required directories"""
        print("Creating directory structure...")

        directories = [
            self.base_dir / "core",
            self.base_dir / "storage" / "local_memory",
            self.base_dir / "storage" / "personality_data",
            self.base_dir / "storage" / "learned_knowledge",
            self.base_dir / "gui",
            self.base_dir / "config",
            self.base_dir / "logs",
            self.onedrive_path / "memory_backup",
            self.onedrive_path / "learning_data",
            self.gdrive_path / "memory_backup",
            self.gdrive_path / "learning_data"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {directory}")

    def create_config_files(self):
        """Create configuration files"""
        print("\nInitializing configuration...")

        # System config
        system_config = {
            "version": "1.0.0",
            "installed_date": str(datetime.now()),
            "creator": "Joseph Dougherty",
            "company": "13th Chamber LLC"
        }

        config_file = self.base_dir / "config" / "system_config.json"
        with open(config_file, 'w') as f:
            json.dump(system_config, f, indent=4)
        print(f"✓ Created: {config_file}")

        # Cloud paths config
        cloud_config = {
            "onedrive_path": str(self.onedrive_path),
            "google_drive_path": str(self.gdrive_path),
            "sync_enabled": True
        }

        cloud_file = self.base_dir / "config" / "cloud_paths.json"
        with open(cloud_file, 'w') as f:
            json.dump(cloud_config, f, indent=4)
        print(f"✓ Created: {cloud_file}")

        # Memory config
        memory_config = {
            "max_memory_items": 10000,
            "auto_sync": True,
            "sync_frequency": "after_conversation"
        }

        memory_file = self.base_dir / "config" / "memory_config.json"
        with open(memory_file, 'w') as f:
            json.dump(memory_config, f, indent=4)
        print(f"✓ Created: {memory_file}")

    def initialize_databases(self):
        """Initialize empty databases"""
        print("\nInitializing databases...")

        # Memory database
        memory_db = {
            "interactions": [],
            "metadata": {
                "created": str(datetime.now()),
                "total_interactions": 0
            }
        }

        memory_file = self.base_dir / "storage" / "local_memory" / "memory_database.json"
        with open(memory_file, 'w') as f:
            json.dump(memory_db, f, indent=4)
        print(f"✓ Created: {memory_file}")

        # Learning database
        learning_db = {
            "patterns": {},
            "knowledge": [],
            "learning_level": 1,
            "metadata": {
                "created": str(datetime.now()),
                "total_learned": 0
            }
        }

        learning_file = self.base_dir / "storage" / "learned_knowledge" / "learning_database.json"
        with open(learning_file, 'w') as f:
            json.dump(learning_db, f, indent=4)
        print(f"✓ Created: {learning_file}")

    def create_readme(self):
        """Create README file"""
        readme_content = '''# QUANTUM A.I. SYSTEM
## Created by Joseph Dougherty, 13th Chamber LLC

### System Components:
- Core AI Engine (quantum_ai_core.py)
- 10 Personality System (personality_system.py)
- Memory Management (memory_manager.py)
- Learning Engine (learning_engine.py)
- Ethics Framework (ethics_framework.py)
- GUI Interface (chat_interface.py)

### To Launch:
1. Open Command Prompt
2. Navigate to C:\\QuantumAI
3. Run: python QuantumAI.py

### Cloud Storage:
- OneDrive: Automatic backup after conversations
- Google Drive: Secondary backup location

### Support:
- GitHub: github.com/13thchamberllc/quantum-ai-core
- Website: 13thchamberinc.com

Installation Date: {date}
'''
        readme_file = self.base_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write(readme_content.format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(f"\n✓ Created: {readme_file}")

    def install(self):
        """Run complete installation"""
        print("="*60)
        print("QUANTUM A.I. SYSTEM INSTALLER")
        print("Creator: Joseph Dougherty | 13th Chamber LLC")
        print("="*60)
        print()

        try:
            self.create_directories()
            self.create_config_files()
            self.initialize_databases()
            self.create_readme()

            print("\n" + "="*60)
            print("✓ INSTALLATION COMPLETE ✓")
            print("="*60)
            print("\nNext Steps:")
            print("1. Ensure all .py files are in correct folders")
            print("2. Run: pip install requests")
            print("3. Run: python QuantumAI.py")
            print("\nSystem is ready to launch!")

        except Exception as e:
            print(f"\n✗ Installation Error: {e}")
            print("Please contact support for assistance")

if __name__ == "__main__":
    installer = QuantumAIInstaller()
    installer.install()
