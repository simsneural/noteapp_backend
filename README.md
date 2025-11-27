
# Backend (FastAPI)

- Copy `.env.example` to `.env` and set DATABASE_URL and SECRET_KEY.
- Install dependencies: `pip install -r requirements.txt`
- Create DB (Postgres) as in DATABASE_URL
- Run: `uvicorn app.main:app --reload --port 8000`
- API docs: http://localhost:8000/docs
