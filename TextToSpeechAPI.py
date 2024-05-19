from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

def textToSpeech(text, lang='en', fileName='output.mp3'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(fileName)
    except Exception as e:
        return str(e)
    return fileName

@app.route('/text-to-speech', methods=['POST'])
def convert_text_to_speech():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    lang = data.get('lang', 'en')
    fileName = 'output.mp3'

    result = textToSpeech(text, lang, fileName)
    if isinstance(result, str) and result.endswith('.mp3'):
        try:
            return send_file(fileName, as_attachment=True)
        finally:
            os.remove(fileName)  # Clean up the file after sending
    else:
        return jsonify({"error": result}), 500

if __name__ == "__main__":
    app.run(debug=True)

