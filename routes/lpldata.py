from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from auth.jwt_handler import signJWT
from database.database import get_playerinfo, get_player_hero_relationship
from models.playerInfo import PlyaerInfoModel, ResponseModel, ErrorResponseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/{id}", response_description="player_battle_data")
async def get_player_data(id: str, data: dict):
    print(data)
    players = data.get("players")
    print(players)
    student = await get_playerinfo(id, players)
    return ResponseModel(student, "data retrieved successfully") \
        if student \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")


@router.get("/{position}", response_description="选手英雄池")
async def get_hero_pool(position: str):
    print(position)
    data = await get_player_hero_relationship(position)
    return ResponseModel(data, "data retrieved successfully") \
        if data \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")
