
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post('/', response_model=schemas.NoteOut)
def create(note: schemas.NoteCreate, current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current.get('user_id')
    return crud.create_note(db, user_id, note)

@router.get('/', response_model=list[schemas.NoteOut])
def list_notes(current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    role = current.get('role')
    user_id = current.get('user_id')
    if role == 'admin':
        return crud.get_all_notes(db)
    return crud.get_notes_for_user(db, user_id)

@router.get('/{note_id}', response_model=schemas.NoteOut)
def read_note(note_id: str, current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    if current.get('role') != 'admin' and str(note.user_id) != current.get('user_id'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return note

@router.put('/{note_id}', response_model=schemas.NoteOut)
def update_note(note_id: str, payload: schemas.NoteCreate, current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    if current.get('role') != 'admin' and str(note.user_id) != current.get('user_id'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return crud.update_note(db, note, payload.title, payload.description)

@router.delete('/{note_id}')
def delete_note(note_id: str, current: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    if current.get('role') != 'admin' and str(note.user_id) != current.get('user_id'):
        raise HTTPException(status_code=403, detail='Not authorized')
    crud.delete_note(db, note)
    return {"detail": "deleted"}
