import pytest


def test_root_redirect(client):
    # Arrange: client fixture
    # Act
    response = client.get("/", allow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_known_activity(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert activity_name in data


def test_post_signup_happy_path_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "test_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert new_email in participants


def test_post_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400


def test_delete_removal_happy_path_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email_to_remove})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email_to_remove not in participants


def test_delete_removal_of_nonexistent_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    non_existent_email = "noone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": non_existent_email})

    # Assert
    assert response.status_code == 400


def test_missing_email_param_post_returns_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_missing_email_param_delete_returns_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
