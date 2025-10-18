from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class ReportBase(BaseModel):
    title: str
    authors: List[str]
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    references: List[Dict[str, Any]] = Field(default_factory=list)
    template: str = "ieee"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: Optional[PyObjectId] = Field(alias='_id')
    
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    disabled: bool = False

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias='_id')
    hashed_password: str
    
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
