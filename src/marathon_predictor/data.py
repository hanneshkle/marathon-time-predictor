"""Download, load and clean the Berlin Marathon results.

Run from the repository root:

    uv run python -m marathon_predictor.data
"""

import argparse

import pandas as pd
import requests

from marathon_predictor.config import (
    BERLIN_YEARS,
    PROCESSED_DIR,
    RAW_DIR,
    SOURCE_URL,
    SPLITS_KM,
)


def download_berlin(force: bool = False) -> None:
    """Download one raw CSV per year into data/raw/berlin/ (skips existing files)."""
    target_dir = RAW_DIR / "berlin"
    target_dir.mkdir(parents=True, exist_ok=True)

    for year in BERLIN_YEARS:
        path = target_dir / f"results-{year}.csv"
        if path.exists() and not force:
            continue
        url = SOURCE_URL.format(race="Berlin", year=year)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        path.write_bytes(response.content)
        print(f"Downloaded {year} ({len(response.content) / 1e6:.1f} MB)")


def time_to_seconds(times: pd.Series) -> pd.Series:
    """Convert 'HH:MM:SS' strings to seconds; missing or malformed values become NaN."""
    return pd.to_timedelta(times, errors="coerce").dt.total_seconds()


def load_berlin_raw() -> pd.DataFrame:
    """Concatenate all raw yearly CSVs into one DataFrame."""
    files = sorted((RAW_DIR / "berlin").glob("results-*.csv"))
    if not files:
        raise FileNotFoundError("No raw data found. Run download_berlin() first.")
    return pd.concat((pd.read_csv(f) for f in files), ignore_index=True)


def clean_berlin(raw: pd.DataFrame) -> pd.DataFrame:
    """Turn raw results into an analysis-ready table.

    - converts all split times to seconds
    - drops personal identifiers (names, club) - we don't need them for modelling
    - keeps only finishers with a valid finish time
    """
    df = pd.DataFrame(
        {
            "year": raw["year"].astype(int),
            "gender": raw["gender"].replace({"W": "F"}),
            "nationality": raw["nationality"],
        }
    )
    for col in SPLITS_KM:
        df[col] = time_to_seconds(raw[col])

    df = df.dropna(subset=["time_full"]).reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and prepare Berlin Marathon data.")
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    args = parser.parse_args()

    download_berlin(force=args.force)
    df = clean_berlin(load_berlin_raw())

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "berlin.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {len(df):,} finishers to {out}")


if __name__ == "__main__":
    main()
