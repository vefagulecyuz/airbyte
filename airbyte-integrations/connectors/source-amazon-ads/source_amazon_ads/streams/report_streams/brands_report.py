#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from http import HTTPStatus

from .products_report import SponsoredProductsReportStream

METRICS_MAP_V3 = {
    "purchasedAsin": [
        "campaignBudgetCurrencyCode",
        "campaignName",
        "adGroupName",
        "attributionType",
        "purchasedAsin",
        "productName",
        "productCategory",
        "sales14d",
        "orders14d",
        "unitsSold14d",
        "newToBrandSales14d",
        "newToBrandPurchases14d",
        "newToBrandUnitsSold14d",
        "newToBrandSalesPercentage14d",
        "newToBrandPurchasesPercentage14d",
        "newToBrandUnitsSoldPercentage14d",
    ],
    "keywords": [
        "addToCart",
        "addToCartClicks",
        "addToCartRate",
        "adGroupId",
        "adGroupName",
        "addToList",
        "addToListFromClicks",
        "qualifiedBorrows",
        "qualifiedBorrowsFromClicks",
        "royaltyQualifiedBorrows",
        "royaltyQualifiedBorrowsFromClicks",
        "brandedSearches",
        "brandedSearchesClicks",
        "campaignBudgetAmount",
        "campaignBudgetCurrencyCode",
        "campaignBudgetType",
        "campaignId",
        "campaignName",
        "campaignStatus",
        "clicks",
        "cost",
        "costType",
        "detailPageViews",
        "detailPageViewsClicks",
        "eCPAddToCart",
        "endDate",
        "impressions",
        "keywordBid",
        "keywordId",
        "adKeywordStatus",
        "keywordText",
        "keywordType",
        "matchType",
        "newToBrandDetailPageViewRate",
        "newToBrandDetailPageViews",
        "newToBrandDetailPageViewsClicks",
        "newToBrandECPDetailPageView",
        "newToBrandPurchases",
        "newToBrandPurchasesClicks",
        "newToBrandPurchasesPercentage",
        "newToBrandPurchasesRate",
        "newToBrandSales",
        "newToBrandSalesClicks",
        "newToBrandSalesPercentage",
        "newToBrandUnitsSold",
        "newToBrandUnitsSoldClicks",
        "newToBrandUnitsSoldPercentage",
        "purchases",
        "purchasesClicks",
        "purchasesPromoted",
        "sales",
        "salesClicks",
        "salesPromoted",
        "startDate",
        "targetingExpression",
        "targetingId",
        "targetingText",
        "targetingType",
        "topOfSearchImpressionShare",
        "unitsSold",

    ]
}

METRICS_TYPE_TO_ID_MAP_V3 = {
    "purchasedAsin": "purchasedAsin",
    "keywords": "keywordId"
}


class SponsoredBrandsV3ReportStream(SponsoredProductsReportStream):
    """
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#purchased-product-reports
    """

    API_VERSION = "reporting"  # v3
    REPORT_DATE_FORMAT = "YYYY-MM-DD"
    ad_product = "SPONSORED_BRANDS"
    report_is_created = HTTPStatus.OK
    metrics_map = METRICS_MAP_V3
    metrics_type_to_id_map = METRICS_TYPE_TO_ID_MAP_V3

    def _get_init_report_body(self, report_date: str, record_type: str, profile):
        metrics_list = self.metrics_map[record_type]

        reportTypeId = "sbPurchasedProduct"
        group_by = ["purchasedAsin"]
        filters = []

        if record_type == "keywords":
            group_by = ["targeting"]
            reportTypeId = "sbTargeting"
            filters = [{"field": "keywordType", "values": ["BROAD", "PHRASE", "EXACT"]}]

        body = {
            "name": f"{record_type} report {report_date}",
            "startDate": report_date,
            "endDate": report_date,
            "configuration": {
                "adProduct": self.ad_product,
                "groupBy": group_by,
                "columns": metrics_list,
                "reportTypeId": reportTypeId,
                "filters": filters,
                "timeUnit": "SUMMARY",
                "format": "GZIP_JSON",
            },
        }

        yield body
