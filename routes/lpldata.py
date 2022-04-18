from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from auth.jwt_handler import signJWT
from database.database import get_playerinfo
from models.playerInfo import PlyaerInfoModel, ResponseModel, ErrorResponseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/{id}", response_description="Student data retrieved")
async def get_player_data(id:str,data:dict):
    print(data)
    players = data.get("players")
    print(players)
    student = await get_playerinfo(id,players)
    return ResponseModel(student, "data retrieved successfully") \
        if student \
        else ErrorResponseModel("An error occured.", 404, "data doesn't exist.")
