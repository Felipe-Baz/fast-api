from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "api-token":
        raise HTTPException(status_code=400, detail="No api token provided")

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}