import os
from fastapi import APIRouter, File, UploadFile, Request, Response, HTTPException
from backend.config import DATA_PATH, BASE_DIR
from backend.utils.parser import FileParser
from ml.model import predict_docs_class


router = APIRouter(prefix="/api")

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename[filename.rfind('.') + 1:]
    if ext not in ["doc", "docx", "rtf", "pdf"]:
        print(ext)
        raise HTTPException(400, detail="Invalid document type")
    contents = file.file.read()
    file_path = os.path.join(DATA_PATH, file.filename)
    with open(file_path, 'wb') as f:
        f.write(contents)
    file.file.close()
    parser = FileParser(filename)
    json_string = parser.parse()
    print(type(json_string))
    # answer = predict_docs_class(BASE_DIR + "/ml/data.json")
    answer = predict_docs_class(json_string)
    print(answer)
    return {"message": f"Successfuly uploaded {file.filename}"}


@router.get("/download")
async def download(response: Response):
    return {"meta": {"status": 200,
                     "message": "Success!"},
            "response": {"ok": "ok"}
            }
