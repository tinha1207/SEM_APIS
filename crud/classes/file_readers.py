from dataclasses import dataclass
from typing import ClassVar
from fastapi import File
import pandas as pd

from . import bulksheet


@dataclass
class IsoFileHandler:
    """
    Requires one of the following accounts:
    ["Juvo_AMZUS","TLK_AMZUS","Juvo_AMZCA"]
    """

    # file: File
    file: str
    account: str = "Juvo_AMZUS"
    df_good = None
    df_bad = None
    new_bulksheet = None

    acceptable_accounts: ClassVar[list] = ["Juvo_AMZUS", "TLK_AMZUS", "Juvo_AMZCA"]

    def __post_init__(self):
        if self.account not in IsoFileHandler.acceptable_accounts:
            raise Exception
        self._read_iso_file(self.file)
        self.new_bulksheet = bulksheet.Bulksheet(self.account)

    def build_good_df(self):
        """Using Target and Keyword categorization, builds good df for new_bulksheet"""
        for i, row in self.df_good.iterrows():
            if row["type"] == "keyword":
                self.new_bulksheet.write_good_keyword(
                    asin=row["Asin"],
                    search_term=row["Search Term"],
                    max_bid=row["Bid"],
                    sku=row["Sku"],
                    account=self.account,
                )
            if row["type"] == "product":
                self.new_bulksheet.write_good_product(
                    asin=row["Asin"],
                    search_term=row["Search Term"],
                    max_bid=row["Bid"],
                    sku=row["Sku"],
                    account=self.account,
                )

    def build_bad_df(self):
        for i, row in self.df_bad.iterrows():
            if row["type"] == "keyword":
                self.new_bulksheet.write_negative_keyword(
                    asin=row["Asin"],
                    search_term=row["Search Term"],
                    account=self.account,
                )
            if row["type"] == "product":
                self.new_bulksheet.write_negative_product(
                    asin=row["Asin"],
                    search_term=row["Search Term"],
                    account=self.account,
                )

    def _read_iso_file(self, file):
        COLUMNS = ["Asin", "Search Term", "Bid", "Sku"]
        self.df_good = pd.read_excel(file, sheet_name="Good", usecols=COLUMNS)
        self.df_good.Asin = self.df_good.Asin.astype("str")
        self.df_good.Asin = self.df_good.Asin.str.upper()
        print(self.df_good.head())
        self.df_good["type"] = self.df_good["Search Term"].apply(
            lambda x: self._categorize_keyword_product(x)
        )
        self.df_good["Search Term"] = self.df_good["Search Term"].apply(
            lambda x: self._clean_search_terms(x)
        )
        self.df_bad = pd.read_excel(file, sheet_name="Bad")
        self.df_bad.Asin = self.df_bad.Asin.astype("str")
        self.df_bad.Asin = self.df_bad.Asin.str.upper()
        self.df_bad["type"] = self.df_bad["Search Term"].apply(
            lambda x: self._categorize_keyword_product(x)
        )
        self.df_bad["Search Term"] = self.df_bad["Search Term"].apply(
            lambda x: self._clean_search_terms(x)
        )

    def _categorize_keyword_product(self, search_term: str):
        """Looks at "Search Term" to determine if record is keyword or product"""

        if len(search_term) == 10 and search_term[:2].upper() == "B0":
            return "product"
        if len(search_term) == 10 and search_term.isalpha():
            return "product"
        return "keyword"

    def _clean_search_terms(self, search_term):
        """Gets rid of '\xa0' and '"Â"' with ' '"""
        search_term = search_term.replace(r"\xa0", " ")
        search_term = search_term.replace(r"Â", "")
        return search_term

    def export_bulksheet(self, file_name):
        df_good = self.new_bulksheet.df_good.copy()
        df_good.reset_index(inplace=True, drop=True)
        df_bad = self.new_bulksheet.df_bad.copy()
        df_bad.reset_index(inplace=True, drop=True)
        with pd.ExcelWriter(file_name) as writer:
            df_good.to_excel(writer, sheet_name="Good Search Terms", encoding="utf-8")
            df_bad.to_excel(
                writer, sheet_name="Negative Search Terms", encoding="utf-8"
            )


def main():
    ifh = IsoFileHandler(
        r"C:\Users\Tin Ha\Documents\SEM Repository\ISO\iso_template.xlsx",
        account="Juvo_AMZUS",
    )
    ifh.build_good_df()
    ifh.build_bad_df()

    ifh.export_bulksheet("export1.xlsx")


if __name__ == "__main__":
    main()
