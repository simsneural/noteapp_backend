
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db
from .jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/signup', response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    created = crud.create_user(db, user)
    return created

from fastapi.security import OAuth2PasswordRequestForm
from .hashing import verify_password

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    token = create_access_token({"user_id": str(user.id), "role": user.role, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}
