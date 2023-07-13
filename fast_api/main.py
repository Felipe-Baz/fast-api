import time
from typing import Annotated, Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body, Cookie, Depends, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(
        title="The name of the item", max_length=300
    )
    price: float = Field(
        title="The price of the item", gt=0
    )
    is_offer: Union[bool, None] = Field(
        default=False, title="The price of the item", gt=0
    )

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

@app.get("/")
def read_root():
    time.sleep(1)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(
    item_id: Annotated[
        int, 
        Path(title="The ID of the item to get", ge=0, le=10)
    ],
    q: Annotated[
        str | None, 
        Query(min_length=3, max_length=15)
    ] = None
):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(
    item_id: Annotated[
        int, 
        Path(title="The ID of the item to get", ge=0, le=10)
    ],
    item: Annotated[
        Item, 
        Body(
            examples=[
                {
                    "name": "Foo",
                    "price": 35.4
                },
                {
                    "name": "Bar",
                    "price": "35.4"
                },
                {
                    "name": "Bar",
                    "price": 35.4,
                    "is_offer": True
                },
            ],
        )
    ]
):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}

@app.get("/cookies")
def cookieGet(ads_id: Annotated[str | None, Cookie()] = None):
    return {"cookies": ads_id}

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/commons")
def request_with_commons_parameters(commons: Annotated[dict, Depends(common_parameters)]):
    return commons