from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(unique=True, max_length=20)
    password_hash = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=128)
    # first_name = fields.CharField(max_length=15)
    # last_name = fields.CharField(max_length=15)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    class PydanticMeta:
        exclude = ["password_hash"]



