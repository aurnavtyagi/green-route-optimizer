# Delhi AI Green Route

Traffic, weather, and air-quality aware route optimization and congestion analysis for Delhi.

## What is in this repo

- `app.py` runs the Streamlit demo for green route selection.
- `src/` contains routing, AQI, weather, emission, and visualization helpers.
- `models/` contains the traffic prediction and report generation workflow.
- `reports/` and the summary `.md` files contain the generated analysis outputs.

## Setup

1. Create and activate your Python environment.
2. Install dependencies from the project requirements files.
3. Copy `.env.example` to `.env` and add your AQICN token.

## Environment variables

- `AQICN_API_TOKEN`: required for AQI lookups.

## Run the Streamlit app

```bash
streamlit run app.py
```

## Notes

- Large raw datasets are excluded from git via `.gitignore`.
- Generated reports and analysis artifacts are kept in the repository for reference.
