from dataclasses import dataclass, field
from typing import ClassVar, List, Optional
import pandas as pd

from .lines import (
    KeywordLine,
    NegativeKeywordLine,
    CampaignNegativeKeywordLine,
    AdLine,
    AdgroupLine,
    NegativeProductTargetingLine,
    ProductTargetingLine,
)


@dataclass
class Bulksheet:
    """
    Account must be one of the following:
    ["Juvo_AMZUS","TLK_AMZUS","Juvo_AMZCA"]
    """

    df_good: pd.DataFrame = None
    df_bad: pd.DataFrame = None
    account: str = "Juvo_AMZUS"
    BULKSHEET_COLUMNS: ClassVar[list] = [
        "Record ID",
        "Record Type",
        "Campaign ID",
        "Campaign",
        "Campaign Daily Budget",
        "Portfolio ID",
        "Campaign Start Date",
        "Campaign End Date",
        "Campaign Targeting Type",
        "Ad Group",
        "Max Bid",
        "Keyword or Product Targeting",
        "Product Targeting ID",
        "Match Type",
        "SKU",
        "Campaign Status",
        "Ad Group Status",
        "Status",
        "Impressions",
        "Clicks",
        "Spend",
        "Orders",
        "Total Units",
        "Sales",
        "ACoS",
        "Bidding strategy",
        "Placement Type",
        "Increase bids by placement",
    ]

    def __post_init__(self):
        """Builds initial good and bad dataframes"""
        self.df_good = pd.DataFrame(columns=Bulksheet.BULKSHEET_COLUMNS)
        self.df_bad = pd.DataFrame(columns=Bulksheet.BULKSHEET_COLUMNS)

    def write_good_keyword(
        self, asin: str, search_term: str, max_bid: float, sku: str, account: str
    ):
        broad = IsoBroad(
            asin=asin,
            search_term=search_term,
            max_bid=max_bid,
            sku=sku,
            account=account,
        )
        exact = IsoExact(
            asin=asin,
            search_term=search_term,
            max_bid=max_bid,
            sku=sku,
            account=account,
        )
        auto = IsoAuto(asin=asin, search_term=search_term, account=account)

        # Unpack values from classes
        broad_list = [x.__dict__.values() for x in broad.lines]
        exact_list = [x.__dict__.values() for x in exact.lines]
        auto_list = [x.__dict__.values() for x in auto.lines]

        # Build individual dataframes
        df_broad = pd.DataFrame(broad_list, columns=Bulksheet.BULKSHEET_COLUMNS)
        df_exact = pd.DataFrame(exact_list, columns=Bulksheet.BULKSHEET_COLUMNS)
        df_auto = pd.DataFrame(auto_list, columns=Bulksheet.BULKSHEET_COLUMNS)

        # Built Good Dataframe
        self.df_good = pd.concat([self.df_good, df_broad], axis=0)
        self.df_good = pd.concat([self.df_good, df_exact], axis=0)
        self.df_good = pd.concat([self.df_good, df_auto], axis=0)

    def write_good_product(
        self, asin: str, search_term: str, max_bid: float, sku: str, account: str
    ):
        product = IsoProduct(
            asin=asin,
            search_term=search_term,
            max_bid=max_bid,
            sku=sku,
            account=account,
        )
        product_list = [x.__dict__.values() for x in product.lines]

        df_product = pd.DataFrame(product_list, columns=Bulksheet.BULKSHEET_COLUMNS)
        self.df_good = pd.concat([self.df_good, df_product], axis=0)

    def write_negative_keyword(self, asin: str, search_term: str, account: str):
        negative_keyword = IsoNegativeKeyword(
            asin=asin, search_term=search_term, account=account
        )
        negative_keyword_list = [x.__dict__.values() for x in negative_keyword.lines]

        df_negative_keyword = pd.DataFrame(
            negative_keyword_list, columns=Bulksheet.BULKSHEET_COLUMNS
        )
        self.df_bad = pd.concat([self.df_bad, df_negative_keyword], axis=0)

    def write_negative_product(self, asin: str, search_term: str, account: str):
        negative_product = IsoNegativeProduct(
            asin=asin, search_term=search_term, account=account
        )
        negative_product_list = [x.__dict__.values() for x in negative_product.lines]
        df_negative_product = pd.DataFrame(
            negative_product_list, columns=Bulksheet.BULKSHEET_COLUMNS
        )
        self.df_bad = pd.concat([self.df_bad, df_negative_product], axis=0)

    def clean_search_term(self):
        """Gets rid of '/xa0' invisible character"""


@dataclass
class IsoBroad:
    asin: str
    search_term: str
    max_bid: float
    sku: str
    lines: list = field(default_factory=list)
    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.campaign = f"{self.account}_{self.asin}_ISO_Broad"
        self.adgroup = f"AG_{self.asin}_M_Broad_{self.search_term}"
        self.write_adgroup_line()
        self.write_ad_line()
        self.write_keyword_line()
        self.write_negative_keyword_line()

    def write_adgroup_line(self):
        self.lines.append(
            AdgroupLine(
                campaign=self.campaign, adgroup=self.adgroup, max_bid=self.max_bid
            )
        )

    def write_ad_line(self):
        self.lines.append(
            AdLine(campaign=self.campaign, adgroup=self.adgroup, sku=self.sku)
        )

    def write_keyword_line(self):
        self.lines.append(
            KeywordLine(
                campaign=self.campaign,
                adgroup=self.adgroup,
                max_bid=self.max_bid,
                keyword_or_product_targeting=self.search_term,
                match_type="broad",
            )
        )

    def write_negative_keyword_line(self):
        self.lines.append(
            CampaignNegativeKeywordLine(
                campaign=self.campaign,
                keyword_or_product_targeting=self.search_term,
                match_type="Campaign Negative Exact",
            )
        )


