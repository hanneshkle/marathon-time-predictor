import numpy as np
import pandas as pd

from marathon_predictor.data import clean_berlin, time_to_seconds


def test_time_to_seconds_parses_valid_times():
    result = time_to_seconds(pd.Series(["02:01:41", "00:00:05"]))
    assert result.tolist() == [7301.0, 5.0]


def test_time_to_seconds_handles_missing_and_malformed():
    result = time_to_seconds(pd.Series([None, "not a time"]))
    assert result.isna().all()


def test_clean_berlin_drops_names_and_non_finishers():
    raw = pd.DataFrame(
        {
            "first_name": ["A", "B"],
            "last_name": ["X", "Y"],
            "club": [np.nan, "Club"],
            "nationality": ["GER", "SWE"],
            "gender": ["W", "M"],
            "year": [2019, 2019],
            **{
                col: ["00:30:00", None]
                for col in [
                    "split_5k", "split_10k", "split_15k", "split_20k", "time_half",
                    "split_25k", "split_30k", "split_35k", "split_40k", "time_full",
                ]
            },
        }
    )
    df = clean_berlin(raw)

    assert len(df) == 1  # runner without finish time removed
    assert "first_name" not in df.columns
    assert df.loc[0, "gender"] == "F"
    assert df.loc[0, "time_full"] == 1800.0
