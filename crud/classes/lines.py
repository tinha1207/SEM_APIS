from fastapi import File, Form
import pandas as pd
import datetime as dt
from dataclasses import dataclass
from typing import Optional


@dataclass
class Line:
    """Base Class for Bulksheet line"""

    record_id: Optional[str] = ""
    record_type: Optional[str] = ""
    campaign_id: Optional[str] = ""
    campaign: Optional[str] = ""
    campaign_daily_budget: Optional[str] = ""
    portfolio_id: Optional[str] = ""
    campaign_start_date: Optional[str] = ""
    campaign_end_date: Optional[str] = ""
    campaign_targeting_type: Optional[str] = ""
    adgroup: Optional[str] = ""
    max_bid: Optional[str] = ""
    keyword_or_product_targeting: Optional[str] = ""
    product_targeting_id: Optional[str] = ""
    match_type: Optional[str] = ""
    sku: Optional[str] = ""
    campaign_status: Optional[str] = ""
    adgroup_status: Optional[str] = ""
    status: Optional[str] = ""
    impressions: Optional[str] = ""
    clicks: Optional[str] = ""
    spend: Optional[str] = ""
    orders: Optional[str] = ""
    total_units: Optional[str] = ""
    sales: Optional[str] = ""
    acos: Optional[str] = ""
    bidding_strategy: Optional[str] = ""
    placement_type: Optional[str] = ""
    increase_bids_by_placements: Optional[str] = ""


@dataclass
class AdgroupLine(Line):
    # campaign: str
    # adgroup: str
    # max_bid: float
    record_type: str = "Ad Group"
    adgroup_status: str = "enabled"


@dataclass
class AdLine(Line):

    # campaign: str
    # adgroup: str
    # sku: str
    record_type: str = "Ad"
    status: str = "enabled"


@dataclass
class KeywordLine(Line):
    """
    Available Match Types:
    ["broad","exact"]
    """

    # campaign: str
    # adgroup: str
    # max_bid: float
    # keyword_or_product_targeting: str
    # match_type: str
    record_type: str = "Keyword"
    status: str = "Enabled"


@dataclass
class CampaignNegativeKeywordLine(Line):
    """
    For Broad Adgroups
    Need keyword_or_product_targeting
    Available Match Types:
    ["Campaign Negative Exact", "Campaign Negative Phrase"]
    """

    # campaign: str
    # keyword_or_product_targeting: str
    # match_type: str
    record_type: str = "Keyword"
    status: str = "enabled"


@dataclass
class NegativeKeywordLine(Line):
    """
    For Auto Adgroups

    Need:
    - campaign: str
    - adgroup: str
    - keyword_or_product_targeting: str
    - match_type: str

    Available Match Types:
    ["Negative Exact", "Negative Phrase"]
    """

    # campaign: str
    # adgroup: str
    # keyword_or_product_targeting: str
    # match_type: str
    record_type: str = "Keyword"
    status: str = "enabled"


@dataclass
class ProductTargetingLine(Line):
    """
    For converting competitor asins
    """

    # campaign: str
    # adgroup: str
    # max_bid: float
    # product_targeting_id: str
    match_type: str = "Targeting Expression"
    record_type: str = "Product Targeting"
    status: str = "Enabled"


@dataclass
class NegativeProductTargetingLine(Line):
    # campaign: str
    # adgroup: str
    # product_targeting_id: str
    match_type: str = "Negative Targeting Expression"
    record_type: str = "Product Targeting"
    status: str = "Enabled"


def main():
    pass


if __name__ == "__main__":
    main()
