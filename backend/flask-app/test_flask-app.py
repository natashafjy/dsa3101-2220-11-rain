import backend
import pytest
import sqlite3

@pytest.fixture
def conn():
    #connect to Test sqlite3 database with 1 user and 1 routine added
    # con = sqlite3.connect("rainfall.db")
    con = sqlite3.connect(":memory:")
    #yield cursor connection
    yield con

# def mock_get_user_password(connection, username):
#     exist_user_query = """
#         SELECT *
#         FROM USERS
#         WHERE username = ?
#      """
#     cursor = connection.cursor()
#     cursor.execute(exist_user_query, (username,))
#     user_and_password = cursor.fetchall()
#     cursor.close()
#     return user_and_password


def test_login_page_empty_get(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/login' page is requested (GET) with no parameters
    THEN check that the response is valid but both "exist" 
         and "match" parameters are false
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    with flask_app.test_client() as test_client:
        response = test_client.get("/api/login")
        assert response.status_code == 200
        assert response.json.get("exist") == False
        assert response.json.get("match") == False


def test_login_page_post(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/login' page
    THEN check that the response is 405, method not allowed
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    with flask_app.test_client() as test_client:
        response = test_client.post("/api/login")
        assert response.status_code == 405


def test_login_page_get_existing(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/login' page is requested (GET) with existing username
    THEN check that the response is valid but both "exist" 
         and "match" parameters are false
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [("user1","passw1")])
    with flask_app.test_client() as test_client:
        response = test_client.get("/api/login?username=user1&password=passw1")
        assert response.status_code == 200
        assert response.json.get("exist") == True
        assert response.json.get("match") == True
        response = test_client.get("/api/login?username=user1&password=wrongPW")
        assert response.status_code == 200
        assert response.json.get("exist") == True
        assert response.json.get("match") == False

def test_login_page_get_nonexistent(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/login' page is requested (GET) with nonexistent username
    THEN check that the response is valid but both "exist" 
         and "match" parameters are false
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    with flask_app.test_client() as test_client:
        response = test_client.get("/api/login?username=user2&password=pw1")
        assert response.status_code == 200
        assert response.json.get("exist") == False
        assert response.json.get("match") == False


def test_signup_page_empty_post(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/signup' page with no parameters
    THEN check that the response is valid
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    mocker.patch("backend.add_user_to_db", return_value = None)
    with flask_app.test_client() as test_client:
        response = test_client.post("/api/signup")
        assert response.status_code == 200
        assert response.json.get("exist") == False

def test_signup_page_get(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/signup' page
    THEN check that the response is 405, method not allowed
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    mocker.patch("backend.add_user_to_db", return_value = None)
    with flask_app.test_client() as test_client:
        response = test_client.get("/api/signup")
        assert response.status_code == 405

def test_signup_page_post_nonexistant(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/signup' page with 
         a new "username" and "password"
    THEN check that the response is valid
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [])
    mocker.patch("backend.add_user_to_db", return_value = None)
    with flask_app.test_client() as test_client:
        response = test_client.post("/api/signup?username=user1&password=passw1")
        assert response.status_code == 200
        assert response.json.get("exist") == False

def test_signup_page_post_existing(mocker,conn):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/signup' page 
         with an existing "username" and "password"
    THEN check that the response is valid
    """
    flask_app = backend.app
    mocker.patch("backend.establish_db_connection", return_value = conn)
    mocker.patch("backend.get_user_password", return_value = [("user1","passw1")])
    mocker.patch("backend.add_user_to_db", return_value = None)
    with flask_app.test_client() as test_client:  
        response = test_client.post("/api/signup?username=user1&password=pw123")
        assert response.status_code == 200
        assert response.json.get("exist") == True

