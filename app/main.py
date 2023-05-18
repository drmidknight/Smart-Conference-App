import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.routes.api import router as api_router
from fastapi_jwt_auth import AuthJWT
from app.schemas.schemas import Settings
from inspect import re
from fastapi.openapi.utils import get_openapi


app = FastAPI()

#origins = ["http://localhost:4300", "http://localhost:4200"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)



@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)
    print("running")