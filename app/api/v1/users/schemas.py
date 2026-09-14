from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int | None = Field(None, example=1)
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    card_number: str = Field(..., example="1234-5678-9012-3456")
    balance: float = Field(..., example=100.0)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: str | None = Field(None, example="John")
    last_name: str | None = Field(None, example="Doe")
    card_number: str | None = Field(None, example="1234-5678-9012-3456")
    balance: float | None = Field(None, example=100.0)

class UserResponse(UserBase):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True

class UserListResponse(BaseModel):
    users: list[UserResponse] = Field(..., example=[{
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "card_number": "1234-5678-9012-3456",
        "balance": 100.0
    }])



