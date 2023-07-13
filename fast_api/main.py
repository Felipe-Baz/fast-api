from typing import Annotated, Union

from fastapi import FastAPI
from fastapi.params import Body, Path, Query
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
