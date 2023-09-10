## Kindle Backend API Documentation

This API is designed for managing books in a Kindle application. The API allows users to interact with both a global library and a user-specific library.

### Base URL:

All API requests are made to `http://localhost:5000/`

### Endpoints:

```
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
```

#### 1. Get a Book from the Global Library:

- **URL**: `/global/library/<key>/<value>/` or `/global/library/<key>/<value>/<target>`
- **Method**: `GET`
- **Parameters**:
  - `key`: The field by which to search (e.g., "title", "author").
  - `value`: The value to search for in the specified key.
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves a book from the global library based on the provided key-value pair. If a target is provided, only that attribute of the book will be returned.

#### 2. Get a Book from the User Library:

- **URL**: `/user/library/<key>/<value>/` or `/user/library/<key>/<value>/<target>`
- **Method**: `GET`
- **Parameters**:
  - `key`: The field by which to search (e.g., "title", "author").
  - `value`: The value to search for in the specified key.
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves a book from the user's library based on the provided key-value pair. If a target is provided, only that attribute of the book will be returned.

#### 3. Add a Book to the User Library:

- **URL**: `/user/library/add/<uuid>`
- **Method**: `PUT`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
- **Description**: Adds a book from the global library to the user's library using the provided UUID.

#### 4. Add a Book to the Global Library:

- **URL**: `/global/library/add/<uuid>`
- **Method**: `PUT`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
  - `data` (Request Body): JSON object containing book details.
- **Description**: Adds a new book to the global library.

#### 5. Remove a Book from the User Library:

- **URL**: `/user/library/remove/<uuid>`
- **Method**: `DELETE`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
- **Description**: Removes a book from the user's library.

#### 6. Get the highest value of the specified target from the User Library:

- **URL**: `/user/library/top/<target>`
- **Method**: `GET`
- **Parameters**:
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves the target with the highest value from the user's library. If a target is provided, only that attribute of the book will be returned.

#### 7. Update the Last Read Page of a Book in the User Library:

- **URL**: `/user/library/<uuid>/<page_number>`
- **Method**: `POST`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
  - `page_number`: The page number to update.
- **Description**: Updates the last read page number for a specific book in the user's library.

## Kindle Backend API Documentation
