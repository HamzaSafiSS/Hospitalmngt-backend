# schemas/user.py
from pydantic import BaseModel, EmailStr
from py.models import RoleEnum   # or wherever your enum lives

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    # full_name: str | None = None    ← add other safe fields you want to show
    # created_at: datetime | None = None

    class Config:
        from_attributes = True          # allows conversion from ORM objects (SQLAlchemy 2.0+ style)
        # from_attributes = True         # older Pydantic v1 name: orm_mode = True