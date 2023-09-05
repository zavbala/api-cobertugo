from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import router

app = FastAPI()


def create_app():
    app.add_middleware(
        CORSMiddleware,
        allow_headers=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_origins=["http://localhost:3000", "https://cobertugo.vercel.app"],
    )

    app.include_router(router)

    return app


app = create_app()
