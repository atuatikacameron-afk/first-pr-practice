from meta_ads_monitor import config
from meta_ads_monitor.ad_library import fetch_ads
from meta_ads_monitor.report import format_report
from meta_ads_monitor.state import diff_ads, load_previous, save_current


def main():
    previous_by_id = load_previous(config.STATE_FILE)
    current_ads = fetch_ads(config.SEARCH_TERM, config.AD_REACHED_COUNTRIES, config.ACCESS_TOKEN)
    new_ads, stopped_ads = diff_ads(previous_by_id, current_ads)

    print(format_report(current_ads, new_ads, stopped_ads))

    save_current(current_ads, config.STATE_FILE)


if __name__ == "__main__":
    main()
