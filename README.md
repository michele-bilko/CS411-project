# CS411-project
Moogle Books

Moogle Books is a flask based service that users can manage book related data including creating a logging in, searching for books, creating a bookshelf 
and maintaing a book shelf. Users can add books to their reading list and track their reading and receive book recommandation on those reads. 

Routes

**Health** 

Route: /health <br/>
Request Type: GET <br/>
Purpose: Health check route to verify the service is running <br/>
Request Body: None <br/>
Response Format: JSON <br/>
Success Response Example: <br/>
  'status': 'success', <br/>
  'message': 'Service is running' <br/>
      
Example Request: GET /api/health <br/>
Example Response:  <br/>
  'status': 'success', <br/>
  'message': 'Service is running' <br/>

**Create Account** <br/>
Route: /create-account <br/>
Request Type: PUT <br/>
Purpose: Register A new account <br/>
Request Body:  <br/>
  Username: string <br/>
  Passowrd: string <br/>

Response Format: JSON <br/>
Success Response Example: <br/>
  "status": "success", <br/>
  "message": "User '{username}' created successfully" <br/>
      
Example Request:  <br/>
  "username": "newuser", <br/>
  "password": "newpassword" <br/>
  
Example Response:  <br/>
  "status": "success", <br/>
  "message": "User 'newuser' created successfully" <br/>

**login** <br/>
Route: /login <br/>
Request Type: POST <br/>
Purpose: Authenticate a user  <br/>
Request Body:  <br/>
  Username: string <br/>
  Passowrd: string <br/>

Response Format: JSON <br/>
Success Response Example: <br/>    
  "status": "success", <br/>
  "message": "User '{username}' logged in successfully" <br/>
      
Example Request:  <br/>
  "username": "existinguser", <br/>
  "password": "correctpassword" <br/>

Example Response: <br/>
  "status": "success", <br/>
  "message": "User 'existinguser' logged in successfully" <br/>

**log-out** <br/>
Route: /logout <br/>
Request Type: POST <br/>
Purpose: Log out the user <br/>
Request Body: N/A <br/>
Response Format: JSON <br/>
Success Response Example:  <br/> 
  "status": "success", <br/>
  "message": "User logged out successfully" <br/>
      
Example Request: POST /api/logout <br/>

Example Response: <br/>
  "status": "success", <br/>
  "message": "User logged out successfully" <br/>

**change password** <br/>
Route: /change-password <br/>
Request Type: POST <br/>
Purpose: to change the passoword of the user. <br/>
Request Body:  <br/>
  "new_password": "string" <br/>
  
Response Format: JSON <br/>
Success Response Example:              <br/>
  Code: 200 <br/>
  Content: { "message": "Account created successfully" } <br/>

      
Example Request: POST /api/change-password <br/>

Example Response:  <br/>
  "status": "success", <br/>
  "message": "Password changed successfully" <br/>

**Search Books** <br/>
Route: /api/search-books <br/>
Request Type: GET <br/>
Purpose: Search for books using Google Books API. <br/>
Request Body: <br/>
"query": "string", <br/>
"max_results": "int" <br/>

Response Format: JSON <br/>
Success Response Example: <br/>
Code: 200 <br/>
Content: { "status": "success", "books": [book_list] } <br/>

Example Request: GET /api/search-books <br/>
Example Response: <br/>
"status": "success" <br/>
"books": [book_list] <br/>

**Book Details** <br/>
Route: /api/book-details/book_id <br/>
Request Type: GET <br/>
Purpose: Get detailed information about a specific book. <br/>
Response Format: JSON <br/>
Success Response Example: <br/>
Code: 200 <br/>
Content: { "status": "success", "book": book_details } <br/>

Example Request: GET /api/book-details <br/>
Example Response: <br/>
"status": "success" <br/>
"book": book_details <br/>

**Reading List** <br/>
Route: /api/add-to-reading-list <br/>
Request Type: POST <br/>
Purpose: Add a book to the reading list. <br/>
Request Body: <br/>
"book_id": "string" <br/>

Response Format: JSON <br/>
Success Response Example: <br/>
Code: 200 <br/>
Content: { "status": "success", "message": "Book added to reading list" } <br/>

