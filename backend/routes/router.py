import os
from fastapi import APIRouter, File, UploadFile, Request, Response, HTTPException
from config import DATA_PATH


router = APIRouter(prefix="/api")

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename[filename.rfind('.') + 1:-1]
    if ext not in ["doc", "docx", "rtf", "pdf"]:
        raise HTTPException(400, detail="Invalid document type")
    contents = file.file.read()
    file_path = os.path.join(DATA_PATH, file.filename)
    with open(file_path, 'wb') as f:
        f.write(contents)
    file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}


@router.get("/download")
async def download(response: Response):
    return {"meta": {"status": 200,
                     "message": "Success!"},
            "response": {"ok": "ok"}
            }
