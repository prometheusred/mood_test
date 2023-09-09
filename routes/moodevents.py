from typing import List
import logging

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from auth.authenticate import authenticate
from database.connection import Database
from models.moodevents import MoodEvent, MoodEventUpdate
from thirdparty.pretendlocations import close_locations


moodevent_router = APIRouter(
    tags=["MoodEvents"]
)

moodevent_database = Database(MoodEvent)


@moodevent_router.get("/", response_model=List[MoodEvent])
async def retrieve_all_events(user = Depends(authenticate)) -> List[MoodEvent]:
    events = await moodevent_database.get_all({"creator": user})
    return events


@moodevent_router.get("/dist")
async def retrieve_event_dist(user = Depends(authenticate)) -> dict:
    events = await moodevent_database.get_all({"creator": user})
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No MoodEvents for User"
        )
    mood_counts = {}
    for e in events:
        mood_counts[e.mood_type] = mood_counts.get(e.mood_type, 0) + 1
    return {"distribution": mood_counts}

@moodevent_router.get("/happy")
async def retrieve_event_dist(user = Depends(authenticate)) -> dict:
    events = await moodevent_database.get_all({"creator": user, "mood_type": 'happy'})
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No MoodEvents for User"
        )
    locations = []
    proximity_radius = 10
    for e in events:
        locations.extend(close_locations(proximity_radius, e.lat, e.lon))
    return {"locations": locations}


@moodevent_router.post("/new")
async def create_event(body: MoodEvent, user = Depends(authenticate)) -> dict:
    body.creator = user
    await moodevent_database.save(body)
    return {
        "message": "MoodEvent created successfully"
    }


@moodevent_router.put("/{id}", response_model=MoodEvent)
async def update_event(id: PydanticObjectId, body: MoodEventUpdate, user: str = Depends(authenticate)) -> MoodEvent:
    event = await moodevent_database.get(id)
    if event.creator != user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    updated_event = await moodevent_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MoodEvent with supplied ID does not exist"
        )
    return updated_event


@moodevent_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await moodevent_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MoodEvent with supplied ID does not exist"
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    event = await moodevent_database.delete(id)

    return {
        "message": "MoodEvent deleted successfully."
    }