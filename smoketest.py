import requests


def run_smoketest():
    base_url = "http://localhost:5004/api"
    username = "test_user"
    password = "test_password"

    # Test book ID (Harry Potter)
    test_book_id = "wrOQLV6xB-wC"

    # 1. Health check
    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "success"
    print("Health check successful")

    # 2. Reset database tables
    delete_user_response = requests.delete(f"{base_url}/reset-users")
    assert delete_user_response.status_code == 200
    assert delete_user_response.json()["status"] == "success"
    print("Reset users successful")

    delete_books_response = requests.delete(f"{base_url}/reset-books")
    assert delete_books_response.status_code == 200
    assert delete_books_response.json()["status"] == "success"
    print("Reset books successful")

    # 3. Create user
    create_user_response = requests.put(f"{base_url}/create-account", json={
        "username": username,
        "password": password
    })
    assert create_user_response.status_code == 201
    assert create_user_response.json()["status"] == "success"
    print("User creation successful")

    # Create session for authenticated requests
    session = requests.Session()

    # 4. Log in
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login successful")

    # 5. Search for books
    search_resp = session.get(f"{base_url}/search-books?query=harry+potter&max_results=5")
    assert search_resp.status_code == 200
    assert search_resp.json()["status"] == "success"
    assert len(search_resp.json()["books"]) > 0
    print("Book search successful")

    # 6. Add book to reading list
    add_book_resp = session.post(f"{base_url}/add-to-reading-list", json={
        "book_id": test_book_id
    })
    assert add_book_resp.status_code == 200
    assert add_book_resp.json()["status"] == "success"
    print("Add to reading list successful")

    # 7. Get reading list
    get_list_resp = session.get(f"{base_url}/get-reading-list")
    assert get_list_resp.status_code == 200
    assert get_list_resp.json()["status"] == "success"
    assert len(get_list_resp.json()["books"]) == 1
    print("Get reading list successful")

    # 8. Start reading
    start_reading_resp = session.post(f"{base_url}/start-reading", json={
        "book_id": test_book_id
    })
    assert start_reading_resp.status_code == 200
    assert start_reading_resp.json()["status"] == "success"
    print("Start reading successful")

    # 9. Get current reads
    current_reads_resp = session.get(f"{base_url}/get-current-reads")
    assert current_reads_resp.status_code == 200
    assert current_reads_resp.json()["status"] == "success"
    assert len(current_reads_resp.json()["books"]) == 1
    print("Get current reads successful")

    # 10. Mark as read
    mark_read_resp = session.post(f"{base_url}/mark-as-read", json={
        "book_id": test_book_id
    })
    assert mark_read_resp.status_code == 200
    assert mark_read_resp.json()["status"] == "success"
    print("Mark as read successful")

    # 11. Get completed books
    completed_books_resp = session.get(f"{base_url}/get-completed-books")
    assert completed_books_resp.status_code == 200
    assert completed_books_resp.json()["status"] == "success"
    assert len(completed_books_resp.json()["books"]) == 1
    print("Get completed books successful")

    # 12. Get recommendations
    recommendations_resp = session.get(f"{base_url}/get-recommendations")
    assert recommendations_resp.status_code == 200
    assert recommendations_resp.json()["status"] == "success"
    print("Get recommendations successful")

    # 13. Change password
    change_password_resp = session.post(f"{base_url}/change-password", json={
        "new_password": "new_password"
    })
    assert change_password_resp.status_code == 200
    assert change_password_resp.json()["status"] == "success"
    print("Password change successful")

    # 14. Log out
    logout_resp = session.post(f"{base_url}/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "success"
    print("Logout successful")

    # 15. Verify authentication is required (should fail)
    add_book_logged_out_resp = session.post(f"{base_url}/add-to-reading-list", json={
        "book_id": test_book_id
    })
    assert add_book_logged_out_resp.status_code == 401
    assert add_book_logged_out_resp.json()["status"] == "error"
    print("Authentication check successful")

    print("\nAll smoke tests passed!")


if __name__ == "__main__":
    run_smoketest()