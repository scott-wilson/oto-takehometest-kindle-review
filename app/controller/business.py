from app.model import kindle_model


def find_book(key, value, library, target=None):
    # List of allowed keys for sorting
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

    # Validate that the target is either None or one of the allowed keys
    if target is not None and target not in allowed_keys:
        return {
            "status": "failed",
            "reason": f"Invalid target. Allowed keys for searching are {', '.join(allowed_keys)}.",
        }

    # Initialize the Library object from the kindle_model with the given user_library
    library = kindle_model.Library(library)

    # Search for books that match the given key-value criteria in the library
    found = library.find_books(**{key: value})

    # If no books are found, return a 'failed' status
    if not found:
        return {"status": "failed", "reason": "No books found matching the criteria."}

    # If a target attribute is specified, return only that attribute for all found books
    if target:
        return [book.get(target) for book in found]
    else:
        return found


def add_book_user(uuid, global_library, user_library):
    # Initialize the Library object from the kindle_model with the given user_library
    user_library = kindle_model.Library(user_library)
    global_library = kindle_model.Library(global_library)

    # Check if the book with the given UUID already exists in the user's library
    found_user = user_library.find_books(uuid=uuid)
    if found_user:
        return {"status": "failed", "reason": "Book already exists in user's library."}

    # Check if the book with the given UUID exists in the global library
    found_global = global_library.find_books(uuid=uuid)
    if not found_global:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in the global library.",
        }

    add_book = kindle_model.Book.from_json(found_global[0])
    user_library.add_book(add_book)
    return {"status": "success", "book added": found_global}


def add_book_global(uuid, data, global_library):
    # Initialize the Library object from the kindle_model with the given user_library
    global_library = kindle_model.Library(global_library)
    found_global = global_library.find_books(uuid=uuid)
    if found_global:
        return {
            "status": "failed",
            "reason": "Book already exists in the global library.",
        }
    new_book = kindle_model.Book.from_dict(data)
    global_library.add_book(new_book)
    return {"status": "success", "book added": data}


def subtract_book_user(uuid, user_library):
    # Use the updated find_book function for validation and book searching
    user_library = kindle_model.Library(user_library)
    found_user = user_library.find_books(uuid=uuid)
    if not found_user:
        return {
            "status": "failed",
            "reason": "Book not found in the user library.",
        }

    user_library.remove_book(uuid)
    return {
        "status": "success",
        "book removed": found_user,
        "remaining_books": user_library.list_books(),
    }


def find_top_book_user(user_library, target=None):
    # List of allowed keys for sorting
    allowed_keys = [
        "pages",
        "year",
        "last_read_page",
        "percentage_read",
        "last_read_date",
    ]

    # Validate that the target is either None or one of the allowed keys
    if target is not None and target not in allowed_keys:
        return {
            "status": "failed",
            "reason": f"Invalid target. Allowed keys for sorting are {', '.join(allowed_keys)}.",
        }

    # Initialize the Library object from the kindle_model with the given user_library
    user_library = kindle_model.Library(user_library)

    # Get the list of books in the user's library
    books_user = user_library.list_books()
    if not books_user:
        return {"status": "failed", "reason": "No books in user's library."}

    # Sort the books based on the target attribute, in descending order
    def sort_key(book):
        value = book.get(target)
        if value is None:
            return (
                float("-inf") - 1
            )  # This ensures that None values are treated as less than any float
        return value

    sorted_books = sorted(books_user, key=sort_key, reverse=True)

    return {"status": "success", f"highest_value: {target}": sorted_books[0]}


def change_book_page_user(uuid, page_number, user_library):
    # Validate that the page_number is an integer
    page_number = int(page_number)
    if page_number == None:
        return {"status": "failed", "reason": "Page number must be an integer."}

    user_library = kindle_model.Library(user_library)

    # Check if the book with the given UUID exists in the user's library
    found_books = user_library.find_books(uuid=uuid)
    if not found_books:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in user's library.",
        }

    # Get the first found book's metadata (assuming unique UUIDs)
    found_book = found_books[0]

    # Check if the new page number is valid (not greater than total pages)
    total_pages = found_book.get("pages", None)
    if total_pages is not None and page_number > total_pages:
        return {
            "status": "failed",
            "reason": "Page number exceeds total pages of the book.",
        }

    # Update the reading status
    user_library.update_reading_status(uuid, page_number)

    # Fetch updated book metadata
    updated_book = user_library.find_books(uuid=uuid)

    return {"status": "success", "updated_book": updated_book}
