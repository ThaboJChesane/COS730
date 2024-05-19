# File path: textToSpeech.py
# File path: textToSpeech.py

from gtts import gTTS
import os
from playsound import playsound

def textToSpeech(text, lang='en', fileName='output.mp3'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(fileName)
        playsound(fileName)
        os.remove(fileName)  # Remove the file after playing to save space
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    text = input("Enter the text you want to convert to speech: ")
    textToSpeech(text)

