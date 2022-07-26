# test_db.py

from sqlite3 import Time
import unittest
from peewee import *
import os
os.environ['TESTING'] = 'true'
from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests
test_database = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_database.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_database.connect()
        test_database.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_database.drop_tables(MODELS)

        # Close connection to db.
        test_database.close()

    def test_timeline_post(self):
        #Create 2 timeline posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        posts = TimelinePost.select()
        assert posts[0].name == "John Doe"
        assert posts[1].email == "jane@example.com"

if __name__ == '__main__':
    unittest.main()
