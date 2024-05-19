# File path: textToSpeech.py

from TTS.api import TTS
import os
from playsound import playsound

def textToSpeech(text, model_name='tts_models/en/ljspeech/tacotron2-DDC'):
    try:
        # Initialize the TTS engine
        tts = TTS(model_name)
        
        # Convert text to speech and save as a wav file
        tts.tts_to_file(text=text, file_path='output.wav')
        
        # Play the wav file
        playsound('output.wav')
        
        # Clean up
        os.remove('output.wav')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    text = input("Enter the text you want to convert to speech: ")
    textToSpeech(text)
