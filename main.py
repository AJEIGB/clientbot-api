from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    content: str = Field(..., min_length=1, max_length=500)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + MySQL!"}

@app.post("/send")
def send_message(msg: Message):
    db = SessionLocal()
    try:
        new_msg = MessageDB(name=msg.name, content=msg.content)
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return {"status": "stored", "id": new_msg.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
