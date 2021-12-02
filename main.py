from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app import models,schemas,crud
from app.database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/")
def getuser(db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    if current_user:
        return crud.user_list(db=db)


#Post
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