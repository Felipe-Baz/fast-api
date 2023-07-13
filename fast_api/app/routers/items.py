from typing import Annotated, Union
from fastapi import APIRouter
from fastapi.params import Body, Depends, Path, Query
from pydantic import BaseModel, Field

from fast_api.app.dependencies import get_token_header

router = APIRouter()

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

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

@router.get("/{item_id}")
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


@router.put("/{item_id}")
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
