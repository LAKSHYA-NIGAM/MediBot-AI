"""
MediBot-AI - User Authentication and Session Unit Tests
-------------------------------------------------------
Validates user registration, password hashing, login flow,
and chat history persistence in SQLite.
"""
import os
import sys
import unittest
import tempfile

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


class MediBotAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        os.environ["DATABASE_PATH"] = self.temp_db.name

        from auth import init_db, auth_bp
        from flask import Flask
        init_db()

        self.app = Flask(
            __name__,
            template_folder=os.path.join(PROJECT_DIR, 'templates'),
            static_folder=os.path.join(PROJECT_DIR, 'static')
        )
        self.app.secret_key = "test-secret-key"
        self.app.register_blueprint(auth_bp)

        @self.app.route("/")
        def index():
            return "INDEX_PAGE"

        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            try:
                os.unlink(self.temp_db.name)
            except OSError:
                pass

    def test_01_user_registration_success(self):
        """Verify successful user registration and session creation."""
        response = self.client.post("/register", data={
            "username": "dr_john",
            "email": "dr_john@hospital.org",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"INDEX_PAGE", response.data)

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("username"), "dr_john")
            self.assertIsNotNone(sess.get("user_id"))

    def test_02_registration_password_mismatch(self):
        """Verify registration failure on password mismatch."""
        response = self.client.post("/register", data={
            "username": "dr_smith",
            "email": "dr_smith@hospital.org",
            "password": "passwordA123",
            "confirm_password": "passwordB456"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"INDEX_PAGE", response.data)

    def test_03_registration_short_password(self):
        """Verify password length requirement enforcement (>= 6 chars)."""
        response = self.client.post("/register", data={
            "username": "short_user",
            "email": "short@example.com",
            "password": "123",
            "confirm_password": "123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"INDEX_PAGE", response.data)

    def test_04_duplicate_username_rejection(self):
        """Verify rejection of duplicate username or email."""
        self.client.post("/register", data={
            "username": "unique_user",
            "email": "unique@example.com",
            "password": "securepass123",
            "confirm_password": "securepass123"
        })

        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.post("/register", data={
            "username": "unique_user",
            "email": "another@example.com",
            "password": "securepass123",
            "confirm_password": "securepass123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"INDEX_PAGE", response.data)

    def test_05_login_success(self):
        """Verify login succeeds with valid credentials."""
        self.client.post("/register", data={
            "username": "login_test",
            "email": "login@example.com",
            "password": "validpassword",
            "confirm_password": "validpassword"
        })

        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.post("/login", data={
            "username": "login_test",
            "password": "validpassword"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"INDEX_PAGE", response.data)

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("username"), "login_test")

    def test_06_login_invalid_password(self):
        """Verify login rejection with incorrect password."""
        self.client.post("/register", data={
            "username": "patient_01",
            "email": "p01@example.com",
            "password": "correctpassword",
            "confirm_password": "correctpassword"
        })

        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.post("/login", data={
            "username": "patient_01",
            "password": "wrongpassword"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"INDEX_PAGE", response.data)

    def test_07_logout_clears_session(self):
        """Verify logout endpoint clears user session."""
        self.client.post("/register", data={
            "username": "logout_user",
            "email": "logout@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })

        response = self.client.get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        with self.client.session_transaction() as sess:
            self.assertNotIn("user_id", sess)
            self.assertNotIn("username", sess)

    def test_08_chat_history_persistence(self):
        """Verify saving and retrieving user chat messages."""
        from auth import save_chat_message, get_chat_history
        user_id = 999

        save_chat_message(user_id, "user", "What are symptoms of diabetes?")
        save_chat_message(user_id, "bot", "Common symptoms include increased thirst, frequent urination, and fatigue.")

        history = get_chat_history(user_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["message"], "What are symptoms of diabetes?")
        self.assertEqual(history[1]["role"], "bot")


if __name__ == "__main__":
    unittest.main(verbosity=2)
