from fastapi import FastAPI, Depends
from app import crud, models, schemas
from app.database import SessionLocal,engine
from sqlalchemy.orm import Session



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create_post/')
def create_post(title,body,db:Session = Depends(get_db)):
    return crud.create_post(db, title,body)


@app.get('/posts/')
def postlist(db:Session = Depends(get_db)):
    return crud.post_list(db)


@app.get('/post/')
def get_post(id,db:Session = Depends(get_db)):
    return crud.get_post(db,id)


@app.put('/post/{id}')
def post_update(id:int,request: schemas.Post,db:Session = Depends(get_db)):
    return crud.post_update(id, request,db)

@app.delete('/post/{id}')
def destroy(id,db:Session = Depends(get_db)):
    return crud.destroy(id,db)