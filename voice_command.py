import sys
import os
import json
import vosk
import pyaudio
import difflib
import pydirectinput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal

# 🔹 1. Path configuration for executable and script modes
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model")
SPELLS_FILE = os.path.join(BASE_DIR, "spells.txt")

# 🔹 2. Background thread for voice processing to keep UI responsive
class VoiceThread(QThread):
    recognized_text = pyqtSignal(str)

    def __init__(self, model, mic_index):
        super().__init__()
        self.model = model
        self.mic_index = mic_index
        self.running = True

    def run(self):
        samplerate = 16000
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=samplerate, input=True,
                            frames_per_buffer=4000, input_device_index=self.mic_index)
            rec = vosk.KaldiRecognizer(self.model, samplerate)

            while self.running:
                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        self.recognized_text.emit(text)
            
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"Microphone Error: {e}")
        finally:
            p.terminate()

    def stop(self):
        self.running = False

# 🔹 3. Main UI Class
class HarryPotterMagicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_model()
        self.voice_thread = None

    def initUI(self):
        self.setWindowTitle("Harry Potter Voice Control 🪄")
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Waiting...")
        layout.addWidget(self.status_label)

        self.result_label = QLabel("Last Heard: ---")
        layout.addWidget(self.result_label)

        # Microphone selection dropdown
        self.mic_combo = QComboBox()
        self.populate_mics()
        layout.addWidget(self.mic_combo)

        self.btn_start = QPushButton("Start Magic")
        self.btn_start.clicked.connect(self.start)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop)
        layout.addWidget(self.btn_stop)

        self.setLayout(layout)

    def populate_mics(self):
        """ Detects available audio input devices """
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            self.mic_combo.addItem(info['name'], i)
        p.terminate()

    def load_model(self):
        """ Loads the Vosk speech recognition model """
        try:
            if not os.path.exists(MODEL_PATH):
                self.status_label.setText("Error: Model folder missing!")
                return
            self.model = vosk.Model(MODEL_PATH)
            self.status_label.setText("Vosk Model Loaded ✅")
        except Exception as e:
            self.status_label.setText(f"Load Error: {e}")

    def start(self):
        """ Starts the voice recognition thread """
        mic_idx = self.mic_combo.currentData()
        self.voice_thread = VoiceThread(self.model, mic_idx)
        self.voice_thread.recognized_text.connect(self.process_voice)
        self.voice_thread.start()
        self.status_label.setText("Listening for Spells... 👂")

    def stop(self):
        """ Stops the voice recognition thread """
        if self.voice_thread:
            self.voice_thread.stop()
            self.status_label.setText("Magic Paused ⏸️")

    def process_voice(self, text):
        """ Matches recognized voice to spell list using fuzzy matching """
        self.result_label.setText(f"Heard: {text}")
        
        # Default spell list
        valid_spells = ["stupefy", "confringo", "expulso", "petrificus", "protego", "leviosa", "patronum"]
        
        # Load custom spells from file if it exists
        if os.path.exists(SPELLS_FILE):
            with open(SPELLS_FILE, "r") as f:
                valid_spells = [line.strip().lower() for line in f.readlines() if line.strip()]

        # Find the closest match
        matches = difflib.get_close_matches(text.lower(), valid_spells, n=1, cutoff=0.6)
        
        if matches:
            spell = matches[0]
            self.cast_spell(spell)

    def cast_spell(self, spell):
        """ Maps spell names to in-game keyboard/mouse actions """
        self.status_label.setText(f"Casting: {spell.upper()} ✨")
        
        try:
            if spell == "stupefy":
                pydirectinput.click() # Basic attack
            elif spell == "confringo":
                pydirectinput.press('2') # Select explosive spell
                pydirectinput.click()
            elif spell == "expulso":
                pydirectinput.press('3') # Rapid fire
                pydirectinput.click()
            elif spell == "petrificus":
                pydirectinput.press('4') # Stun
                pydirectinput.click()
            elif spell == "protego":
                pydirectinput.press('q') # Shield/Defend
            elif spell == "leviosa":
                pydirectinput.press('5') # Interaction
            elif spell == "patronum":
                pydirectinput.press('6') # Dementor defense
        except Exception as e:
            print(f"Control Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HarryPotterMagicApp()
    ex.show()
    sys.exit(app.exec())