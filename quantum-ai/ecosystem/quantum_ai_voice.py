#!/usr/bin/env python3
"""
Quantum AI - Joseph Voice Assistant
All-in-one local implementation (no external APIs)
Uses: Ollama (Gemma) + pyttsx3 (local TTS)
"""

import ollama
import pyttsx3
import sys

class QuantumAIVoice:
    def __init__(self):
        # Initialize local text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.setup_joseph_voice()
        
        # Codex for formal assistant tone
        self.system_codex = """You are Quantum AI, a formal research assistant created by Joseph Dougherty.
        You specialize in quantum computing, physics, biotechnology, and drug discovery research.
        Respond with precision, clarity, and technical accuracy using formal academic tone.
        Keep responses concise but thorough. This session uses Joseph voice synthesis."""
        
        self.model = "gemma:latest"
        print("✅ Quantum AI initialized with Joseph voice")
    
    def setup_joseph_voice(self):
        """Configure TTS engine for Joseph voice characteristics"""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find a suitable male voice
        for voice in voices:
            if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Voice settings for formal tone
        self.tts_engine.setProperty('rate', 175)     # Speed (150-200 for formal)
        self.tts_engine.setProperty('volume', 0.9)   # Volume (0.0 to 1.0)
        
        print(f"🎙️ Voice configured: {self.tts_engine.getProperty('voice')}")
    
    def query_gemma(self, user_prompt):
        """Query Ollama Gemma model with system codex"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_codex},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error connecting to Ollama: {e}\nMake sure Ollama is running with: ollama serve"
    
    def speak(self, text):
        """Convert text to speech using Joseph voice"""
        print("\n🎙️ Speaking response...")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def process_query(self, user_input):
        """Main processing: Gemma response + voice output"""
        # Check for voice activation codex
        voice_enabled = "CODEX:VOICE" in user_input.upper() or "VOICE:" in user_input.upper()
        user_input = user_input.replace("CODEX:VOICE", "").replace("VOICE:", "").strip()
        
        print(f"\n🔬 Quantum AI processing: {user_input}")
        print("⏳ Generating response...\n")
        
        # Get response from Gemma
        response = self.query_gemma(user_input)
        
        print("─" * 70)
        print("📝 RESPONSE:")
        print("─" * 70)
        print(response)
        print("─" * 70)
        
        # Voice output if codex present or always-on
        if voice_enabled or self.always_voice:
            self.speak(response)
        
        return response
    
    def interactive_mode(self):
        """Run interactive terminal session"""
        print("\n" + "=" * 70)
        print("QUANTUM AI - JOSEPH VOICE ASSISTANT")
        print("=" * 70)
        print("Powered by: Gemma (Ollama) + Local TTS")
        print("Created by: Joseph Dougherty")
        print("=" * 70)
        print("\nCommands:")
        print("  • Type your query and press Enter")
        print("  • Prefix with 'CODEX:VOICE' or 'VOICE:' to enable voice")
        print("  • Type 'voice on' to enable voice for all responses")
        print("  • Type 'voice off' to disable voice")
        print("  • Type 'exit' or 'quit' to stop")
        print("=" * 70)
        
        self.always_voice = False
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'stop', 'q']:
                    print("\n🔴 Shutting down Quantum AI...")
                    break
                
                if user_input.lower() == 'voice on':
                    self.always_voice = True
                    print("✅ Voice enabled for all responses")
                    continue
                
                if user_input.lower() == 'voice off':
                    self.always_voice = False
                    print("🔇 Voice disabled")
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🔴 Shutting down Quantum AI...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def single_query(self, query, use_voice=True):
        """Process a single query (for programmatic use)"""
        self.always_voice = use_voice
        return self.process_query(query)


def main():
    """Entry point"""
    # Create Quantum AI instance
    ai = QuantumAIVoice()
    
    # Check if query provided as command-line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        ai.single_query(query, use_voice=True)
    else:
        # Run interactive mode
        ai.interactive_mode()


if __name__ == "__main__":
    main()
