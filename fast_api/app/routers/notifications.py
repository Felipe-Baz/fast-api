from typing import Annotated
from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from fast_api.app.background_tasks import get_query, write_log

from fast_api.app.dependencies import get_token_header

router = APIRouter()

router = APIRouter(
    prefix="/notification",
    tags=["notifications"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/send/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}