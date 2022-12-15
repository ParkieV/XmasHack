from fastapi import APIRouter, Request, Response


userRouter = APIRouter(prefix="/docs")


@userRouter.get("/upload")
async def upload_view(request: Request, detail: str = None):
    pass

@userRouter.post("/upload", status_code=204, response_class=Response)
async def upload_view():
    pass