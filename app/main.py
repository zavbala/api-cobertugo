from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import router


app = FastAPI()

def create_app():

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["GET"],
        allow_credentials=True,
    )

    app.include_router(router)

    return app

app = create_app()