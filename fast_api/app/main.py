import time
from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Cookie, Depends
from fast_api.app.dependencies import common_parameters, get_query_token, get_token_header
from fast_api.app.internal import admin
from fast_api.app.routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.get("/cookies")
def cookieGet(ads_id: Annotated[str | None, Cookie()] = None):
    return {"cookies": ads_id}

@app.get("/commons")
def request_with_commons_parameters(commons: Annotated[dict, Depends(common_parameters)]):
    return commons