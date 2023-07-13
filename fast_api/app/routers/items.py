from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Body, Depends, Path, Query

from fast_api.app.dependencies import get_token_header
from fast_api.app.models.item import Item

router = APIRouter()

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
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
