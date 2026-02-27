import sys
import os
import json
import time
import vosk
import pyaudio
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal

# 🔹 proccesing voice 
class VoiceRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # sending text to UI

    def __init__(self, model, mic_index,parent=None):
        super().__init__(parent)
        self.model = model
        self.mic_index = mic_index
        self.is_listening = True

    def run(self):
        samplerate = 16000  
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=samplerate, input=True,
                        frames_per_buffer=4000, input_device_index=self.mic_index)
        rec = vosk.KaldiRecognizer(self.model, samplerate)

        while self.is_listening:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result["text"]
                self.recognized_text.emit(text)  # 🔹 sending voice to UI

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self.is_listening = False


# 🔹 main class of application
class VoiceCommandApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Command App")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.start_listening)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Listening")
        self.stop_button.clicked.connect(self.stop_listening)
        self.layout.addWidget(self.stop_button)

        self.text_label = QLabel("Recognized Text: ")
        self.layout.addWidget(self.text_label)

        self.mic_combo = QComboBox()
        self.populate_microphones()
        self.layout.addWidget(self.mic_combo)

        self.loading_label = QLabel("Loading... Please wait.")
        self.layout.addWidget(self.loading_label)

        self.setLayout(self.layout)

        print("Loading Vosk Model...")
        try:
            self.model = vosk.Model("model")
            print("Vosk Model loaded successfully!")
            self.loading_label.setText("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.loading_label.setText(f"Error loading model: {e}")

        self.voice_thread = None

    def populate_microphones(self):
        """ detecting microphone """
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            self.mic_combo.addItem(info['name'], i)
        p.terminate()

    def start_listening(self):
        """ starting voice record """
        if self.voice_thread and self.voice_thread.isRunning():
            return  
        mic_index = self.mic_combo.currentData()
        self.voice_thread = VoiceRecognitionThread(self.model, mic_index, self)
        self.voice_thread.recognized_text.connect(self.update_text)  # 🔹 connecting to UI
        self.voice_thread.start()
        self.text_label.setText("Listening...")

    def stop_listening(self):
        """ stoping recording voice"""
        if self.voice_thread:
            self.voice_thread.stop()
            self.voice_thread.wait()
        self.text_label.setText("Stopped Listening.")

    def update_text(self, text):
        """ updating text in UI """
        self.text_label.setText(f"Recognized: {text}")
        print(f"Recognized text: {text}")
        if "notepad" in text:
            os.system("notepad.exe")
        elif "shutdown" in text:
            os.system("shutdown /s /t 10")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceCommandApp()
    window.show()
    sys.exit(app.exec())
