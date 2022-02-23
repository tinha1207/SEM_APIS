from fastapi import APIRouter, File, UploadFile
from fastapi.params import Form
from fastapi.responses import FileResponse
import pandas as pd
from crud.bulksheets import create_temp_file
import os

from crud.bulksheets2 import create_iso_file_handler


router = APIRouter(tags=["Utility"], prefix="/utility")


# @router.post("/fileupload")
# async def upload_file(file: bytes = File(...), data: str = Form(...)):
#     df = create_temp_file(file)
#     path = f"{os.getcwd()}//files/random.xlsx"
#     new_file = df.to_excel(path)
#     print(data)
#     return FileResponse(path, headers={"Content-Type": "multipart/form-data"})


@router.post("/fileupload")
async def upload_file(file: bytes = File(...), data: str = Form(...)):
    return create_iso_file_handler(file, data)
