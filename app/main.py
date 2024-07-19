from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .dependencies import get_db

app = FastAPI()

@app.get("/memes/", response_model=List[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes

@app.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    meme = crud.get_meme(db, meme_id=meme_id)
    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme

@app.post("/memes/", response_model=schemas.Meme)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db=db, meme=meme)

@app.put("/memes/{meme_id}", response_model=schemas.Meme)
def update_meme(meme_id: int, meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.update_meme(db=db, meme_id=meme_id, meme=meme)

@app.delete("/memes/{meme_id}", response_model=schemas.Meme)
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    return crud.delete_meme(db=db, meme_id=meme_id)

@app.get("*")
async def read_root():
    return {"message": "Route not found"}

