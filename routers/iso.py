from fastapi import APIRouter, Depends
import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from typing import List, Dict

import database
from crud import productad
import schemas


router = APIRouter(
    tags = ["Iso-Keywords"],
    prefix = "/iso"
)

#B00XN0KSDI

@router.get("/adgroups/{asin}")
def get_adgroups(asin:str, db:Session = Depends(database.get_db_uds)):
    return productad.get_adgroups(asin,db)
    
