# CS411-project
Moogle Books

Moogle Books is a flask based service that users can manage book related data including creating a logging in, searching for books, creating a bookshelf 
and maintaing a book shelf. Users can add books to their reading list and track their reading and receive book recommandation on those reads. 

Routes

**Health** 

Route: /health
Request Type: GET
Purpose: Health check route to verify the service is running
Request Body: None
Response Format: JSON
Success Response Example:             
  'status': 'success',
  'message': 'Service is running'
      
Example Request: GET /api/health
Example Response: 
  'status': 'success',
  'message': 'Service is running'

**Create Account**
Route: /create-account
Request Type: PUT
Purpose: Register A new account
Request Body: 
  Username: string
  Passowrd: string

Response Format: JSON
Success Response Example:             
  "status": "success",
  "message": "User '{username}' created successfully"
      
Example Request: 
  "username": "newuser",
  "password": "newpassword"
  
Example Response: 
  "status": "success",
  "message": "User 'newuser' created successfully"

**login**
Route: /login
Request Type: POST
Purpose: Authenticate a user 
Request Body: 
  Username: string
  Passowrd: string

Response Format: JSON
Success Response Example:             
  "status": "success",
  "message": "User '{username}' logged in successfully"
      
Example Request: 
  "username": "existinguser",
  "password": "correctpassword"

  
Example Response: 
  "status": "success",
  "message": "User 'existinguser' logged in successfully"

**log-out**
Route: /logout
Request Type: POST
Purpose: Log out the user
Request Body: N/A
Response Format: JSON
Success Response Example:             
  "status": "success",
  "message": "User logged out successfully"
      
Example Request: POST /api/logout

Example Response: 
  "status": "success",
  "message": "User logged out successfully"

**change password**
Route: /change-password
Request Type: POST
Purpose: to change the passoword of the user.
Request Body: 
  "new_password": "string"
  
Response Format: JSON
Success Response Example:             
  Code: 200
  Content: { "message": "Account created successfully" }

      
Example Request: POST /api/change-password

Example Response: 
  "status": "success",
  "message": "Password changed successfully"

**Search Books**
Route: /api/search-books
Request Type: GET
Purpose: Search for books using Google Books API.
Request Body:
"query": "string",
"max_results": "int"

Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "books": [book_list] }

Example Request: GET /api/search-books?query=python&max_results=5
Example Response:
"status": "success"
"books": [book_list]

**Book Details**
Route: /api/book-details/book_id
Request Type: GET
Purpose: Get detailed information about a specific book.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "book": book_details }

Example Request: GET /api/book-details/12345
Example Response:
"status": "success"
"book": book_details

**Reading List**
Route: /api/add-to-reading-list
Request Type: POST
Purpose: Add a book to the reading list.
Request Body:
"book_id": "string"

Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Book added to reading list" }

Example Request: POST /api/add-to-reading-list
Example Response:
"status": "success"
"message": "Book added to reading list"

**Start Reading**
Route: /api/start-reading
Request Type: POST
Purpose: Move a book from reading list to currently reading.
Request Body:
"book_id": "string"

Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Book moved to currently reading" }

Example Request: POST /api/start-reading
Example Response:
"status": "success"
"message": "Book moved to currently reading"

**Mark as Read**
Route: /api/mark-as-read
Request Type: POST
Purpose: Mark a book as completed.
Request Body:
"book_id": "string"

Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Book marked as read" }

Example Request: POST /api/mark-as-read
Example Response:
"status": "success"
"message": "Book marked as read"

**Remove Book**
Route: /api/remove-book
Request Type: POST
Purpose: Remove a book from a specific list.
Request Body:
"book_id": "string",
"list_type": "string" (Optional, defaults to 'reading_list')

Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Book removed from {list_type}" }

Example Request: POST /api/remove-book
Example Response:
"status": "success"
"message": "Book removed from reading list"

**Get Reading List**
Route: /api/get-reading-list
Request Type: GET
Purpose: Get all books in the reading list.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "books": [book_list] }

Example Request: GET /api/get-reading-list
Example Response:
"status": "success"
"books": [book_list]

**Get Current Reads**
Route: /api/get-current-reads
Request Type: GET
Purpose: Get all books currently being read.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "books": [book_list] }

Example Request: GET /api/get-current-reads
Example Response:
"status": "success"
"books": [book_list]

**Get Completed Books**
Route: /api/get-completed-books
Request Type: GET
Purpose: Get all completed books.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "books": [book_list] }

Example Request: GET /api/get-completed-books
Example Response:
"status": "success"
"books": [book_list]

**Get Recommendations**
Route: /api/get-recommendations
Request Type: GET
Purpose: Get book recommendations based on completed books.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "recommendations": [book_list] }

Example Request: GET /api/get-recommendations
Example Response:
"status": "success"
"recommendations": [book_list]

**Reset Users**
Route: /api/reset-users
Request Type: DELETE
Purpose: Recreate the users table to delete all users.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Users table recreated successfully" }

Example Request: DELETE /api/reset-users
Example Response:
"status": "success"
"message": "Users table recreated successfully"

**Reset Books**
Route: /api/reset-books
Request Type: DELETE
Purpose: Recreate the books table to delete all books.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Books table recreated successfully" }

Example Request: DELETE /api/reset-books
Example Response:
"status": "success"
"message": "Books table recreated successfully"

**Clear Shelf**
Route: /api/clear-shelf
Request Type: POST
Purpose: Clear all lists in the shelf.
Response Format: JSON
Success Response Example:
Code: 200
Content: { "status": "success", "message": "Shelf cleared successfully" }

Example Request: POST /api/clear-shelf
Example Response:
"status": "success"
"message": "Shelf cleared successfully"

  
