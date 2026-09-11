from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.database import engine, Base
from app import models
from app.routes import jobs_router, user_router, application_router


app = FastAPI()

app.include_router(jobs_router)
app.include_router(user_router)
app.include_router(application_router)

app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

Base.metadata.create_all(bind=engine)