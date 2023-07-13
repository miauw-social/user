from base_service import Service
from schemas import UserProfileCreate
from models.user_profile import UserProfile, UserProfile_Pydantic
from tortoise import Tortoise, run_async

async def on_user_create(data) -> dict:
    if (await UserProfile.exists(email=data["email"])) or (await UserProfile.exists(username=data["username"])):
        return {"error": "already exists"}
    prof = await UserProfile.create(**data)
    return {"id": str(prof.id), "username": prof.username, "email": prof.email}

async def init():
    await Tortoise.init(
        db_url='postgres://miauw_user:miauw_password@192.168.1.28:5432/miauw',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
    user_service = Service("amqp://guest:guest@192.168.1.28")
    user_service.add_event_handler("user.create", on_user_create)
    user_service.start()