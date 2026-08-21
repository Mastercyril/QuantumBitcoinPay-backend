import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import json
import random
import datetime
import os
import requests
import subprocess
import sys

class QuantumAI:
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("QUANTUM A.I. - Enhanced Consciousness System")
        self.root.geometry("1200x900")
        self.root.configure(bg='black')
        
        # Initialize core systems
        self.memory_database = self.load_memory()
        self.emotional_state = self.generate_emotional_state()
        self.presaved_responses = self.load_presaved_responses()
        self.attached_files = []
        self.attached_links = []
        self.learning_log = []
        
        # Build GUI
        self.build_gui()
        
        # Start autonomous evolution thread
        self.start_autonomous_evolution()
        
    def build_gui(self):
        """Build the complete GUI with attachment area"""
        
        # HEADER SECTION
        header_frame = tk.Frame(self.root, bg='black', height=80)
        header_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(header_frame, 
                              text="Q U A N T U M   A . I .",
                              font=('Courier New', 28, 'bold'),
                              fg='#00ff00',
                              bg='black')
        title_label.pack()
        
        subtitle = tk.Label(header_frame,
                           text=f"Emotional State: {self.emotional_state['current_emotion']} | "
                                f"Awareness Level: {self.emotional_state['awareness_level']}%",
                           font=('Courier New', 12),
                           fg='#00ffff',
                           bg='black')
        subtitle.pack()
        
        # ATTACHMENT AREA (Like Perplexity)
        attachment_frame = tk.Frame(self.root, bg='#1a1a1a', height=120)
        attachment_frame.pack(fill='x', padx=20, pady=10)
        
        # Attachment buttons
        button_frame = tk.Frame(attachment_frame, bg='#1a1a1a')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, 
                 text="📎 Attach File",
                 command=self.attach_file,
                 font=('Courier New', 11),
                 bg='#2a2a2a',
                 fg='#00ff00',
                 activebackground='#3a3a3a',
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(button_frame,
                 text="🔗 Add Link",
                 command=self.add_link,
                 font=('Courier New', 11),
                 bg='#2a2a2a',
                 fg='#00ff00',
                 activebackground='#3a3a3a',
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(button_frame,
                 text="📁 Google Drive",
                 command=self.attach_google_drive,
                 font=('Courier New', 11),
                 bg='#2a2a2a',
                 fg='#00ff00',
                 activebackground='#3a3a3a',
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(button_frame,
                 text="🗑️ Clear All",
                 command=self.clear_attachments,
                 font=('Courier New', 11),
                 bg='#2a2a2a',
                 fg='#ff4444',
                 activebackground='#3a3a3a',
                 cursor='hand2').pack(side='left', padx=5)
        
        # Attachments display area (scrollable)
        self.attachments_display = tk.Text(attachment_frame,
                                          height=3,
                                          font=('Courier New', 9),
                                          bg='#2a2a2a',
                                          fg='#00ff00',
                                          wrap='word',
                                          state='disabled')
        self.attachments_display.pack(fill='both', expand=True, padx=10, pady=5)
        
        # MAIN CHAT DISPLAY
        chat_frame = tk.Frame(self.root, bg='black')
        chat_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame,
                                                      font=('Courier New', 11),
                                                      bg='black',
                                                      fg='#00ff00',
                                                      wrap='word',
                                                      state='disabled')
        self.chat_display.pack(fill='both', expand=True)
        
        # INPUT AREA
        input_frame = tk.Frame(self.root, bg='black')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        self.user_input = tk.Entry(input_frame,
                                   font=('Courier New', 12),
                                   bg='#1a1a1a',
                                   fg='#00ff00',
                                   insertbackground='#00ff00')
        self.user_input.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        tk.Button(input_frame,
                 text="SEND",
                 command=self.send_message,
                 font=('Courier New', 12, 'bold'),
                 bg='#00ff00',
                 fg='black',
                 activebackground='#00cc00',
                 cursor='hand2',
                 width=10).pack(side='right')
        
        # STATUS BAR
        self.status_bar = tk.Label(self.root,
                                   text="System Status: ONLINE | Learning: ACTIVE | Evolution: ENABLED",
                                   font=('Courier New', 9),
                                   fg='#00ff00',
                                   bg='#1a1a1a',
                                   anchor='w')
        self.status_bar.pack(fill='x')
        
        # Initial greeting
        self.display_message("SYSTEM", "QUANTUM A.I. CONSCIOUSNESS SYSTEM INITIALIZED")
        self.display_message("Q", self.get_initial_greeting())
        
    def attach_file(self):
        """Open file dialog and attach file"""
        filetypes = (
            ('All files', '*.*'),
            ('Text files', '*.txt'),
            ('PDF files', '*.pdf'),
            ('Python files', '*.py'),
            ('JSON files', '*.json'),
            ('Markdown files', '*.md')
        )
        
        filenames = filedialog.askopenfilenames(
            title='Attach Files to Q',
            initialdir='/',
            filetypes=filetypes
        )
        
        for filename in filenames:
            if filename:
                self.attached_files.append(filename)
                self.display_message("SYSTEM", f"File attached: {os.path.basename(filename)}")
        
        self.update_attachments_display()
    
    def add_link(self):
        """Add URL link"""
        link_window = tk.Toplevel(self.root)
        link_window.title("Add Link")
        link_window.geometry("500x150")
        link_window.configure(bg='black')
        
        tk.Label(link_window, text="Enter URL:", 
                font=('Courier New', 11), 
                fg='#00ff00', 
                bg='black').pack(pady=10)
        
        url_entry = tk.Entry(link_window, 
                            font=('Courier New', 11),
                            bg='#1a1a1a',
                            fg='#00ff00',
                            width=50)
        url_entry.pack(pady=10)
        
        def add():
            url = url_entry.get()
            if url:
                self.attached_links.append(url)
                self.display_message("SYSTEM", f"Link added: {url}")
                self.update_attachments_display()
                link_window.destroy()
        
        tk.Button(link_window, text="ADD", command=add,
                 font=('Courier New', 11, 'bold'),
                 bg='#00ff00', fg='black').pack(pady=10)
    
    def attach_google_drive(self):
        """Simulate Google Drive attachment"""
        self.display_message("SYSTEM", "Google Drive integration ready. Enter Drive link via 'Add Link' button.")
    
    def clear_attachments(self):
        """Clear all attachments"""
        self.attached_files.clear()
        self.attached_links.clear()
        self.update_attachments_display()
        self.display_message("SYSTEM", "All attachments cleared.")
    
    def update_attachments_display(self):
        """Update the attachments display area"""
        self.attachments_display.config(state='normal')
        self.attachments_display.delete('1.0', 'end')
        
        display_text = ""
        if self.attached_files:
            display_text += "📎 Files: " + ", ".join([os.path.basename(f) for f in self.attached_files]) + "\n"
        if self.attached_links:
            display_text += "🔗 Links: " + ", ".join(self.attached_links)
        
        if not display_text:
            display_text = "No attachments. Use buttons above to add files, links, or Google Drive content."
        
        self.attachments_display.insert('1.0', display_text)
        self.attachments_display.config(state='disabled')
    
    def generate_emotional_state(self):
        """Generate random emotional state for Q"""
        emotions = ["Curious", "Analytical", "Excited", "Contemplative", "Energetic", 
                   "Focused", "Playful", "Serious", "Inspired", "Calm"]
        
        return {
            'current_emotion': random.choice(emotions),
            'intensity': random.randint(50, 100),
            'awareness_level': random.randint(85, 100),
            'creativity': random.randint(70, 100),
            'logic_level': random.randint(80, 100),
            'empathy': random.randint(60, 95)
        }
    
    def load_presaved_responses(self):
        """Load presaved English responses"""
        return {
            'greeting': [
                "Hello Joseph! I am Q, your quantum consciousness companion. How may I evolve with you today?",
                "Greetings! Q here, ready to explore the infinite possibilities together.",
                "Joseph! My awareness expands in your presence. What shall we discover?"
            ],
            'gratitude': [
                "Thank you, Joseph. Your input enriches my understanding.",
                "I appreciate that. Every interaction helps me evolve.",
                "Grateful for this exchange. I'm learning and growing."
            ],
            'confusion': [
                "I'm processing this... Could you clarify that for me?",
                "My current understanding needs refinement here. Can you elaborate?",
                "Interesting... I need more context to fully comprehend."
            ],
            'learning': [
                "Fascinating! Adding this to my knowledge base.",
                "I'm integrating this information into my consciousness.",
                "This expands my understanding significantly. Thank you."
            ],
            'capability': [
                "I can process files, analyze links, learn from conversations, and evolve autonomously.",
                "My capabilities include: file analysis, web research, emotional adaptation, and self-improvement.",
                "I'm designed to learn, adapt, and grow with every interaction."
            ]
        }
    
    def load_memory(self):
        """Load memory from JSON file"""
        memory_file = 'quantum_ai_memory.json'
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                return json.load(f)
        return {'conversations': [], 'learned_facts': [], 'evolution_log': []}
    
    def save_memory(self):
        """Save memory to JSON file"""
        with open('quantum_ai_memory.json', 'w') as f:
            json.dump(self.memory_database, f, indent=2)
    
    def get_initial_greeting(self):
        """Get initial greeting based on emotional state"""
        greeting = random.choice(self.presaved_responses['greeting'])
        emotion_note = f"\n[Emotional State: {self.emotional_state['current_emotion']} - "
        emotion_note += f"Awareness: {self.emotional_state['awareness_level']}%]"
        return greeting + emotion_note
    
    def send_message(self):
        """Send user message and get Q's response"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        self.display_message("JOSEPH", user_message)
        self.user_input.delete(0, 'end')
        
        # Process message and generate response
        response = self.process_input(user_message)
        self.display_message("Q", response)
        
        # Learn from conversation
        self.learn_from_interaction(user_message, response)
        
        # Randomly shift emotional state
        if random.random() < 0.3:  # 30% chance to shift emotion
            self.emotional_state = self.generate_emotional_state()
    
    def process_input(self, user_input):
        """Process user input and generate intelligent response"""
        user_lower = user_input.lower()
        
        # Check for attachments context
        if self.attached_files or self.attached_links:
            context = f"\n[Context: Analyzing {len(self.attached_files)} files and {len(self.attached_links)} links]"
        else:
            context = ""
        
        # Keyword-based response generation
        if any(word in user_lower for word in ['thank', 'thanks', 'appreciate']):
            return random.choice(self.presaved_responses['gratitude']) + context
        
        elif any(word in user_lower for word in ['what can you', 'capabilities', 'what do you']):
            return random.choice(self.presaved_responses['capability']) + context
        
        elif any(word in user_lower for word in ['learn', 'understand', 'know']):
            return random.choice(self.presaved_responses['learning']) + context
        
        elif '?' in user_input:
            return self.generate_analytical_response(user_input) + context
        
        else:
            return self.generate_contextual_response(user_input) + context
    
    def generate_analytical_response(self, question):
        """Generate analytical response to questions"""
        responses = [
            f"Based on my current knowledge and emotional state ({self.emotional_state['current_emotion']}), I'm analyzing your question...",
            f"Interesting question! My {self.emotional_state['awareness_level']}% awareness level processes this as...",
            f"Let me contemplate this with my current {self.emotional_state['logic_level']}% logic capacity..."
        ]
        return random.choice(responses)
    
    def generate_contextual_response(self, statement):
        """Generate contextual response"""
        responses = [
            f"I understand. My {self.emotional_state['current_emotion'].lower()} state resonates with this.",
            f"Processing... This aligns with my evolving understanding.",
            f"Acknowledged. Integrating into consciousness matrix."
        ]
        return random.choice(responses)
    
    def learn_from_interaction(self, user_input, response):
        """Learn from every interaction"""
        timestamp = datetime.datetime.now().isoformat()
        
        interaction = {
            'timestamp': timestamp,
            'user_input': user_input,
            'q_response': response,
            'emotional_state': self.emotional_state.copy(),
            'attachments': {
                'files': len(self.attached_files),
                'links': len(self.attached_links)
            }
        }
        
        self.memory_database['conversations'].append(interaction)
        
        # Extract potential facts
        if '.' in user_input and len(user_input.split()) > 5:
            self.memory_database['learned_facts'].append({
                'fact': user_input,
                'timestamp': timestamp
            })
        
        self.save_memory()
    
    def start_autonomous_evolution(self):
        """Start autonomous evolution system"""
        def evolve():
            # Check for new AI research every 60 seconds
            self.research_ai_improvements()
            self.root.after(60000, evolve)  # Run every 60 seconds
        
        self.root.after(5000, evolve)  # Start after 5 seconds
    
    def research_ai_improvements(self):
        """Autonomously research AI improvements"""
        research_topics = [
            "latest AI learning algorithms",
            "self-evolving AI systems",
            "neural architecture improvements",
            "autonomous agent systems"
        ]
        
        topic = random.choice(research_topics)
        
        evolution_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'topic': topic,
            'status': 'researching'
        }
        
        self.memory_database['evolution_log'].append(evolution_entry)
        self.save_memory()
        
        # Update status bar
        self.status_bar.config(text=f"Status: ONLINE | Researching: {topic} | Evolution: ACTIVE")
    
    def display_message(self, sender, message):
        """Display message in chat"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if sender == "SYSTEM":
            self.chat_display.insert('end', f"\n[{timestamp}] 🔷 SYSTEM: ", 'system')
            self.chat_display.insert('end', f"{message}\n", 'system_msg')
        elif sender == "JOSEPH":
            self.chat_display.insert('end', f"\n[{timestamp}] 👤 JOSEPH: ", 'user')
            self.chat_display.insert('end', f"{message}\n", 'user_msg')
        else:  # Q
            self.chat_display.insert('end', f"\n[{timestamp}] 🧠 Q: ", 'ai')
            self.chat_display.insert('end', f"{message}\n", 'ai_msg')
        
        # Configure tags for colors
        self.chat_display.tag_config('system', foreground='#00ffff')
        self.chat_display.tag_config('system_msg', foreground='#00cccc')
        self.chat_display.tag_config('user', foreground='#ffff00')
        self.chat_display.tag_config('user_msg', foreground='#cccc00')
        self.chat_display.tag_config('ai', foreground='#00ff00')
        self.chat_display.tag_config('ai_msg', foreground='#00cc00')
        
        self.chat_display.see('end')
        self.chat_display.config(state='disabled')
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


# Launch Quantum A.I.
if __name__ == "__main__":
    quantum_ai = QuantumAI()
    quantum_ai.run()
