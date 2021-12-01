from sqlalchemy.orm import Session

from app import models,schemas


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
