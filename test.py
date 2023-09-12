import unittest
from flask import Flask, json
from app.routes import routes


# Make sure the tests validate the following:
# - All the success conditions.
# - All the failure conditions.
# - All the edge cases.

# I usually format my test argument name like this:
# test_<function_name>_<condition>_<expected_result>_<reason>
# For example, test_add_book_to_user_library_success.
# Or, test_add_book_to_user_library_failure_book_does_not_exist.


class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        routes.register_routes(self.app)
        self.client = self.app.test_client()

    def test_get_all_books_user(self):
        response = self.client.get("/user/books")
        self.assertEqual(response.status_code, 200)

    def test_get_all_books_global(self):
        response = self.client.get("/global/books")
        self.assertEqual(response.status_code, 200)

    def test_search_book_global(self):
        response = self.client.get("/global/books/search/title/Oedipus the King")
        self.assertEqual(response.status_code, 200)

    def test_search_book_global_with_target(self):
        response = self.client.get("/global/books/search/title/Oedipus the King/author")
        self.assertEqual(response.status_code, 200)

    def test_search_book_user(self):
        response = self.client.get("/user/books/search/title/Oedipus the King")
        self.assertEqual(response.status_code, 200)

    def test_search_book_user_with_target(self):
        response = self.client.get("/user/books/search/title/Oedipus the King/author")
        self.assertEqual(response.status_code, 200)

    def test_get_last_user_book(self):
        response = self.client.put("/user/books/last_read")
        self.assertEqual(response.status_code, 200)

    def test_add_book_to_user_library(self):
        response = self.client.put("/user/books/82f0ea02-de55-4b2c-abd0-171395b69193")
        self.assertEqual(response.status_code, 200)

    def test_add_book_to_global_library(self):
        mock_data = {
            "author": "Test",
            "country": "Test",
            "imageLink": "Test",
            "language": "Test",
            "link": "https://en.wikipedia.org/wiki/Anna_Karenina\n",
            "pages": 864,
            "title": "Anna Karenina",
            "year": 1877,
            "last_read_page": 0,
            "percentage_read": 0.0,
            "last_read_date": 0.0,
        }
        response = self.client.put("/global/books", json=mock_data)
        self.assertEqual(response.status_code, 200)

    def test_remove_book_from_user_library(self):
        response = self.client.delete(
            "/user/books/82f0ea02-de55-4b2c-abd0-171395b69193"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_top_user_book(self):
        response = self.client.get("/user/books/top/last_read_date")
        self.assertEqual(response.status_code, 200)

    def test_update_book_page_for_user(self):
        response = self.client.post(
            "/user/books/82f0ea02-de55-4b2c-abd0-171395b69193/page/123"
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
