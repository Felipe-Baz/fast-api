from typing import Union
from pydantic import BaseModel, Field


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