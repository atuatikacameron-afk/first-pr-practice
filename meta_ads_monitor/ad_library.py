import json

import requests

API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}/ads_archive"

FIELDS = [
    "id",
    "page_id",
    "page_name",
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_creative_bodies",
    "ad_creative_link_captions",
    "ad_creative_link_titles",
    "ad_snapshot_url",
]


def fetch_ads(search_term, ad_reached_countries, access_token):
    """Fetch all Ad Library entries matching search_term, following pagination."""
    ads = []
    params = {
        "search_terms": search_term,
        "ad_reached_countries": json.dumps(ad_reached_countries),
        "ad_type": "ALL",
        "fields": ",".join(FIELDS),
        "access_token": access_token,
        "limit": 100,
    }

    url = BASE_URL
    while url:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        ads.extend(payload.get("data", []))

        next_url = payload.get("paging", {}).get("next")
        url = next_url
        params = None  # next_url already includes all query params

    return ads
