import os
from fastapi import APIRouter, File, UploadFile, Response
from config import DATA_PATH


router = APIRouter(prefix="/api")

@router.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()
            file_path = os.path.join(DATA_PATH, file.filename)
            with open(file_path, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}


@router.get("/download")
async def download(response: Response):
    return {"meta": {"status": 200,
                     "message": "Success!"},
            "response": {"ok": "ok"}
            }