from typing import Optional,List,Dict

from pydantic import BaseModel, EmailStr, Field, AnyHttpUrl


class PlyaerInfoModel(BaseModel):
    playerId: int = Field(...)
    playerName: str = Field(...)
    playerLocation: str = Field(...)
    playerAvatar: str = Field(...)
    heroId: int = Field(...)
    heroName: str = Field(...)
    items: List[Dict] = Field(...)
    minionKilled: int = Field(...)
    perkRunes: List[Dict] = Field(...)
    battleDetail: Dict = Field(...)
    damageDetail: Dict = Field(...)
    DamageTakenDetail: Dict = Field(...)
    otherDetail: Dict = Field(...)
    visionDetail: Dict = Field(...)


    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
