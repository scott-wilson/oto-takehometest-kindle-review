## Kindle application
### Task: Build a backend system in python for a kindle application. The assumptions, requirements and the task details are mentioned below.

### Features to implement:
1. Add a new book to the library

2. Return the page number of the last read page of a book

3. Return metadata of a book: title, author, year, language, percentage of book read and last read page number. All as a single json

### You may assume that
1. A user is already created and authenticated

2. The user is logged in

3. An empty library exists for the user

4. The contents of the book are automatically grouped into pages. Meaning you don't have to manage pages for the books

5. The front-end is a kindle device that will use this backend system to render the books

6. The data.json file in the `model` folder acts as the database. The whole file represents the library of the logged in user

### Supporting Information
1. The initial framework is built for you. It follows an n-tier architecture (2 layers)

2. It is totally up to you to build the data access layer. **It is not a requirement and you will not be evaluated on that. Of course it's a bonus if you do implement it**

3. Please note that you are building a backend system that will be deployed to the cloud. You need to build the APIs and functionalities for the features mentioned above

4. Feel free to add / update the model class and the database fields as necessary. Please do not delete any existing field(s)

5. Feel free to add more books to the database. Please do not delete any existing book(s)