from fastapi import FastAPI
from api import *

app = FastAPI()


@app.get("/health")
def healthCheack():
    return {"status": "running"}


user_router = UserRouter("auth_service", "data_service")
app.include_router(user_router.router)

photos_router = PhotosRouter("auth_service", "data_service")
app.include_router(photos_router.router)

messages_router = MessagesRouter("auth_service", "data_service")
app.include_router(messages_router.router)
