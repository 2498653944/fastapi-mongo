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


async def get_playerinfo(query_data):
    """:arg
        list[ISOtimeString]
    """
    query = [
        #   {"$match": {"data.matchInfos.matchWin": 29}},
    ]
    time_range = query_data.time_range
    time_condition = {"$match": {
        "data.matchTime": {"$gte": time_range[0],
                           "$lt": time_range[1]}
    }}

    if time_range:
        query.append(time_condition)
    season_name = query_data.season_name
    season_condition = {"$match": {"data.seasonName": season_name}}
    if season_name:
        query.append(season_condition)

    match_id = query_data.match_id
    match_condition = {"$match": {"data.matchId": match_id}}
    if match_id:
        query.append(match_condition)

    unwind_condition = [{"$unwind": "$data.matchInfos"},
                        {"$unwind": "$data.matchInfos.teamInfos"},
                        {"$unwind": "$data.matchInfos.teamInfos.playerInfos"}]
    query.extend(unwind_condition)

    players = query_data.players
    player_condition = {"$match": {"data.matchInfos.teamInfos.playerInfos.playerName": {"$in": players}}}
    if players:
        query.append(player_condition)
    agg_condition = [{"$group": {"_id": "$data.matchInfos.teamInfos.playerInfos.playerName",
                                 "battleDetail": {"$push": "$data.matchInfos.teamInfos.playerInfos.battleDetail"}},
                      "data": {"$push": "$data.matchInfos.teamInfos.playerInfos"},
                      }]
    query.extend(agg_condition)
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
                                       "playerId": "$data.matchInfos.teamInfos.playerInfos.playerId",
                                       "heroName": "$data.matchInfos.teamInfos.playerInfos.heroName",
                                       "heroId": "$data.matchInfos.teamInfos.playerInfos.heroId"
                                       }
                             }
                    }}
    ]
    given_position = {"$match": {"_id": position}}
    query.append(given_position)
    if position == "ALL":
        query.pop()
    data = await lpldata_collection.aggregate(query).to_list(length=None)
    return data
