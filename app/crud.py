
from sqlalchemy.orm import Session
from . import models, schemas
from .auth.hashing import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role or "user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_note(db: Session, user_id, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, description=note.description, user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_note(db: Session, note_id):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def get_notes_for_user(db: Session, user_id):
    return db.query(models.Note).filter(models.Note.user_id == user_id).order_by(models.Note.title).all()

def get_all_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.title).all()

def update_note(db: Session, note_obj, title: str, description: str):
    note_obj.title = title
    note_obj.description = description
    db.commit()
    db.refresh(note_obj)
    return note_obj

def delete_note(db: Session, note_obj):
    db.delete(note_obj)
    db.commit()
    return True
