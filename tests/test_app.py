import sys
from pathlib import Path

# Ensure `src` is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient
import pytest

from app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister():
    email = "tester@example.com"
    activity = "Basketball"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    before = len(activities[activity]["participants"])

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    r2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r2.status_code == 200
    assert email not in activities[activity]["participants"]

    after = len(activities[activity]["participants"])
    assert before == after


def test_unregister_nonexistent():
    email = "noone@example.com"
    activity = "Basketball"

    # Ensure email not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    r = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r.status_code == 404
