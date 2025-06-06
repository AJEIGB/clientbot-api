from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the .env file")

# Set up database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

# Create the table
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    content: str = Field(..., min_length=1, max_length=500)

class MessageResponse(BaseModel):
    status: str
    id: int

class MessageOut(BaseModel):
    id: int
    name: str
    content: str

    class Config:
        orm_mode = True

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + MySQL!"}

# Endpoint to send message
@app.post("/send", response_model=MessageResponse)
def send_message(msg: Message, db: Session = Depends(get_db)):
    try:
        new_msg = MessageDB(name=msg.name, content=msg.content)
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return {"status": "stored", "id": new_msg.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all messages
@app.get("/messages", response_model=List[MessageOut])
def get_messages(db: Session = Depends(get_db)):
    return db.query(MessageDB).all()
