#!/usr/bin/env python3
# Quantum A.I. GUI Chat Interface
# Complete chat interface with instruction panel and web learning

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path("C:/QuantumAI/core")))

from quantum_ai_core import QuantumAICore

class QuantumAIInterface:
    """Main GUI interface for Quantum A.I."""

    def __init__(self, root):
        self.root = root
        self.root.title("Quantum A.I. - 13th Chamber LLC")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')

        # Initialize AI core
        self.ai_core = QuantumAICore()
        self.conversation_started = False

        # Create GUI
        self.create_widgets()

        # Display welcome message
        self.display_system_message("Quantum A.I. System Online")
        self.display_system_message("Created by Joseph Dougherty, 13th Chamber LLC")
        self.display_system_message("Type 'hello' to begin conversation")

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#0066cc', height=50)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="QUANTUM A.I.",
            font=("Arial", 20, "bold"),
            bg='#0066cc',
            fg='white'
        )
        title_label.pack(pady=10)

        # Status bar
        status_frame = tk.Frame(self.root, bg='#2a2a2a')
        status_frame.pack(fill=tk.X)

        self.status_label = tk.Label(
            status_frame,
            text="Status: Online | Personality: None | Memory: 0",
            font=("Arial", 10),
            bg='#2a2a2a',
            fg='#00ff00'
        )
        self.status_label.pack(pady=5)

        # Instruction panel
        instruction_frame = tk.LabelFrame(
            self.root,
            text="Instructions & Web Learning",
            font=("Arial", 10, "bold"),
            bg='#2a2a2a',
            fg='white'
        )
        instruction_frame.pack(fill=tk.X, padx=10, pady=5)

        # URL input
        url_frame = tk.Frame(instruction_frame, bg='#2a2a2a')
        url_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(
            url_frame,
            text="Learn from URL:",
            bg='#2a2a2a',
            fg='white'
        ).pack(side=tk.LEFT)

        self.url_entry = tk.Entry(url_frame, width=60)
        self.url_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            url_frame,
            text="Load",
            command=self.learn_from_url,
            bg='#0066cc',
            fg='white'
        ).pack(side=tk.LEFT)

        # Command input
        command_frame = tk.Frame(instruction_frame, bg='#2a2a2a')
        command_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(
            command_frame,
            text="System Command:",
            bg='#2a2a2a',
            fg='white'
        ).pack(side=tk.LEFT)

        self.command_entry = tk.Entry(command_frame, width=60)
        self.command_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            command_frame,
            text="Execute",
            command=self.execute_command,
            bg='#cc6600',
            fg='white'
        ).pack(side=tk.LEFT)

        # Chat display
        chat_frame = tk.LabelFrame(
            self.root,
            text="Conversation",
            font=("Arial", 10, "bold"),
            bg='#2a2a2a',
            fg='white'
        )
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 10),
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)

        # Input area
        input_frame = tk.Frame(self.root, bg='#2a2a2a')
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            input_frame,
            text="You:",
            bg='#2a2a2a',
            fg='white',
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)

        self.user_input = tk.Entry(
            input_frame,
            width=70,
            font=("Arial", 11)
        )
        self.user_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.user_input.bind('<Return>', lambda e: self.send_message())

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg='#00cc00',
            fg='white',
            font=("Arial", 10, "bold"),
            width=10
        )
        self.send_button.pack(side=tk.LEFT)

        # Control buttons
        control_frame = tk.Frame(self.root, bg='#2a2a2a')
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            control_frame,
            text="New Conversation",
            command=self.new_conversation,
            bg='#0066cc',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="View Memory",
            command=self.view_memory,
            bg='#cc00cc',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Learning Stats",
            command=self.show_learning_stats,
            bg='#cc6600',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Exit",
            command=self.exit_application,
            bg='#cc0000',
            fg='white'
        ).pack(side=tk.RIGHT, padx=5)

    def send_message(self):
        """Send user message and get AI response"""
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        # Display user message
        self.display_user_message(user_text)
        self.user_input.delete(0, tk.END)

        # Get AI response
        if not self.conversation_started:
            response = self.ai_core.start_conversation()
            self.conversation_started = True
        else:
            response = self.ai_core.process_input(user_text)

        # Display AI response
        self.display_ai_message(response)

        # Update status
        self.update_status()

    def display_user_message(self, message):
        """Display user message in chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[YOU]: {message}\n", "user")
        self.chat_display.tag_config("user", foreground="#00ccff")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def display_ai_message(self, message):
        """Display AI message in chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[Q]: {message}\n", "ai")
        self.chat_display.tag_config("ai", foreground="#00ff00")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def display_system_message(self, message):
        """Display system message in chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[SYSTEM]: {message}\n", "system")
        self.chat_display.tag_config("system", foreground="#ffff00")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def learn_from_url(self):
        """Learn from website URL"""
        url = self.url_entry.get().strip()
        if url:
            self.display_system_message(f"Learning from: {url}")
            result = self.ai_core.learn_from_website(url)
            self.display_system_message(result)
            self.url_entry.delete(0, tk.END)

    def execute_command(self):
        """Execute system command"""
        command = self.command_entry.get().strip()
        if command:
            self.display_system_message(f"Command: {command}")
            # Command processing would go here
            self.command_entry.delete(0, tk.END)

    def new_conversation(self):
        """Start new conversation"""
        if self.conversation_started:
            self.ai_core.end_conversation()
        self.conversation_started = False
        self.display_system_message("Starting new conversation...")
        self.update_status()

    def view_memory(self):
        """View memory statistics"""
        memory_count = self.ai_core.memory_manager.get_memory_count()
        messagebox.showinfo(
            "Memory Statistics",
            f"Total Interactions: {memory_count}"
        )

    def show_learning_stats(self):
        """Show learning statistics"""
        stats = self.ai_core.learning_engine.get_learning_stats()
        stats_text = f'''Learning Statistics:

Learning Level: {stats['learning_level']}
Total Learned: {stats['total_learned']}
Patterns Learned: {stats['patterns_learned']}
Knowledge Items: {stats['knowledge_items']}
'''
        messagebox.showinfo("Learning Statistics", stats_text)

    def update_status(self):
        """Update status bar"""
        status = self.ai_core.get_system_status()
        personality = status['personality'] or 'None'
        memory = status['memory_count']

        self.status_label.config(
            text=f"Status: Online | Personality: {personality} | Memory: {memory}"
        )

    def exit_application(self):
        """Exit application"""
        if self.conversation_started:
            self.ai_core.end_conversation()
        self.root.destroy()

def main():
    """Launch GUI application"""
    root = tk.Tk()
    app = QuantumAIInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
