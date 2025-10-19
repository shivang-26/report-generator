from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import PlainValidator
from typing import List, Optional, Dict, Any, Annotated
from datetime import datetime
from bson import ObjectId

def validate_objectid(v):
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return str(v)

PyObjectId = Annotated[str, PlainValidator(validate_objectid)]

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
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Sample Report",
                "authors": ["Author One", "Author Two"],
                "template": "ieee"
            }
        }
    )

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    disabled: bool = False

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    hashed_password: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "disabled": False,
                "hashed_password": "hashedpassword123"
            }
        }
    )
