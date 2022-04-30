import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .database_helper import student_helper, admin_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.lpldata

student_collection = database.get_collection('students_collection')
admin_collection = database.get_collection('admins')
lpldata_collection = database.get_collection('MatchData')


async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)


async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_student_data(id: str, data: dict):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        student_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


async def get_playerinfo(name: str,
                         players: list,
                         timerange=['020-01-30T00:00:00.000Z', '2022-08-23T00:00:00.000Z']):
    """:arg
        list[ISOtimeString]
    """
    query = [
        {"$match": {
            "data.matchTime": {"$gte": timerange[0],
                               "$lt": timerange[1]}
        }
        },
        {"$match": {"data.seasonName": "2022LPL春季赛季后赛"}},
        #       {"$match": {"data.matchInfos.matchWin": 29}},
        {"$unwind": "$data.matchInfos"},
        {"$unwind": "$data.matchInfos.teamInfos"},
        {"$unwind": "$data.matchInfos.teamInfos.playerInfos"},
        {"$match": {"data.matchInfos.teamInfos.playerInfos.playerName": {"$in": players}}},
        #      {"$group": {"_id": "$data.matchInfos.teamInfos.playerInfos.playerName",
        #                  "avgKill": {"$avg": "$data.matchInfos.teamInfos.playerInfos.battleDetail.kills"}}},
        {"$group": {"_id": "$data.matchInfos.teamInfos.playerInfos.playerName",
                    "battleDetail": {"$push": "$data.matchInfos.teamInfos.playerInfos.battleDetail"}},
         "data": {"$push": "$data.matchInfos.teamInfos.playerInfos"},
         },
        {"$sort": {"avgKill": -1}}]
    data_info = await lpldata_collection.aggregate(query).to_list(length=None)
    return data_info


async def get_player_hero_relationship(position: str):
    query = [
        {"$match": {"data.seasonName": "2022LPL春季赛季后赛"}},
        {"$unwind": "$data.matchInfos"},
        {"$unwind": "$data.matchInfos.teamInfos"},
        {"$unwind": "$data.matchInfos.teamInfos.playerInfos"},
        {"$group": {"_id": "$data.matchInfos.teamInfos.playerInfos.playerLocation",
                    "hero": {"$push": {"playerName": "$data.matchInfos.teamInfos.playerInfos.playerName",
                                       "heroName": "$data.matchInfos.teamInfos.playerInfos.heroName"}}
                    }}
    ]
    given_position = {"$match":{"$_id":position}}
    if position:
        query.append(given_position)
    data = await lpldata_collection.aggregate(query).to_list(length=None)
    return data


