from fastapi import File
import pandas as pd
import datetime as dt
from dataclasses import dataclass
from typing import List


def create_temp_file(file: bytes = File(...)):
    FILE_INPUT = file
    BULKSHEET_COLUMNS = [
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

    @dataclass
    class Record:
        asin: str
        sku: str
        keyword: str
        bid: int

    def get_today() -> str:
        """Returns YYYYMMDD format"""
        date = dt.date.today()
        date = date.strftime("%Y%m%d")
        return date

    def validate_inputs(asin: str, match_type: str):
        match_type = match_type.title()
        if match_type not in ["Exact", "Broad", "Auto"]:
            print("Not valid match type")
            raise Exception
        if len(asin) != 10:
            print("Not valid asin")
            raise Exception

    def get_campaign(asin: str, match_type: str, market: str = "US") -> str:
        """Gets iso campaigns of the asin"""
        match_type = match_type.title()
        validate_inputs(asin, match_type)

        campaign = f"Juvo_AMZ{market.upper()}_{asin.upper()}_ISO_{match_type.title()}"
        return campaign

    def create_adgroup(asin: str, match_type: str, keyword: str):
        """"""
        match_type = match_type.title()
        validate_inputs(asin, match_type)
        adgroup = f"AG_{asin.upper()}_M_{match_type}_{keyword.lower()}"
        return adgroup

    def create_adgroup_line(
        campaign, adgroup, max_bid, adgroup_status="enabled", record_type="Ad Group"
    ):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": adgroup,
            "Max Bid": max_bid,
            "Keyword or Product Targeting": "",
            "Product Targeting ID": "",
            "Match Type": "",
            "SKU": "",
            "Campaign Status": "",
            "Ad Group Status": adgroup_status,
            "Status": "",
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def create_ad_line(campaign, adgroup, sku, status="enabled", record_type="Ad"):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": adgroup,
            "Max Bid": "",
            "Keyword or Product Targeting": "",
            "Product Targeting ID": "",
            "Match Type": "",
            "SKU": sku,
            "Campaign Status": "",
            "Ad Group Status": "",
            "Status": status,
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def create_keyword_line(
        campaign,
        adgroup,
        max_bid,
        keyword,
        match_type,
        status="Enabled",
        record_type="Keyword",
    ):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": adgroup,
            "Max Bid": max_bid,
            "Keyword or Product Targeting": keyword,
            "Product Targeting ID": "",
            "Match Type": match_type,
            "SKU": "",
            "Campaign Status": "",
            "Ad Group Status": "",
            "Status": status,
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def create_negative_keyword_line(
        campaign,
        keyword,
        match_type="Campaign Negative Exact",
        status="Enabled",
        record_type="Keyword",
    ):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": "",
            "Max Bid": "",
            "Keyword or Product Targeting": keyword,
            "Product Targeting ID": "",
            "Match Type": match_type,
            "SKU": "",
            "Campaign Status": "",
            "Ad Group Status": "",
            "Status": status,
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def create_product_targeting(
        campaign,
        adgroup,
        max_bid,
        product,
        match_type="Targeting Expression",
        status="Enabled",
        record_type="Product Targeting",
    ):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": adgroup,
            "Max Bid": max_bid,
            "Keyword or Product Targeting": "",
            "Product Targeting ID": f'asin="{product.upper()}"',
            "Match Type": match_type,
            "SKU": "",
            "Campaign Status": "",
            "Ad Group Status": "",
            "Status": status,
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def create_negative_product_targeting(
        campaign,
        adgroup,
        product,
        match_type="Negative Targeting Expression",
        status="Enabled",
        record_type="Product Targeting",
    ):
        return {
            "Record ID": "",
            "Record Type": record_type,
            "Campaign ID": "",
            "Campaign": campaign,
            "Campaign Daily Budget": "",
            "Portfolio ID": "",
            "Campaign Start Date": "",
            "Campaign End Date": "",
            "Campaign Targeting Type": "",
            "Ad Group": adgroup,
            "Max Bid": "",
            "Keyword or Product Targeting": "",
            "Product Targeting ID": f'asin="{product.upper()}"',
            "Match Type": match_type,
            "SKU": "",
            "Campaign Status": "",
            "Ad Group Status": "",
            "Status": status,
            "Impressions": "",
            "Clicks": "",
            "Spend": "",
            "Orders": "",
            "Total Units": "",
            "Sales": "",
            "ACoS": "",
            "Bidding strategy": "",
            "Placement Type": "",
            "Increase bids by placement": "",
        }

    def read_file(file):
        USE_COLUMNS = ["asin", "sku", "keyword", "bid"]
        df = pd.read_excel(file, engine="openpyxl", usecols=USE_COLUMNS)
        df.asin = df.asin.astype("str")
        df_dict = df.to_dict(orient="index")
        list_records = [
            Record(v["asin"], v["sku"], v["keyword"], v["bid"])
            for v in df_dict.values()
        ]
        return list_records

    def read_negatives(file) -> List:
        USE_COLUMNS = ["asin", "keyword"]

        df = pd.read_excel(file, sheet_name="Negative Exact", usecols=USE_COLUMNS)
        df.asin = df.asin.astype("str")
        list_values = df.values.tolist()
        return list_values

    def read_products(file) -> List:
        USE_COLUMNS = ["asin", "product", "max_bid", "sku"]
        df = pd.read_excel(file, sheet_name="Product Targeting", usecols=USE_COLUMNS)
        df.asin = df.asin.astype("str")
        list_values = df.values.tolist()
        return list_values

    def read_negative_products(file) -> List:
        USE_COLUMNS = ["asin", "product"]
        df = pd.read_excel(file, sheet_name="Negative Product", usecols=USE_COLUMNS)
        df.asin = df.asin.astype("str")
        list_values = df.values.tolist()
        return list_values

    def main():
        list_records = read_file(FILE_INPUT)
        match_types = ["Broad", "Exact", "Auto"]

        bulk_sheet_lines = []

        for record in list_records:
            campaigns = []
            adgroups = []
            matches = ["broad", "exact", "auto"]
            for match in matches:
                campaigns.append(get_campaign(record.asin, match))
                adgroups.append(create_adgroup(record.asin, match, record.keyword))
            print(campaigns)
            print(adgroups)

            # BROAD
            bulk_sheet_lines.append(
                create_adgroup_line(campaigns[0], adgroups[0], record.bid).values()
            )
            bulk_sheet_lines.append(
                create_ad_line(campaigns[0], adgroups[0], record.sku).values()
            )
            bulk_sheet_lines.append(
                create_keyword_line(
                    campaigns[0], adgroups[0], record.bid, record.keyword, matches[0]
                ).values()
            )
            bulk_sheet_lines.append(
                create_negative_keyword_line(campaigns[0], record.keyword).values()
            )

            # EXACT
            bulk_sheet_lines.append(
                create_adgroup_line(campaigns[1], adgroups[1], record.bid).values()
            )
            bulk_sheet_lines.append(
                create_ad_line(campaigns[1], adgroups[1], record.sku).values()
            )
            bulk_sheet_lines.append(
                create_keyword_line(
                    campaigns[1], adgroups[1], record.bid, record.keyword, matches[1]
                ).values()
            )

            # AUTO
            bulk_sheet_lines.append(
                create_negative_keyword_line(campaigns[2], record.keyword).values()
            )
            bulk_sheet_lines.append(
                create_negative_keyword_line(
                    campaigns[2], record.keyword, match_type="Campaign Negative Phrase"
                ).values()
            )

        # Negative Exact
        negatives_list = read_negatives(FILE_INPUT)
        for negative_exact in negatives_list:
            bulk_sheet_lines.append(
                create_negative_keyword_line(
                    f"Juvo_AMZUS_{negative_exact[0].upper()}_ISO_Auto",
                    negative_exact[1],
                ).values()
            )
            bulk_sheet_lines.append(
                create_negative_keyword_line(
                    f"Juvo_AMZUS_{negative_exact[0].upper()}_ISO_Broad",
                    negative_exact[1],
                ).values()
            )

        # Product Targeting
        product_targets_list = read_products(FILE_INPUT)
        for record in product_targets_list:
            bulk_sheet_lines.append(
                create_adgroup_line(
                    f"Juvo_AMZUS_{record[0].upper()}_ISO_Exact",
                    f"AG_{record[0].upper()}_M_Product_{record[1].upper()}",
                    record[2],
                ).values()
            )
            bulk_sheet_lines.append(
                create_ad_line(
                    f"Juvo_AMZUS_{record[0]}_ISO_Exact",
                    f"AG_{record[0].upper()}_M_Product_{record[1].upper()}",
                    record[3],
                ).values()
            )
            bulk_sheet_lines.append(
                create_product_targeting(
                    f"Juvo_AMZUS_{record[0].upper()}_ISO_Exact",
                    f"AG_{record[0].upper()}_M_Product_{record[1].upper()}",
                    record[2],
                    record[1].upper(),
                ).values()
            )
            bulk_sheet_lines.append(
                create_negative_product_targeting(
                    f"Juvo_AMZUS_{record[0].upper()}_ISO_Auto",
                    f"AG_{record[0].upper()}_A",
                    record[1].upper(),
                ).values()
            )
        # Negative Product Targeting
        negative_products_list = read_negative_products(FILE_INPUT)
        for record in negative_products_list:
            bulk_sheet_lines.append(
                create_negative_product_targeting(
                    f"Juvo_AMZUS_{record[0].upper()}_ISO_Auto",
                    f"AG_{record[0].upper()}_A",
                    record[1].upper(),
                ).values()
            )

        df = pd.DataFrame(bulk_sheet_lines, columns=BULKSHEET_COLUMNS)
        print(df)
        return df

    return main()
