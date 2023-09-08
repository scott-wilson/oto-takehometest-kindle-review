## Kindle application
### Task: Build a basic backend python flask application for a kindle app. The assumptions, requirements and the task details are mentioned below.

### Features to implement:
1. Add a new book to the library

2. Remove a book from the library

3. Return the last read book

4. Return the last read page number of a book

5. Return metadata of a book: title, author, year, language, percentage of book read and last read page number. All as a single json

6. Add a data access layer to the system

7. Containerize the application using Docker

### You may assume that
1. A user is already created and authenticated

2. The user is logged in

3. An empty library exists for the user

4. The actual text of the book is automatically grouped into pages. Meaning, you don't need to worry about splitting the book's content into pages.

5. The front-end is a kindle device that will use this backend system to render the books

6. The `data.json` file is the global kindle library.

### Supporting Information

1. Please note that you are building a backend system that will be deployed to the cloud. You need to build the APIs and functionalities for the features mentioned above

2. Feel free to add / update the model class and the database fields as necessary. Please do not delete any existing field(s)

3. Feel free to add more books to the database. Please do not delete any existing book(s)

### Evaluation
1. The app should be able to run on localhost port 5000 (default port for a python flask application)

2. The APIs will be invoked through postman and tested
