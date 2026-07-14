import json
import os


def load_previous(state_file):
    if not os.path.exists(state_file):
        return {}
    with open(state_file) as f:
        return {ad["id"]: ad for ad in json.load(f)}


def save_current(ads, state_file):
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(ads, f, indent=2)


def diff_ads(previous_by_id, current_ads):
    """Compare current Ad Library snapshot against the previous one.

    Returns (new_ads, newly_stopped_ads).
    """
    new_ads = []
    newly_stopped_ads = []

    for ad in current_ads:
        prev = previous_by_id.get(ad["id"])
        if prev is None:
            new_ads.append(ad)
            continue

        if not prev.get("ad_delivery_stop_time") and ad.get("ad_delivery_stop_time"):
            newly_stopped_ads.append(ad)

    return new_ads, newly_stopped_ads
