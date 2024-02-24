from fastapi import FastAPI

from src.live_server.api.dependencies.implementations import Impl
from src.live_server.api.routers.subscribe_router import SubscribeRouter

app = FastAPI()


@app.get("/health")
def healthCheack():
    return {"running": True}


implementations = Impl()

subscribe_router = SubscribeRouter(
    implementations.message_queue,
    implementations.connection_manager,
    implementations.notification_service,
    implementations.subscriptions_db,
    implementations.auth_service,
)

app.include_router(subscribe_router.create_router())
