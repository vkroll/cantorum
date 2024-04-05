import unittest
from app import create_app, db
from app.services.user_service import register_user, add_person_data
from app.models import Login
from time import sleep
class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        username = "testuser"
        email = "test@example.com"
        password = "testpassword"

        # Call the service to register a new user
        user = register_user(username, email, password)

        # Assert that the user was created
        self.assertIsNotNone(user)

        # Retrieve the user from the database and assert details
        retrieved_user = Login.query.filter_by(email=email).first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, username) 
    def test_singer(self):
        user = register_user('singer', 'singer@ex.de', 'foo')
        person = add_person_data(user.email, 'Volker', 'Kroll')
        sleep(100)

if __name__ == '__main__':
    unittest.main()