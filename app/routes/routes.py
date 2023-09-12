from flask import Blueprint, request, jsonify
from app.controller.business import (
    find_book,
    add_book_user,
    subtract_book_user,
    find_top_book_user,
    change_book_page_user,
    add_book_global,
    list_books,
)


global_json = "data.json"
user_json = "user_library/user_library.json"


book_routes = Blueprint("book_routes", __name__)
# Type hints, please!


def register_routes(app):
    app.register_blueprint(book_routes)


@book_routes.route("/user/books", methods=["GET"])
def get_all_books_user():
    # Have the REST api functions be responsible for formatting the data for the REST
    # response.
    return list_books(user_json)


@book_routes.route("/global/books", methods=["GET"])
def get_all_books_global():
    return list_books(global_json)


@book_routes.route(
    "/global/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/global/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_global(key, value, target=None):
    return find_book(key, value, global_json, target=target)


@book_routes.route(
    "/user/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/user/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_user(key, value, target=None):
    return find_book(key, value, user_json, target=target)


@book_routes.route("/user/books/<uuid>", methods=["PUT"])
def add_book_to_user_library(uuid):
    return add_book_user(uuid, global_json, user_json)


@book_routes.route("/global/books", methods=["PUT"])
def add_book_to_global_library():
    data = request.get_json()
    # We don't know the shape of the data in the request. This should be documented in
    # some way.
    return add_book_global(data, global_json)


@book_routes.route("/user/books/<uuid>", methods=["DELETE"])
def remove_book_from_user_library(uuid):
    return subtract_book_user(uuid, user_json)


@book_routes.route("/user/books/top/<target>", methods=["GET"])
def get_top_user_book(target=None):
    return find_top_book_user(user_json, target=target)


@book_routes.route("/user/books/last_read", methods=["GET"])
def get_last_user_book():
    return find_top_book_user(user_json, "last_read_date")


@book_routes.route("/user/books/<uuid>/page/<page_number>", methods=["POST"])
def update_book_page_for_user(uuid, page_number):
    return change_book_page_user(uuid, page_number, user_json)
