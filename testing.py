import unittest 

from server import app
from model import *
from flask import Flask, render_template, redirect, request, flash, session, jsonify, g 
from flask_debugtoolbar import DebugToolbarExtension


class NextBookTests(unittest.TestCase):
    """Test NextBook site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def test_homepage(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Goals", result.data)

    def test_login(self):
        """Test search page inital rendering"""

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Email", result.data)

    def test_register_form(self):
        """Test register page intital rendering"""

        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Sign Up", result.data)



if __name__ == "__main__": 

    unittest.main()
    init_app()