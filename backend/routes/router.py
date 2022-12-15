from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates



router = APIRouter(prefix="/api")

router.include_router(userRouter)

@router.get("/upload")
async def upload(request: Request):
    pass