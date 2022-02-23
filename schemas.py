from pydantic import BaseModel
from typing import Optional, List, Dict

    
class ShowProductAd(BaseModel):
    date: str
    market: str
    adid: int
    adgroupid: str
    campaignid: int
    asin:str
    sku:str
    state:str
    create_date:str
    last_updated_date:str
    servingstatus:str
    uds_load_date:str
    sales_channel_id:int

    class Config:
        orm_mode=True
    
class ShowProductAds(BaseModel):
    adgroupid: Optional[ShowProductAd]

    class Config:
        orm_mode=True