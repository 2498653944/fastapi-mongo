from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from auth.jwt_handler import signJWT
from database.database import get_playerinfo, get_player_hero_relationship
from models.playerInfo import PlyaerInfoModel, ResponseModel, ErrorResponseModel

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

import datetime


class PositionName(str, Enum):
    TOP = "TOP"
    JUN = "JUN"
    MID = "MID"
    BOT = "BOT"
    SUP = "SUP"
    ALL = "ALL"


class Item(BaseModel):
    time_range: Optional[List[str]] = [datetime.datetime(2021, 1, 1, 0, 0, 1).isoformat(),
                                       datetime.datetime.now().isoformat()]
    season_name: Optional[str] = ""
    match_id: Optional[List[int]] = []
    players: Optional[List[str]] = []


@router.post("/player/", response_description="player_battle_data")
async def get_player_data(data: Item):
    student = await get_playerinfo(data)
    return ResponseModel(student, "data retrieved successfully") \
        if student \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")


@router.get("/hero/{position}", response_description="选手英雄池")
async def get_hero_pool(
        start_time: Optional[str] = datetime.datetime(2021, 1, 1, 0, 0, 1).isoformat(),
        end_time: Optional[str] = datetime.datetime.now().isoformat(),
        season_name: Optional[str] = "2022LPL春季赛季后赛",
        position: Optional[PositionName] = None):
    data = await get_player_hero_relationship(position, season_name, start_time, end_time)
    return ResponseModel(data, "data retrieved successfully") \
        if data \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")
