# Does the repr method work as expected?
# Does is_following successfully detect when user1 is following user2?
# Does is_following successfully detect when user1 is not following user2?
# Does is_followed_by successfully detect when user1 is followed by user2?
# Does is_followed_by successfully detect when user1 is not followed by user2?
# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?

"""Message about models."""
import os 
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app
from models import db, User, Message, Follows
from unittest import TestCase
from test_user_model import UserModelTestCase

with app.app_context():
    db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""
    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.client = app.test_client()
        u1 = User.signup(
            "uniqueusername1", "uniqueemail1@email.com",None)

        u1.id = 1
        db.session.commit()

        m = Message(
            text="Hello World.",
            # timestamp=datetime.utcnow(),
            user_id=u1.id
        )

    def test_message_model(self):
        """Does basic model work?"""
        u = UserModelTestCase(u)
        self.assertEqual(len(u.messages), 1)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(Message.query.count(), 1)

    def test_text(self):
        """Is the text of the message correct?"""


    def test_timestamp(self):
        """Is the timestamp of the message correct?"""


    def test_user_id(self):
        """Is the user_id of the message correct?"""
