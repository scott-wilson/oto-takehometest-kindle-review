from typing import Optional
from app.model import kindle_model

# I suggest setting up mypy for type checking, black for auto-formatting, and
# ruff for linting.


# Allowed keys should look like `list[str]`, and dict should look like `dict[str, str]`.
# Or, allowed keys should look like `typing.Iterable[str]`.
def validate_target(target: str, allowed_keys: list) -> dict:
    """Validate that the target is either None or one of the allowed keys."""
    # According to the type hints, target cannot be None.
    # This might be simplified to simply `if target not in allowed_keys:`.
    if target is not None and target not in allowed_keys:
        # Instead of returning, why not raise an exception? You can have the calling
        # code handle if an exception is raised. Also, should this data be sent to the
        # user, or should it be developer only information while a user gets an "its
        # broken" error?
        return {
            "status": "failed",
            "reason": f"Invalid target. Allowed keys for searching are {', '.join(allowed_keys)}.",
        }
    # Returning None, even though the function is annotated to return a dict.
    return None


# No annotation for return.
# It looks like nothing really makes much use of this function. Could either remove or
# update the rest of the code to use this function. But it is two lines... Could
# probably just remove this and use the underlying functions everywhere.
def list_books(library_path: str):
    library_instance = kindle_model.Library(library_path)
    return library_instance.list_books()


# No annotation for return.
def find_book(key: str, value: str, library_path: str, target: Optional[str] = None):
    # Maybe have this as a global?
    allowed_keys = [
        "pages",
        "year",
        "last_read_page",
        "percentage_read",
        "last_read_date",
        "author",
        "country",
        "imageLink",
        "language",
        "link",
        "title",
        "uuid",
    ]

    # Target is a str or None, so validate_target is sending a type error because it
    # only expects a str.
    validation_error = validate_target(target, allowed_keys)
    if validation_error:
        # I think this should raise an error at this point (assuming the validate_target
        # doesn't already).
        return validation_error

    library_instance = kindle_model.Library(library_path)
    found = library_instance.find_books(**{key: value})

    if not found:
        # This should probably be an exception.
        return {"status": "failed", "reason": "No books found matching the criteria."}

    if target:
        return [book.get(target) for book in found]
    else:
        return found


# No annotation for return.
def add_book_user(book_uuid: str, global_library_path: str, user_library_path: str):
    user_library_instance = kindle_model.Library(user_library_path)
    global_library_instance = kindle_model.Library(global_library_path)

    # So, going further with the idea of raising exceptions when something goes wrong, I
    # think it is okay/a good idea to have all of the functions here return the data in
    # a way that is not formatted for the REST API, and just deal with making stuff REST
    # compatible near the end of the process.

    found_user = user_library_instance.find_books(uuid=book_uuid)
    if found_user:
        return {"status": "failed", "reason": "Book already exists in user's library."}

    found_global = global_library_instance.find_books(uuid=book_uuid)
    if not found_global:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in the global library.",
        }

    add_book = kindle_model.Book.from_json(found_global[0])
    user_library_instance.add_book(add_book)
    return {"status": "success", "book added": found_global}


# No annotation for return.
# The data doesn't describe the shape other than it is a dict. I think this should just
# take a book instance instead.
def add_book_global(data: dict, global_library_path: str):
    global_library_instance = kindle_model.Library(global_library_path)
    new_book = kindle_model.Book.from_dict(data)
    global_library_instance.add_book(new_book)
    return {"status": "success", "book added": new_book.to_dict()}


# No annotation for return.
def subtract_book_user(book_uuid: str, user_library_path: str):
    user_library_instance = kindle_model.Library(user_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)

    if not found_user:
        return {"status": "failed", "reason": "Book not found in the user library."}

    # What should happen if remove_book fails?
    user_library_instance.remove_book(book_uuid)
    return {
        "status": "success",
        "book removed": found_user,
        "remaining_books": user_library_instance.list_books(),
    }


# No annotation for return.
def find_top_book_user(user_library_path: str, target: Optional[str] = None):
    allowed_keys = [
        "pages",
        "year",
        "last_read_page",
        "percentage_read",
        "last_read_date",
    ]

    validation_error = validate_target(target, allowed_keys)
    if validation_error:
        return validation_error

    user_library_instance = kindle_model.Library(user_library_path)
    books_user = user_library_instance.list_books()

    if not books_user:
        return {"status": "failed", "reason": "No books in user's library."}

    # COuld use max(books_user, key=...) instead.
    sorted_books = sorted(
        books_user, key=lambda book: book.get(target, float("-inf")), reverse=True
    )
    return {"status": "success", f"highest_value: {target}": sorted_books[0]}


# No annotation for return.
def change_book_page_user(book_uuid: str, page_number: str, user_library_path: str):
    try:
        page_number = int(page_number)
    except ValueError:
        return {"status": "failed", "reason": "Page number must be an integer."}

    user_library_instance = kindle_model.Library(user_library_path)
    found_books = user_library_instance.find_books(uuid=book_uuid)

    if not found_books:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in user's library.",
        }

    total_pages = found_books[0].get("pages", None)
    if total_pages is not None and page_number > total_pages:
        return {
            "status": "failed",
            "reason": "Page number exceeds total pages of the book.",
        }

    user_library_instance.update_reading_status(book_uuid, page_number)
    updated_book = user_library_instance.find_books(uuid=book_uuid)

    return {"status": "success", "updated_book": updated_book}
