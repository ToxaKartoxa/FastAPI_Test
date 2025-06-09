from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    name: str
    description: str | None = None

class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class STaskID(BaseModel):
    ok: bool = True
    task_id: int

###########################################################

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
