import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import Column, and_
from sqlalchemy.engine import Engine
import pandas as pd

import database


def get_today():
    date = dt.date.today()
    date = date.strftime("%Y-%m-%d")
    return date

def get_yesterday():
    date = dt.date.today()-dt.timedelta(days=1)
    date = date.strftime("%Y-%m-%d")
    return date


def get_adgroups(asin:str ,db:Session):
    now = dt.datetime.now()
    if now <= dt.datetime(now.year,now.month,now.day,10):
        date = get_yesterday()
    else:
        date = get_today()
    query = """
        SELECT * FROM amz_ads_sp_productads
        WHERE asin = %(asin)s
        AND date = %(date)s
        AND sales_channel_id = 1111
        AND market = 'US'
        AND asin is NOT NULL
        AND state in ('enabled','paused')
        AND servingstatus NOT IN ('CAMPAIGN_ARCHIVED','ADGROUP_ARCHIVED')
    """
    params={
        "asin":asin,
        "date":date
    }
    df = pd.read_sql(query,db,params=params)
    df.drop_duplicates(inplace=True)
    response = df.to_dict(orient="index")
    return response

    



