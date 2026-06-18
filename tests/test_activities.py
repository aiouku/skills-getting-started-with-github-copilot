from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic smoke checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_and_duplicate(client):
    activity = "Soccer Club"
    email = "tester@example.com"

    # Ensure email not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json().get(activity, {}).get("participants", [])

    # Signup should succeed
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Signup again should fail with 400
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up for this activity"


def test_signup_capacity(client):
    # Create a temporary activity with capacity 1
    activity = "Temp Capacity Test"
    app = client.app
    # inject activity directly
    app_module = __import__("src.app", fromlist=["activities"]) 
    app_module.activities[activity] = {
        "description": "Temporary capacity test",
        "schedule": "Now",
        "max_participants": 1,
        "participants": []
    }

    # first signup OK
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": "a@example.com"})
    assert r1.status_code == 200

    # second signup should be rejected (activity full)
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": "b@example.com"})
    assert r2.status_code == 400
    assert r2.json().get("detail") == "Activity is full"


def test_remove_participant(client):
    activity = "Programming Class"
    email = "delete_me@example.com"

    # add participant
    r_add = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r_add.status_code == 200

    # ensure present
    r_get = client.get("/activities")
    assert email in r_get.json()[activity]["participants"]

    # remove participant
    r_del = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r_del.status_code == 200
    assert "Removed" in r_del.json().get("message", "")

    # verify removed
    r_get2 = client.get("/activities")
    assert email not in r_get2.json()[activity]["participants"]
