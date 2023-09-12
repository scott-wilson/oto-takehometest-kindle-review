import json
from datetime import datetime
from typing import Union, Dict, Optional, List
import uuid


# This could make use of dataclasses. EIther that, or use a library like pydantic.
class Book:
    def __init__(
        self,
        author: str,
        country: str,
        image_link: str,
        language: str,
        link: str,
        pages: int,
        title: str,
        year: int,
        book_uuid: Optional[str] = None,
        last_read_page: Optional[int] = 0,
        percentage_read: Optional[float] = 0.0,
        last_read_date: Optional[float] = None,
    ):
        self.author = author
        self.country = country
        self.image_link = image_link
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.uuid = book_uuid
        self.last_read_page = last_read_page
        self.percentage_read = percentage_read
        self.last_read_date = last_read_date

    @classmethod
    def from_json(cls, json_data: Union[str, Dict]) -> "Book":
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            return cls.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON data for creating a Book instance: {e}")

    @classmethod
    def from_dict(cls, data: Dict) -> "Book":
        return cls(
            author=data["author"],
            country=data["country"],
            image_link=data["imageLink"],
            language=data["language"],
            link=data["link"],
            pages=data["pages"],
            title=data["title"],
            year=data["year"],
            book_uuid=data.get("uuid", str(uuid.uuid4())),
            last_read_page=data.get("last_read_page", 0),
            percentage_read=data.get("percentage_read", 0.0),
            last_read_date=data.get("last_read_date", 0.0),
        )

    def to_json(self) -> str:
        return json.dumps(self.metadata())

    # This code uses 3.7 compatible type hints, but the app/controller/business.py is
    # using 3.9+. Should be consistent.
    def to_dict(self) -> Dict[str, Union[str, int, float]]:
        return self.metadata()

    def metadata(self) -> Dict[str, Union[str, int, float]]:
        # Type hint is failing because the union does not contain all of the possible
        # types. Consider having the return type be a TypedDict.
        return {
            "author": self.author,
            "country": self.country,
            "imageLink": self.image_link,
            "language": self.language,
            "link": self.link,
            "pages": self.pages,
            "title": self.title,
            "year": self.year,
            "uuid": self.uuid,
            "last_read_page": self.last_read_page,
            "percentage_read": self.percentage_read,
            "last_read_date": self.last_read_date,
        }


# What's ExtendedBook for? Why not just Book?
class ExtendedBook(Book):
    def update_last_read_date(self) -> None:
        """Update the last read date."""
        self.last_read_date = datetime.now().timestamp()

    def update_uuid(self) -> None:
        """Update the uuid."""
        self.uuid = str(uuid.uuid4())

    def update_last_read_page(self, last_read_page: int) -> None:
        """Update the last read page and calculate the reading percentage."""
        self.last_read_page = last_read_page
        self.percentage_read = (last_read_page / self.pages) * 100 if self.pages else 0


class Library:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.books = self.load_library()

    def load_library(self) -> List[ExtendedBook]:
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            books = [ExtendedBook.from_json(book) for book in data]

            self.books = books
            updated = False
            for book in self.books:
                # Use is instead of ==.
                # When would the book not have a UUID?
                if book.uuid == None:
                    # This can either be a book class or an extended book class. Only
                    # the extended book class has the update_uuid method.
                    book.update_uuid()
                    updated = True

            # Use is instead of ==. Or just `if updated:`.
            if updated == True:
                self.save_library()
            return self.books
        except json.JSONDecodeError:
            return []

    def save_library(self) -> None:
        with open(self.data_file, "w") as f:
            json.dump([book.metadata() for book in self.books], f, indent=4)

    def add_book(self, book: ExtendedBook) -> None:
        self.books.append(book)
        # Is it a good idea to save here? What if the user wants to add multiple books?
        # I'd suggest having the save be done outside of this method and make it
        # explicit.
        self.save_library()

    def remove_book(self, uuid: str) -> None:
        self.books = [book for book in self.books if book.uuid != uuid]
        self.save_library()

    def list_books(self) -> List[Dict]:
        return [book.metadata() for book in self.books]

    def find_books(self, **kwargs) -> List[Dict]:
        # I personally don't like the use of kwargs like this. It would be better to do
        # something like...
        # `find_books(self, query: dict[str, Any]) -> list[dict[str, Any]]`
        # Although, if you can avoid using any, that would be better.
        found_books = []
        for book in self.books:
            if all(getattr(book, key, None) == value for key, value in kwargs.items()):
                found_books.append(book.metadata())
        return found_books

    def update_reading_status(self, uuid: str, last_read_page: int) -> None:
        for book in self.books:
            if book.uuid == uuid:
                # This can either be a book class or an extended book class. Only
                # the extended book class has the update_last_read_* methods.
                book.update_last_read_date()
                book.update_last_read_page(int(last_read_page))
                self.save_library()
                break
