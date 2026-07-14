import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ["META_ACCESS_TOKEN"]
SEARCH_TERM = os.environ.get("TRUFORM_SEARCH_TERM", "Truform")
AD_REACHED_COUNTRIES = os.environ.get("AD_REACHED_COUNTRIES", "US").split(",")

STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STATE_FILE = os.path.join(STATE_DIR, "ad_library_state.json")
