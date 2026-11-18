# Marathon Time Predictor

Predicting marathon finish times — with uncertainty — from race splits, using ~680,000 Berlin Marathon results (1999–2019).

> 🚧 Work in progress

## Project goals

1. **Finish time prediction** from intermediate splits, benchmarked against the classic Riegel formula
2. **"Hitting the wall" classification**: who slows down sharply in the second half?
3. **Personal case study**: applying the model to my own Berlin Marathon 2026

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/hanneshkle/marathon-time-predictor.git
cd marathon-time-predictor
uv sync                                   # create environment and install dependencies
uv run python -m marathon_predictor.data  # download and prepare the data
uv run pytest                             # run tests
```

## Project structure

```
├── data/
│   ├── raw/            # downloaded source files (not versioned)
│   └── processed/      # cleaned data (not versioned)
├── notebooks/          # exploratory analysis
├── src/marathon_predictor/
│   ├── config.py       # paths and data sources
│   └── data.py         # download, loading and cleaning
└── tests/              # unit tests
```

## Data

Marathon results from [AndrewMillerOnline/marathon-results](https://github.com/AndrewMillerOnline/marathon-results).
Personal identifiers (names, clubs) are dropped during processing.
