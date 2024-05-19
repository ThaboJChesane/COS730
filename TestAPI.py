import unittest
from unittest.mock import patch
from flask import Flask
from flask_testing import TestCase
import json
import pandas as pd
import numpy as np

# Import the Flask app from RecommenderAPI.py
from RecommenderAPI import app, recommendBooks

class TestRecommenderAPI(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('RecommenderAPI.reviews', pd.DataFrame({
        'UserId': ['user1', 'user2', 'user3'],
        'BookTitle': ['Book A', 'Book B', 'Book C'],
        'Review': [5.0, 4.0, 3.0]
    }))
    @patch('RecommenderAPI.x', pd.DataFrame({
        'user1': [1, 0, 0],
        'user2': [0, 1, 0],
        'user3': [0, 0, 1]
    }, index=['user1', 'user2', 'user3']))
    @patch('RecommenderAPI.cosine_sim', np.array([
        [1, 0.1, 0.2],
        [0.1, 1, 0.3],
        [0.2, 0.3, 1]
    ]))
    #

    def testRecommendMissingUserId(self):
        with self.client:
            response = self.client.get('/recommend')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)

    @patch('RecommenderAPI.recommendBooks')
    def testRecommendInvalidUser(self, mockRecommendBooks):
        mockRecommendBooks.side_effect = Exception('User not found')
        with self.client:
            response = self.client.get('/recommend?user_id=invalid_user')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
