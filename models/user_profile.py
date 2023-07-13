from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class UserProfile(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(unique=True, max_length=20)
    email = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_profiles"

UserProfile_Pydantic = pydantic_model_creator(UserProfile)