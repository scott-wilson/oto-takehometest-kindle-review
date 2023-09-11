from flask import Blueprint, request, jsonify
from app.controller.business import (
    find_book,
    add_book_user,
    subtract_book_user,
    find_top_book_user,
    change_book_page_user,
    add_book_global,
)


global_json = "data.json"
user_json = "user_library/user_library.json"


book_routes = Blueprint("book_routes", __name__)


def register_routes(app):
    app.register_blueprint(book_routes)


@book_routes.route(
    "/global/library/<key>/<value>/", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/global/library/<key>/<value>/<target>", methods=["GET"])
def get_book_global(key, value, target=None):
    return find_book(key, value, global_json, target=target)


@book_routes.route(
    "/user/library/<key>/<value>/", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/user/library/<key>/<value>/<target>", methods=["GET"])
def get_book_user(key, value, target=None):
    return find_book(key, value, user_json, target=target)


@book_routes.route("/user/library/add/<uuid>", methods=["PUT"])
def put_book_user(uuid):
    return add_book_user(uuid, global_json, user_json)


@book_routes.route("/global/library/add", methods=["PUT"])
def put_book_global():
    data = request.get_json()
    return add_book_global(data, global_json)


@book_routes.route("/user/library/remove/<uuid>", methods=["DELETE"])
def delete_book_user(uuid):
    return subtract_book_user(uuid, user_json)


@book_routes.route("/user/library/top/<target>", methods=["GET"])
def get_top_book_user(target=None):
    return find_top_book_user(user_json, target=target)


@book_routes.route("/user/library/<uuid>/<page_number>", methods=["POST"])
def post_book_page_user(uuid, page_number):
    return change_book_page_user(uuid, page_number, user_json)
