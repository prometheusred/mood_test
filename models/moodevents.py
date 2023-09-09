from typing import Optional, List

from beanie import Document
from pydantic import BaseModel


class MoodEvent(Document):
    creator: Optional[str]
    mood_type: str
    timestamp: str
    lat: float
    lon: float

    class Config:
        schema_extra = {
            "example": {
                "mood_type": "happy",
                "timestamp": "2008-09-15T15:53:00+05:00",
                "lat": 88.0,
                "lon": 70.2
            }
        }

    class Settings:
        name = "moodevents"


class MoodEventUpdate(BaseModel):
    mood_type: Optional[str]
    timestamp: Optional[str]
    lat: Optional[float]
    lon: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "mood_type": "happy",
                "timestamp": "2008-09-15T15:53:00+05:00",
                "lat": 88.0,
                "lon": 70.2
            }
        }