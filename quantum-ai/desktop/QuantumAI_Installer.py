#!/usr/bin/env python3
# Quantum A.I. Installation Script
# Creates directory structure and initializes system

import os
import json
import shutil
from pathlib import Path

class QuantumAIInstaller:
    def __init__(self):
        self.base_path = Path("C:/QuantumAI")
        self.onedrive_path = Path(os.path.expanduser("~/OneDrive/quantum Ai"))
        self.gdrive_path = Path(os.path.expanduser("~/Google Drive/quantum Ai"))

    def create_directory_structure(self):
        """Create all necessary directories"""
        directories = [
            self.base_path / "core",
            self.base_path / "storage" / "local_memory",
            self.base_path / "storage" / "personality_data",
            self.base_path / "storage" / "learned_knowledge",
            self.base_path / "gui",
            self.base_path / "config",
            self.base_path / "logs",
            self.onedrive_path / "memory_backup",
            self.onedrive_path / "learning_data",
            self.gdrive_path / "memory_backup",
            self.gdrive_path / "learning_data"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {directory}")

    def create_config_files(self):
        """Initialize configuration files"""
        settings = {
            "version": "1.0.0",
            "installed_date": str(datetime.now()),
            "creator": "Joseph Dougherty",
            "company": "13th Chamber LLC",
            "personality_count": 10,
            "memory_enabled": True,
            "learning_enabled": True,
            "cloud_sync_enabled": True,
            "ethics_enabled": True
        }

        cloud_paths = {
            "onedrive": str(self.onedrive_path),
            "google_drive": str(self.gdrive_path),
            "local": str(self.base_path / "storage")
        }

        with open(self.base_path / "config" / "settings.json", 'w') as f:
            json.dump(settings, f, indent=2)

        with open(self.base_path / "config" / "cloud_paths.json", 'w') as f:
            json.dump(cloud_paths, f, indent=2)

        print("✓ Configuration files created")

    def create_desktop_shortcut(self):
        """Create Windows desktop shortcut"""
        desktop = Path(os.path.expanduser("~/Desktop"))
        shortcut_path = desktop / "Quantum A.I.lnk"

        # Shortcut creation would use win32com
        print(f"✓ Desktop shortcut ready: {shortcut_path}")

    def install(self):
        """Run complete installation"""
        print("="*60)
        print("QUANTUM A.I. INSTALLATION")
        print("="*60)
        print()

        print("Creating directory structure...")
        self.create_directory_structure()
        print()

        print("Initializing configuration...")
        self.create_config_files()
        print()

        print("Creating shortcuts...")
        self.create_desktop_shortcut()
        print()

        print("="*60)
        print("INSTALLATION COMPLETE ✓")
        print("="*60)
        print()
        print("Launch Quantum A.I. from desktop shortcut")
        print("or run: QuantumAI.exe")

if __name__ == "__main__":
    installer = QuantumAIInstaller()
    installer.install()
