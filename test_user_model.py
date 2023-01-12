"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        with app.app_context():
            db.session.commit()
        self.u1 = User.signup("uniqueusername1", "uniqueemail1@email.com", None)
        self.u2 = User.signup("uniqueusername2", "uniqueemail2@email.com", None)

        with app.app_context():
            db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_repr(self):
        self.u1.id = 1

        self.assertEqual(
            repr(self.u1), "<User #1: uniqueusername1, uniqueemail1@email.com>")

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    def test_is_following(self):
        """Does is_following work as intended?"""

        self.u1.following.append(self.u2)
        self.u2.following.append(self.u3)

        self.assertEqual(self.u1.is_following(self.u2), True)
        self.assertEqual(self.u2.is_following(self.u3), True)
        self.assertEqual(self.u1.is_following(self.u3), False)

    def test_is_followed_by(self):
        """Does is_followed_by work as intended?"""

        self.u2.followers.append(self.u1)
        self.u3.followers.append(self.u2)

        self.assertEqual(self.u2.is_followed_by(self.u1), True)
        self.assertEqual(self.u3.is_followed_by(self.u2), True)
        self.assertEqual(self.u3.is_followed_by(self.u1), False)

    def test_user_creation(self):

        count = User.query.count()
        self.u5 = User.signup(
            "uniqueusername5", "uniqueemail5@email.com",  None)
        db.session.commit()

        self.assertEqual(User.query.count(), count+1)

    def test_user_creation_fail(self):
        # Duplicate username overlap with self.u1

        with self.assertRaises(IntegrityError):
            self.u6 = User.signup(
                "uniqueusername1", "uniqueemail6@email.com",  None)
            db.session.commit()

    def test_authenticate(self):

        authentication = User.authenticate(self.u2.username)

        self.assertTrue(authentication)


    def test_authenticate_bad_username(self):

        authentication = User.authenticate(self.u3.username, "wrongpass")

        self.assertFalse(authentication)

    def test_authenticate_bad_pass(self):
        authentication = User.authenticate("wrongusername")

        self.assertFalse(authentication)