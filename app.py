from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import ProductionConfig

from book_discovery.db import db
from book_discovery.models.books_model import Books
from book_discovery.models.shelf_model import ShelfModel
from book_discovery.models.user_model import Users
from book_discovery.utils.logger import configure_logger
from book_discovery.utils.api_utils import search_books, get_book_details

load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    configure_logger(app.logger)

    app.config.from_object(config_class)

    db.init_app(app)  
    with app.app_context():
        db.create_all()  

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)

    # Initialize our in-memory shelf model
    shelf_model = ShelfModel()

    # HEALTH CHECK ROUTE
    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """Health check route to verify the service is running."""
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)

    # USER MANAGEMENT ROUTES
    @app.route('/api/create-account', methods=['PUT'])
    def create_user() -> Response:
        """Register a new user account."""
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """Authenticate a user and log them in."""
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        """Log out the current user."""
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        """Change the password for the current user."""
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    # BOOK SEARCH ROUTE (API INTEGRATION)
    @app.route('/api/search-books', methods=['GET'])
    @login_required
    def search_books_route() -> Response:
        """Search for books using Google Books API."""
        try:
            query = request.args.get('query', '')
            max_results = request.args.get('max_results', 10, type=int)
            
            if not query:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Search query is required"
                }), 400)
            
            app.logger.info(f"Searching for books with query: {query}")
            results = search_books(query, max_results)
            
            return make_response(jsonify({
                "status": "success",
                "books": results
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Book search failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred during book search: {str(e)}"
            }), 500)
    
    @app.route('/api/book-details/<string:book_id>', methods=['GET'])
    @login_required
    def get_book_details_route(book_id: str) -> Response:
        """Get detailed information about a specific book."""
        try:
            app.logger.info(f"Getting book details for ID: {book_id}")
            book = get_book_details(book_id)
            
            return make_response(jsonify({
                "status": "success",
                "book": book
            }), 200)
            
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 404)
        except Exception as e:
            app.logger.error(f"Getting book details failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred while retrieving book details: {str(e)}"
            }), 500)
    
    # BOOKSHELF MANAGEMENT ROUTES (IN-MEMORY MODEL)
    @app.route('/api/add-to-reading-list', methods=['POST'])
    @login_required
    def add_to_reading_list() -> Response:
        """Add a book to the reading list."""
        try:
            data = request.get_json()
            book_id = data.get('book_id')
            
            if not book_id:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Book ID is required"
                }), 400)
            
            shelf_model.add_to_reading_list(book_id)
            
            return make_response(jsonify({
                "status": "success",
                "message": "Book added to reading list"
            }), 200)
            
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to add book to reading list: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/start-reading', methods=['POST'])
    @login_required
    def start_reading() -> Response:
        """Move a book from reading list to currently reading."""
        try:
            data = request.get_json()
            book_id = data.get('book_id')
            
            if not book_id:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Book ID is required"
                }), 400)
            
            shelf_model.add_to_current_reads(book_id)
            
            return make_response(jsonify({
                "status": "success",
                "message": "Book moved to currently reading"
            }), 200)
            
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to start reading book: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/mark-as-read', methods=['POST'])
    @login_required
    def mark_as_read() -> Response:
        """Mark a book as completed."""
        try:
            data = request.get_json()
            book_id = data.get('book_id')
            
            if not book_id:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Book ID is required"
                }), 400)
            
            shelf_model.mark_as_read(book_id)
            
            return make_response(jsonify({
                "status": "success",
                "message": "Book marked as read"
            }), 200)
            
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to mark book as read: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/remove-book', methods=['POST'])
    @login_required
    def remove_book() -> Response:
        """Remove a book from a specific list."""
        try:
            data = request.get_json()
            book_id = data.get('book_id')
            list_type = data.get('list_type', 'reading_list')
            
            if not book_id:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Book ID is required"
                }), 400)
            
            shelf_model.remove_book(book_id, list_type)
            
            return make_response(jsonify({
                "status": "success",
                "message": f"Book removed from {list_type}"
            }), 200)
            
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to remove book: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/get-reading-list', methods=['GET'])
    @login_required
    def get_reading_list() -> Response:
        """Get all books in the reading list."""
        try:
            books = shelf_model.get_reading_list()
            
            return make_response(jsonify({
                "status": "success",
                "books": books
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Failed to get reading list: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/get-current-reads', methods=['GET'])
    @login_required
    def get_current_reads() -> Response:
        """Get all books currently being read."""
        try:
            books = shelf_model.get_current_reads()
            
            return make_response(jsonify({
                "status": "success",
                "books": books
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Failed to get current reads: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/get-completed-books', methods=['GET'])
    @login_required
    def get_completed_books() -> Response:
        """Get all completed books."""
        try:
            books = shelf_model.get_completed_books()
            
            return make_response(jsonify({
                "status": "success",
                "books": books
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Failed to get completed books: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    @app.route('/api/get-recommendations', methods=['GET'])
    @login_required
    def get_recommendations() -> Response:
        """Get book recommendations based on completed books."""
        try:
            recommendations = shelf_model.get_book_recommendations()
            
            return make_response(jsonify({
                "status": "success",
                "recommendations": recommendations
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Failed to get recommendations: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    # Database management routes
    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        """Recreate the users table to delete all users."""
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": "Users table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Users table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while resetting users",
                "details": str(e)
            }), 500)
    
    @app.route('/api/reset-books', methods=['DELETE'])
    def reset_books() -> Response:
        """Recreate the books table to delete all books."""
        try:
            app.logger.info("Received request to recreate Books table")
            with app.app_context():
                Books.__table__.drop(db.engine)
                Books.__table__.create(db.engine)
            app.logger.info("Books table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": "Books table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Books table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while resetting books",
                "details": str(e)
            }), 500)
    
    @app.route('/api/clear-shelf', methods=['POST'])
    @login_required
    def clear_shelf() -> Response:
        """Clear all lists in the shelf."""
        try:
            shelf_model.reading_list.clear()
            shelf_model.current_reads.clear()
            shelf_model.completed.clear()
            shelf_model.clear_cache()
            
            return make_response(jsonify({
                "status": "success",
                "message": "Shelf cleared successfully"
            }), 200)
            
        except Exception as e:
            app.logger.error(f"Failed to clear shelf: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }), 500)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5004)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")