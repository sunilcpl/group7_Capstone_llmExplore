from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String, TIMESTAMP, text, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from fastapi.middleware.cors import CORSMiddleware

# Define DB connection
DATABASE_URL = "postgresql://postgres:Capstone2025$@finagent.cfm8ykkm0s84.ap-south-1.rds.amazonaws.com/postgres"

# SQLAlchemy setup, 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLAlchemy model
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "agent"}  # ✅ schema is specified separately

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    age = Column(Integer)
    designation = Column(String)
    salary = Column(Numeric)

# Pydantic schema
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int
    designation: str
    salary: float
  

# FastAPI app
app = FastAPI()

# Allow frontend (e.g., from file:// or http://localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()
    try:
        new_user = User(
            email=user.email,
            name=user.name,
            age=user.age,
            designation=user.designation,
            salary=user.salary
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

def login():
    #Validate the users
    #If valid 
       #Redirects user to chat
    #else
       #Error message or move user to registration 
    return ""
