import unittest
from unittest.mock import patch
from flask import json
from TextToSpeechAPI import app, textToSpeech

class TextToSpeechTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_no_text_provided(self):
        response = self.app.post('/text-to-speech', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No text provided"})

    @patch('TextToSpeechAPI.textToSpeech', return_value='output.mp3')
    def test_text_to_speech_success(self, mock_text_to_speech):
        response = self.app.post('/text-to-speech', json={'text': 'hello world', 'lang': 'en'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Disposition'].startswith('attachment; filename=output.mp3'))

    @patch('TextToSpeechAPI.textToSpeech', return_value='An error occurred')
    def test_text_to_speech_failure(self, mock_text_to_speech):
        response = self.app.post('/text-to-speech', json={'text': 'hello world', 'lang': 'en'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "An error occurred"})

if __name__ == "__main__":
    unittest.main()

