import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.moodevents import MoodEvent


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@me.com")


@pytest.fixture(scope="module")
async def mock_event() -> MoodEvent:
    new_event = MoodEvent(
        creator="testuser@me.com",
        mood_type="sad",
        timestamp="2008-09-15T15:53:00+05:00",
        lat=33.0,
        lon=10.32
    )

    await MoodEvent.insert_one(new_event)

    yield new_event


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, access_token: str, mock_event: MoodEvent) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = await default_client.get("/moodevents/", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "creator":"testuser@me.com",
        "mood_type": "happy",
        "timestamp": "2008-09-15T15:53:00+05:00",
        "lat": 53.0,
        "lon": 52.2
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "message": "MoodEvent created successfully"
    }

    response = await default_client.post("/moodevents/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient, access_token: str) -> None:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = await default_client.get("/moodevents/", headers=headers)

    events = response.json()

    assert response.status_code == 200
    assert len(events) == 2


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: MoodEvent, access_token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = "/moodevents/dist"
    response = await default_client.get(url, headers=headers)

    assert response.status_code == 200
    dist = response.json()["distribution"]
    assert dist["sad"] == 1
    assert dist["happy"] == 1


@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: MoodEvent, access_token: str) -> None:
    test_payload = {
        "mood_type": "neutral"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/moodevents/{str(mock_event.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["mood_type"] == test_payload["mood_type"]


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: MoodEvent, access_token: str) -> None:
    test_response = {
        "message": "MoodEvent deleted successfully."
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/moodevents/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: MoodEvent, access_token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/moodevents/happy"

    response = await default_client.get(url, headers=headers)

    assert response.status_code == 200
    assert response.json()["locations"][0]['name'] == "HOME"