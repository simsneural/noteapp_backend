
from fastapi import FastAPI
from . import models
from .database import engine
from .auth import routes as auth_routes
from .notes import routes as notes_routes
from .users import routes as users_routes
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*", 
    ]
app = FastAPI(title='Notes App API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],    
)

app.include_router(auth_routes.router)
app.include_router(notes_routes.router)
app.include_router(users_routes.router)

@app.get('/')
def root():
    return {'msg': 'Notes API'}

@app.on_event('startup')
def startup_event():
    models.Base.metadata.create_all(bind=engine)
