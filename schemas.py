from pydantic import BaseModel, EmailStr
class UserProfileCreate:
    email: EmailStr
    username: str
