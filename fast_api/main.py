from typing import Annotated, Union

from fastapi import FastAPI
from fastapi.params import Path, Query
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
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
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}
