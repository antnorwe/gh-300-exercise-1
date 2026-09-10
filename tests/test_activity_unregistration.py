from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_student_can_signup_once_and_then_unregister():
    activity_name = "Chess Club"
    email = "duplicate-check@example.com"

    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_signup.status_code == 200

    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_signup.status_code == 400

    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
