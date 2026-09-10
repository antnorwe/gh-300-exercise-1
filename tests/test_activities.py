def test_get_activities_returns_activity_details(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activity = response.json()[expected_activity]
    assert activity["description"]
    assert activity["schedule"]
    assert activity["max_participants"] == 12
    assert isinstance(activity["participants"], list)


def test_root_redirects_to_static_app(client):
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"