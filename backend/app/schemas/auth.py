from pydantic import BaseModel, EmailStr, Field

class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = "EMPLOYEE"

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOutput
