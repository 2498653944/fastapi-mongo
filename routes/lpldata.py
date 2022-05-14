from collections import Counter

from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from auth.jwt_handler import signJWT
from database.database import get_playerinfo, get_player_hero_relationship
from models.playerInfo import PlyaerInfoModel, HeroDataResponseModel, ErrorResponseModel

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

import datetime

import numpy as np

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
    data = await get_playerinfo(data)
    return HeroDataResponseModel(data,len(data), "data retrieved successfully") \
        if data \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")


@router.get("/hero/", response_description="选手英雄池")
async def get_hero_pool(
        start_time: Optional[str] = datetime.datetime(2021, 1, 1, 0, 0, 1).isoformat(),
        end_time: Optional[str] = datetime.datetime.now().isoformat(),
        season_name: Optional[str] = "2022季中冠军赛小组赛",
        position: Optional[PositionName] = PositionName.ALL):
    data,total = await get_player_hero_relationship(position, season_name, start_time, end_time)

    return HeroDataResponseModel(data,total,"data retrieved successfully") \
        if data \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")
