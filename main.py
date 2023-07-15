from base_service import BaseService
from schemas import UserProfileCreate
from models.user_profile import UserProfile, UserProfile_Pydantic
from tortoise import Tortoise, run_async

user_service = BaseService("user", "amqp://guest:guest@192.168.1.28")

@user_service.event("user.create")
async def on_user_create(data) -> dict:
    if (await UserProfile.exists(email=data["email"])) or (
        await UserProfile.exists(username=data["username"])
    ):
        return {"error": "already exists"}
    prof = await UserProfile.create(**data)
    return {
        "id": str(prof.id),
        "username": prof.username,
        "email": prof.email,
        "createdAt": prof.created_at.timestamp(),
        "updatedAt": prof.updated_at.timestamp(),
    }

@user_service.event("user.find.id")
async def on_user_find_id(data: dict) -> dict:
    user = await UserProfile.get(id=data["id"])
    if not user:
        return {}
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "createdAt": user.created_at.timestamp(),
        "updatedAt": user.updated_at.timestamp(),
    }

@user_service.event("user.find")
async def on_user_find(data) -> dict:
    user = await UserProfile.get(username=data["login"]) or await UserProfile.get(
        email=data["login"]
    )
    if not user:
        return {}
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "createdAt": user.created_at.timestamp(),
        "updatedAt": user.updated_at.timestamp(),
    }


async def init():
    user_service.logger.debug("connecting to database")
    await Tortoise.init(
        db_url="postgres://miauw_user:miauw_password@192.168.1.28:5432/miauw",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    user_service.logger.debug("generating schemas")


if __name__ == "__main__":
    run_async(init())
    user_service.start()
