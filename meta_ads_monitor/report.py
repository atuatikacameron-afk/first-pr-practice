def format_report(current_ads, new_ads, stopped_ads):
    lines = [f"Truform Ad Library check: {len(current_ads)} active ad(s) found."]

    if new_ads:
        lines.append(f"\n{len(new_ads)} new ad(s):")
        for ad in new_ads:
            body = (ad.get("ad_creative_bodies") or [""])[0]
            lines.append(f"  - [{ad['id']}] {ad.get('page_name')}: {body[:120]}")
            lines.append(f"    {ad.get('ad_snapshot_url')}")

    if stopped_ads:
        lines.append(f"\n{len(stopped_ads)} ad(s) stopped running:")
        for ad in stopped_ads:
            lines.append(f"  - [{ad['id']}] {ad.get('page_name')} (stopped {ad.get('ad_delivery_stop_time')})")

    if not new_ads and not stopped_ads:
        lines.append("No changes since last check.")

    return "\n".join(lines)