Example Request: POST /api/add-to-reading-list <br/>
Example Response: <br/>
"status": "success" <br/>
"message": "Book added to reading list" <br/>

**Start Reading** <br/>
Route: /api/start-reading <br/>
Request Type: POST <br/>
Purpose: Move a book from reading list to currently reading. <br/>
Request Body: <br/>
"book_id": "string" <br/>

Response Format: JSON <br/>
Success Response Example: <br/>
Code: 200 <br/>
Content: { "status": "success", "message": "Book moved to currently reading" } <br/>

Example Request: POST /api/start-reading <br/>
Example Response: <br/>
"status": "success" <br/>
"message": "Book moved to currently reading" <br/>
 
**Mark as Read**<br/>
Route: /api/mark-as-read<br/>
Request Type: POST<br/>
Purpose: Mark a book as completed.<br/>
Request Body:<br/>
"book_id": "string"<br/>

Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "message": "Book marked as read" }<br/>

Example Request: POST /api/mark-as-read <br/>
Example Response:<br/>
"status": "success"<br/>
"message": "Book marked as read"<br/>

**Remove Book**<br/>
Route: /api/remove-book<br/>
Request Type: POST<br/>
Purpose: Remove a book from a specific list.<br/>
Request Body:<br/>
"book_id": "string",<br/>
"list_type": "string" (Optional, defaults to 'reading_list')<br/>

Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "message": "Book removed from {list_type}" }<br/>

Example Request: POST /api/remove-book<br/>
Example Response:<br/>
"status": "success"<br/>
"message": "Book removed from reading list"<br/>

**Get Reading List**<br/>
Route: /api/get-reading-list<br/>
Request Type: GET<br/>
Purpose: Get all books in the reading list.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "books": [book_list] }<br/>

Example Request: GET /api/get-reading-list<br/>
Example Response:<br/>
"status": "success"<br/>
"books": [book_list]<br/>

**Get Current Reads**<br/>
Route: /api/get-current-reads<br/>
Request Type: GET<br/>
Purpose: Get all books currently being read.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "books": [book_list] }<br/>

Example Request: GET /api/get-current-reads<br/>
Example Response:<br/>
"status": "success"<br/>
"books": [book_list]<br/>

**Get Completed Books**<br/>
Route: /api/get-completed-books<br/>
Request Type: GET<br/>
Purpose: Get all completed books.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "books": [book_list] }<br/>

Example Request: GET /api/get-completed-books<br/>
Example Response:<br/>
"status": "success"<br/>
"books": [book_list]<br/>

**Get Recommendations**<br/>
Route: /api/get-recommendations<br/>
Request Type: GET<br/>
Purpose: Get book recommendations based on completed books.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "recommendations": [book_list] }<br/>

Example Request: GET /api/get-recommendations<br/>
Example Response:<br/>
"status": "success"<br/>
"recommendations": [book_list]<br/>

**Reset Users**<br/>
Route: /api/reset-users<br/>
Request Type: DELETE<br/>
Purpose: Recreate the users table to delete all users.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "message": "Users table recreated successfully" }<br/>

Example Request: DELETE /api/reset-users<br/>
Example Response:<br/>
"status": "success"<br/>
"message": "Users table recreated successfully"<br/>

**Reset Books**<br/>
Route: /api/reset-books<br/>
Request Type: DELETE<br/>
Purpose: Recreate the books table to delete all books.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "message": "Books table recreated successfully" }<br/>

Example Request: DELETE /api/reset-books<br/>
Example Response:<br/>
"status": "success"<br/>
"message": "Books table recreated successfully"<br/>

**Clear Shelf**<br/>
Route: /api/clear-shelf<br/>
Request Type: POST<br/>
Purpose: Clear all lists in the shelf.<br/>
Response Format: JSON<br/>
Success Response Example:<br/>
Code: 200<br/>
Content: { "status": "success", "message": "Shelf cleared successfully" }<br/>

Example Request: POST /api/clear-shelf<br/>
Example Response:<br/>
"status": "success"<br/>
"message": "Shelf cleared successfully"<br/>

  
