from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from auth.jwt_handler import signJWT
from database.database import get_playerinfo
from models.playerInfo import PlyaerInfoModel, ResponseModel, ErrorResponseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.get("/v1/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await get_playerinfo(id)
    return ResponseModel(student, "Student data retrieved successfully") \
        if student \
        else ErrorResponseModel("An error occured.", 404, "Student doesn't exist.")
