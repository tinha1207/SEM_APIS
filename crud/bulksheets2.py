from fastapi import File
from fastapi.params import Form
from fastapi.responses import FileResponse
import pandas as pd
import datetime as dt
import os

from crud.classes.file_readers import IsoFileHandler


def create_iso_file_handler(file: bytes = File(...), data: str = Form(...)):
    path = f"{os.getcwd()}//files/iso_bulksheet.xlsx"
    account = data
    fh = IsoFileHandler(file, account)
    fh.build_good_df()
    fh.build_bad_df()
    fh.export_bulksheet(path)
    return FileResponse(path, headers={"Content-Type": "multipart/form-data"})
