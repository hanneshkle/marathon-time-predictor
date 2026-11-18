"""Central project configuration: paths and data sources."""

from pathlib import Path

# Repository root: src/marathon_predictor/config.py -> two levels up from the package
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Public marathon results collected by Andrew Miller:
# https://github.com/AndrewMillerOnline/marathon-results
SOURCE_URL = (
    "https://raw.githubusercontent.com/AndrewMillerOnline/marathon-results/main/"
    "{race}/results-{year}.csv"
)
BERLIN_YEARS = range(1999, 2020)  # 1999-2019

# Split checkpoints in race order: column name -> distance in km
SPLITS_KM = {
    "split_5k": 5.0,
    "split_10k": 10.0,
    "split_15k": 15.0,
    "split_20k": 20.0,
    "time_half": 21.0975,
    "split_25k": 25.0,
    "split_30k": 30.0,
    "split_35k": 35.0,
    "split_40k": 40.0,
    "time_full": 42.195,
}