@dataclass
class IsoExact:
    asin: str
    search_term: str
    max_bid: float
    sku: str
    lines: list = field(default_factory=list)

    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.campaign = f"{self.account}_{self.asin}_ISO_Exact"
        self.adgroup = f"AG_{self.asin}_M_Exact_{self.search_term}"
        self.write_adgroup_line()
        self.write_ad_line()
        self.write_keyword_line()

    def write_adgroup_line(self):
        self.lines.append(
            AdgroupLine(
                campaign=self.campaign, adgroup=self.adgroup, max_bid=self.max_bid
            )
        )

    def write_ad_line(self):
        self.lines.append(
            AdLine(campaign=self.campaign, adgroup=self.adgroup, sku=self.sku)
        )

    def write_keyword_line(self):
        self.lines.append(
            KeywordLine(
                campaign=self.campaign,
                adgroup=self.adgroup,
                max_bid=self.max_bid,
                keyword_or_product_targeting=self.search_term,
                match_type="exact",
            )
        )


@dataclass
class IsoAuto:
    asin: str
    search_term: str
    lines: list = field(default_factory=list)
    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.campaign = f"{self.account}_{self.asin}_ISO_Auto"
        self.write_negative_exact()

    def write_negative_exact(self):  # Create a negative campaign keyword line
        self.lines.append(
            CampaignNegativeKeywordLine(
                campaign=self.campaign,
                # adgroup=f"AG_{self.asin}_A",
                keyword_or_product_targeting=self.search_term,
                match_type="Campaign Negative Exact",
            )
        )


@dataclass
class IsoProduct:
    asin: str
    search_term: str
    max_bid: float
    sku: str
    lines: list = field(default_factory=list)
    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.campaign = f"{self.account}_{self.asin}_ISO_Exact"
        self.adgroup = f"AG_{self.asin}_M_Product_{self.search_term.upper()}"
        self.write_adgroup_line()
        self.write_ad_line()
        self.write_product_line()
        self.write_negative_product_line()

    def write_adgroup_line(self):
        self.lines.append(
            AdgroupLine(
                campaign=self.campaign, adgroup=self.adgroup, max_bid=self.max_bid
            )
        )

    def write_ad_line(self):
        self.lines.append(
            AdLine(campaign=self.campaign, adgroup=self.adgroup, sku=self.sku)
        )

    def write_product_line(self):
        self.lines.append(
            ProductTargetingLine(
                campaign=self.campaign,
                adgroup=self.adgroup,
                max_bid=self.max_bid,
                product_targeting_id=f'asin="{self.search_term.upper()}"',
            )
        )

    def write_negative_product_line(self):
        self.lines.append(
            NegativeProductTargetingLine(
                campaign=f"{self.account}_{self.asin}_ISO_Auto",
                adgroup=f"AG_{self.asin}_A",
                product_targeting_id=f'asin="{self.search_term.upper()}"',
            )
        )


@dataclass
class IsoNegativeKeyword:
    asin: str
    search_term: str
    lines: list = field(default_factory=list)
    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.write_negative_campaign_exact()
        self.write_negative_campaign_broad()
        self.write_negative_auto()

    def write_negative_campaign_exact(self):
        exact_campaign = f"{self.account}_{self.asin.upper()}_ISO_Exact"
        self.lines.append(
            CampaignNegativeKeywordLine(
                campaign=exact_campaign,
                keyword_or_product_targeting=self.search_term,
                match_type="Campaign Negative Exact",
            )
        )

    def write_negative_campaign_broad(self):
        broad_campaign = f"{self.account}_{self.asin.upper()}_ISO_Broad"
        self.lines.append(
            CampaignNegativeKeywordLine(
                campaign=broad_campaign,
                keyword_or_product_targeting=self.search_term,
                match_type="Campaign Negative Exact",
            )
        )

    def write_negative_auto(self):
        auto_campaign = f"{self.account}_{self.asin.upper()}_ISO_Auto"
        auto_adgroup = f"AG_{self.asin.upper()}_A"
        self.lines.append(
            NegativeKeywordLine(
                campaign=auto_campaign,
                adgroup=auto_adgroup,
                keyword_or_product_targeting=self.search_term,
                match_type="Negative Exact",
            )
        )


@dataclass
class IsoNegativeProduct:
    asin: str
    search_term: str
    lines: list = field(default_factory=list)
    account: str = "Juvo_AMZUS"

    def __post_init__(self):
        self.write_negative_auto()
        self.write_archive_exact()

    def write_negative_auto(self):
        auto_campaign = f"{self.account}_{self.asin.upper()}_ISO_Auto"
        auto_adgroup = f"AG_{self.asin}_A"
        self.lines.append(
            NegativeProductTargetingLine(
                campaign=auto_campaign,
                adgroup=auto_adgroup,
                product_targeting_id=f'asin="{self.search_term}"',
            )
        )

    def write_archive_exact(self):
        exact_campaign = f"{self.account}_{self.asin.upper()}_ISO_Exact"
        exact_adgroup = f"AG_{self.asin.upper()}_M_Product_{self.search_term}"
        self.lines.append(
            AdgroupLine(
                campaign=exact_campaign,
                adgroup=exact_adgroup,
                adgroup_status="archived",
                max_bid=0.02,
            )
        )
