import unittest
from flask import Flask, json
from app.routes import routes


class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        routes.register_routes(self.app)
        self.client = self.app.test_client()

    def test_add_book_user(self):
        response = self.client.get(
            "/user/library/add/uuid/ba6601d9-6b30-4287-a0d4-5737ea943294"
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_book_user(self):
        response = self.client.get(
            "/user/library/remove/uuid/ba6601d9-6b30-4287-a0d4-5737ea943294"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_top_last_read(self):
        response = self.client.get("/user/library/top/last_read_date")
        self.assertEqual(response.status_code, 200)

    def test_get_top_last_read_page(self):
        response = self.client.get(
            "/user/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581/last_read_page"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_book_metadata(self):
        response = self.client.get(
            "/user/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581/"
        )
        self.assertEqual(response.status_code, 200)

    # def test_get_book_global(self):
    #     response = self.client.get(
    #         "/global/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581"
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_get_book_global(self):
    #     response = self.client.get(
    #         "/global/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581"
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_get_book_user(self):
    #     response = self.client.get(
    #         "/user/library/uuid/8df99dcd-4042-40d6-b4d0-2f8615206581"
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_post_book_page_user(self):
    #     response = self.client.get(
    #         "user/library/ba6601d9-6b30-4287-a0d4-5737ea943294/25"
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_remove_book_user(self):
    #     response = self.client.get(
    #         "/user/library/add/uuid/ba6601d9-6b30-4287-a0d4-5737ea943294"
    #     )
    #     self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
