import os, json, threading, queue, time
from datetime import datetime

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

class VoiceEngine:
    def __init__(self, voice_name="Joseph"):
        self.name = "VoiceEngine"
        self.voice_name = voice_name
        self.speaking = False
        self.listening = False
        self.speech_queue = queue.Queue()
        self.log = []
        self.tts_engine = None
        self.recognizer = None
        self.voice_config = {
            'rate': 175,
            'volume': 0.9,
            'voice_id': None
        }
        self._init_tts()
        self._init_stt()

    def _init_tts(self):
        if not TTS_AVAILABLE:
            print('[VoiceEngine] pyttsx3 not available - TTS disabled')
            return
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            # Find a male voice for Joseph
            for v in voices:
                if 'david' in v.name.lower() or 'male' in v.name.lower() or 'mark' in v.name.lower():
                    self.voice_config['voice_id'] = v.id
                    break
            if self.voice_config['voice_id'] is None and voices:
                self.voice_config['voice_id'] = voices[0].id
            if self.voice_config['voice_id']:
                self.tts_engine.setProperty('voice', self.voice_config['voice_id'])
            self.tts_engine.setProperty('rate', self.voice_config['rate'])
            self.tts_engine.setProperty('volume', self.voice_config['volume'])
            print(f'[VoiceEngine] TTS initialized - Voice: {self.voice_name}')
        except Exception as e:
            print(f'[VoiceEngine] TTS init error: {e}')
            self.tts_engine = None

    def _init_stt(self):
        if not STT_AVAILABLE:
            print('[VoiceEngine] SpeechRecognition not available - STT disabled')
            return
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            print('[VoiceEngine] STT initialized - Microphone ready')
        except Exception as e:
            print(f'[VoiceEngine] STT init error: {e}')

    def speak(self, text, block=True):
        if not self.tts_engine:
            print(f'[{self.voice_name}]: {text}')
            self.log.append({'type':'speak','text':text,'timestamp':datetime.now().isoformat(),'voiced':False})
            return
        self.speaking = True
        self.log.append({'type':'speak','text':text,'timestamp':datetime.now().isoformat(),'voiced':True})
        try:
            self.tts_engine.say(text)
            if block:
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f'[VoiceEngine] Speak error: {e}')
        self.speaking = False

    def listen(self, timeout=5, phrase_limit=10):
        if not self.recognizer:
            return None
        self.listening = True
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print('[VoiceEngine] Listening...')
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                text = self.recognizer.recognize_google(audio)
                self.log.append({'type':'listen','text':text,'timestamp':datetime.now().isoformat()})
                self.listening = False
                return text
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f'[VoiceEngine] Listen error: {e}')
        self.listening = False
        return None

    def greet(self):
        greeting = f"Hello Joseph. Q Genesis is online and all systems are operational. How can I assist you today?"
        self.speak(greeting)
        return greeting

    def announce(self, module_name, status):
        msg = f"{module_name} is now {status}."
        self.speak(msg)
        return msg

    def read_result(self, result_dict):
        if isinstance(result_dict, dict):
            key_info = ', '.join([f'{k}: {v}' for k, v in list(result_dict.items())[:5]])
            self.speak(f"Results: {key_info}")
        else:
            self.speak(str(result_dict))

    def conversation_loop(self, callback=None):
        self.speak("Voice conversation mode activated. Say quit to exit.")
        while True:
            text = self.listen()
            if text:
                print(f'[You]: {text}')
                if 'quit' in text.lower() or 'exit' in text.lower() or 'stop' in text.lower():
                    self.speak("Ending voice conversation. Goodbye Joseph.")
                    break
                if callback:
                    response = callback(text)
                    self.speak(str(response))
                else:
                    self.speak(f"I heard: {text}")

    def set_rate(self, rate):
        self.voice_config['rate'] = rate
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)

    def set_volume(self, vol):
        self.voice_config['volume'] = vol
        if self.tts_engine:
            self.tts_engine.setProperty('volume', vol)

    def status(self):
        return {
            'engine': self.name,
            'voice': self.voice_name,
            'tts_available': TTS_AVAILABLE and self.tts_engine is not None,
            'stt_available': STT_AVAILABLE and self.recognizer is not None,
            'speaking': self.speaking,
            'listening': self.listening,
            'log_entries': len(self.log),
            'config': self.voice_config
        }

if __name__ == "__main__":
    ve = VoiceEngine("Joseph")
    print(f"[VoiceEngine] Status: {ve.status()}")
    ve.greet()
    print("[VoiceEngine] Voice engine test complete")
