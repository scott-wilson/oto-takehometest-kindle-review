import unittest
from flask import Flask, json
from app.routes import routes


class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        routes.register_routes(self.app)
        self.client = self.app.test_client()

    def test_add_book_user(self):
        response = self.client.put(
            "/user/library/add/82f0ea02-de55-4b2c-abd0-171395b69193"
        )
        print("Output for test_add_book_user:", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_remove_book_user(self):
        response = self.client.delete(
            "/user/library/remove/82f0ea02-de55-4b2c-abd0-171395b69193"
        )
        print("Output for test_remove_book_user:", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_get_top_last_read(self):
        response = self.client.get("/user/library/top/last_read_date")
        print("Output for test_get_top_last_read:", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_get_top_last_read_page(self):
        response = self.client.get(
            "/user/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581/last_read_page"
        )
        print(
            "Output for test_get_top_last_read_page:", response.get_data(as_text=True)
        )
        self.assertEqual(response.status_code, 200)

    def test_get_book_metadata(self):
        response = self.client.get(
            "/user/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581/"
        )
        print("Output for test_get_book_metadata:", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
