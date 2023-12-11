from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test that the homepage shows the board."""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'<table class="board">', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["A", "B", "C", "D", "E"],
                                 ["F", "G", "H", "I", "J"],
                                 ["K", "L", "M", "N", "O"],
                                 ["P", "Q", "R", "S", "T"],
                                 ["U", "V", "W", "X", "Y"]]

            response = self.client.get('/check-word?guess=abc')
            self.assertEqual(response.json['result'], 'not-word')

    def test_invalid_word(self):
        """Test if word is in the dictionary but not on the board."""

        self.client.get('/')
        response = self.client.get('/check-word?guess=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if non-english word is identified."""

        self.client.get('/')
        response = self.client.get('/check-word?guess=fsjdakfkldsfjdsl')
        self.assertEqual(response.json['result'], 'not-word')

    def test_reset_game(self):
        """Test if game resets."""

        with self.client:
            self.client.get('/')
            session['board'] = [["A", "B", "C", "D", "E"],
                                ["F", "G", "H", "I", "J"],
                                ["K", "L", "M", "N", "O"],
                                ["P", "Q", "R", "S", "T"],
                                ["U", "V", "W", "X", "Y"]]
            response = self.client.post('/reset-game')
            self.assertNotEqual(session['board'], [["A", "B", "C", "D", "E"],
                                                   ["F", "G", "H", "I", "J"],
                                                   ["K", "L", "M", "N", "O"],
                                                   ["P", "Q", "R", "S", "T"],
                                                   ["U", "V", "W", "X", "Y"]])
            self.assertEqual(response.json['message'], 'Game reset successfully!')

    def test_score_tracking(self):
        """Test if score is being tracked."""

        with self.client:
            self.client.get('/')
            response = self.client.post('/track-score', json={"score": 100})
            self.assertEqual(session['highest_score'], 100)
            self.assertEqual(response.json['message'], 'Score tracked successfully!')