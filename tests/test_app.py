# APP TESTING


import unittest
import os
os.environ['TESTING'] = 'true'
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "elaine.png" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        response2 = self.client.post("/api/timeline_post", data={
            "name": "Tony the Tiger",
            "email": "tony@frostedflakes.com",
            "content": "They're grrrrrrrrreat!",
        })
        assert response2.status_code == 200

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]['name'] == "Tony the Tiger"
        assert json["timeline_posts"][0]['email'] == "tony@frostedflakes.com"
        assert json["timeline_posts"][0]['content'] == "They're grrrrrrrrreat!"

    # Edge cases; application of TDD
    def test_malformed_timeline_post(self):

        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
        # TODO: Fix code to pass cases

if __name__ == '__main__':
    unittest.main()
