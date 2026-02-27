# Magic-Voice-Control
Lightweight Python-based voice recognition for Harry Potter games. Speak to cast spells and experience the magic hands-free.

🌟 The Story Behind the Magic
This project wasn't born in a high-tech lab with expensive gear. It was born out of a passion for the Wizarding World and a personal challenge to overcome hardware limitations.

For years, I kept my ideas hidden in a "vacant theater," waiting for the perfect time or the perfect equipment. But then I realized: The magic is in the code, not the desk. I built this assistant using Python and Vosk to ensure it's fast, offline, and runs on almost any machine. It’s a testament that you don't need a massive setup to start creating—you just need a spark of inspiration and the courage to take the first step.

🚀 Features
Ultra-Lightweight: Designed to run in the background without affecting game performance.

Offline Recognition: Powered by the Vosk engine—no internet required, ensuring privacy and zero latency.

Customizable Spells: Easily map your voice commands to any in-game keybinds.

Minimalist UI: Built with PyQt6 for a clean and simple user experience.

🛠️ Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/aryantaker/Magic-Voice-Control.git
Install Dependencies:

Bash
pip install vosk pyaudio PyQt6 pydirectinput
Download the Model:

Download a compatible lightweight model from Vosk Models.

Extract it into a folder named model in the project root.

Run the Wizardry:

Bash
python voice_command.py
📜 How to Cast Spells
The current version is pre-configured for basic commands. You can modify the update_text function in voice_command.py to add your favorite spells:

Say "Lumos" to light up your way (Maps to L).

Say "Nox" to extinguish the light.

Add your own custom elif statements for Expelliarmus, Alohomora, and more!

🤝 Contributing
This is an open-source project, and I am looking for fellow "wizards" to help expand it!

Want to add multi-language support?

Want to improve the UI?

Have a better way to simulate keypresses?

Feel free to fork this repo, create a branch, and submit a Pull Request. Let’s build the ultimate gaming assistant together.

🏛️ License
This project is licensed under the MIT License.

✉️ Final Word from the Author
"Even in the darkest of times, one can find happiness, if one only remembers to turn on the light... or in this case, code the light."
