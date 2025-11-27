
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/')
def list_users(current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
    return db.query(User).all()
