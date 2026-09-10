def test_student_can_signup_once_and_then_unregister(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-check@example.com"

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregistering_missing_student_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing-student@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"


def test_unregistering_from_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
