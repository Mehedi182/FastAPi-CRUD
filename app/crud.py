from sqlalchemy.orm import Session
from . import models, schemas
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate):
#     db_item = models.Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

SECRET_KEY = "bfcaa24859af5279d4ec6c1de8f9d2624f6d819b020eba2bcd9fe0483af45ed3"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username== username).first()


def user_list(db):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username,hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Post
def create_post(db: Session, title:str, body: str):
    new_post = models.Post(title=title,body=body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_post(db,id:int):
    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
         return f'There is no Blog with id {id}'
    return db.query(models.Post).filter(models.Post.id == id).first()


def post_list(db):
    posts = db.query(models.Post).all()
    if not posts:
        return "There is no Post in the List"
    return db.query(models.Post).all()

def post_update(id:int,request,db):
    db.query(models.Post).filter(models.Post.id == id).update({
        'title':request.title,
        'body': request.body
    })
    db.commit()
    return f'Blog with the id {id} is updated'

def destroy(id,db):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return f"Blog with {id} deleted"