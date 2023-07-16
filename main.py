from base_service import BaseService, ProblemJSON
from schemas import UserProfileCreate
from models.user_profile import UserProfile, UserProfile_Pydantic
from tortoise import Tortoise, run_async

user_service = BaseService("user", "amqp://guest:guest@192.168.1.28")


@user_service.event("user.create")
async def on_user_create(data) -> dict:
    exists = False
    if check_mail(data.get("email")):
        exists = await UserProfile.exists(email=data["email"])
    else:
        exists = await UserProfile.exists(username=data["username"])
    if exists:
        return ProblemJSON.build(
            "https://user.miauw.social/user/exists/" + "email"
            if check_mail(data.get("email"))
            else "username",
            "User already exists",
            f"""The user with email '{data["email"]}' already exists."""
            if check_mail(data.get("email"))
            else f"""The user with username '{data}' already exists.""",
            409,
            {
                "providedInformation": {
                    "email": data["email"],
                    "username": data["username"],
                }
            },
        )
    prof = await UserProfile.create(**data)
    return {
        "id": str(prof.id),
        "username": prof.username,
        "email": prof.email,
        "createdAt": prof.created_at.timestamp(),
        "updatedAt": prof.updated_at.timestamp(),
    }


@user_service.event("user.find.id")
async def on_user_find_id(id: str) -> dict:
    user = await UserProfile.get(id=data["id"])
    if not user:
        return ProblemJSON.build(
            "https://user.miauw.social/user/not-found",
            "User not found",
            f"""User with id '{data["id"]}' is not found.""",
            404,
            {"providedInformation": {"id": data["id"]}},
        )
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "createdAt": user.created_at.timestamp(),
        "updatedAt": user.updated_at.timestamp(),
    }


@user_service.event("user.find")
async def on_user_find(identifier: str) -> dict:
    user = None
    if check_mail(identifier):
        user = await UserProfile.get(email=identifier)
    else:
        user = await UserProfile.get(username=identifier)
    if not user:
        return ProblemJSON.build(
            "https://user.miauw.social/user/not-found",
            "User not found",
            f"""User with username '{identifier}' is not found."""
            if not check_mail(identifier)
            else f"""User with email '{identifier}' is not found.""",
            404,
            {"providedInformation": {"identifier": identifier}}
        )
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "createdAt": user.created_at.timestamp(),
        "updatedAt": user.updated_at.timestamp(),
    }


async def init():
    user_service.logger.debug("connecting to database")
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
