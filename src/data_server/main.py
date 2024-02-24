from fastapi import FastAPI
from src.data_server.api.dependencies.implementations import Impl
from src.data_server.api.routers.contacts_router import ContactsRouter
from src.data_server.api.routers.messages_router import MessagesRouter
from src.data_server.api.routers.photos_router import PhotosRouter
from src.data_server.api.routers.users_router import UserRouter

app = FastAPI()


@app.get("/health")
def healthCheack():
    return {"running": True}


implementations = Impl()

user_router = UserRouter(
    implementations.user_db,
    implementations.user_cache,
    implementations.contacts_db,
    implementations.auth_service,
)
app.include_router(user_router.create_router())

photos_router = PhotosRouter(
    implementations.auth_service,
    implementations.user_db,
    implementations.message_db,
    implementations.storage,
)
app.include_router(photos_router.create_router())

messages_router = MessagesRouter(
    implementations.auth_service,
    implementations.message_db,
    implementations.message_queue,
    implementations.user_db,
    implementations.contacts_db,
)
app.include_router(messages_router.create_router())

contacts_router = ContactsRouter(
    implementations.contacts_db, implementations.auth_service
)
app.include_router(contacts_router.create_router())
