# Delhi AI Green Route Optimizer

Delhi AI Green Route Optimizer is a data-informed route recommendation application
that helps people travel through Delhi with lower estimated carbon emissions. Instead
of choosing a route using travel time alone, the application compares available
driving routes and considers route distance, estimated congestion, weather
conditions, air quality, and vehicle type.

The project combines a Streamlit user interface with routing, geocoding, weather,
air-quality, emission-calculation, visualization, and traffic-analysis modules.
It is intended as a practical prototype for greener urban mobility and as a
foundation for more advanced traffic and emissions prediction systems.

## The real-life problem

Delhi faces several connected transportation challenges:

- Heavy traffic increases idling, fuel consumption, journey time, and vehicle
  emissions.
- The shortest route is not always the cleanest route. A short route with severe
  congestion can produce more emissions than a slightly longer, faster-moving
  alternative.
- Weather conditions such as rain, poor visibility, and high temperature can
  affect driving conditions and traffic flow.
- Air pollution is already a serious public-health concern, so route decisions
  should account for the conditions in the places where people start and finish
  their journeys.
- Conventional navigation generally optimizes for distance or time, but does not
  clearly communicate the environmental cost of each alternative.

These issues affect commuters, delivery services, fleet operators, emergency
responders, and city planners. Even small reductions in fuel use and congestion
across many daily journeys can reduce emissions and improve urban mobility.

## Our solution

The application turns a normal route search into an environmental comparison:

1. The user enters a starting location and destination in Delhi.
2. The locations are geocoded into coordinates.
3. The routing service retrieves up to three alternative driving routes.
4. The application obtains current weather conditions and, when configured,
   nearby air-quality data.
5. A congestion factor is estimated from route speed and adjusted using weather
   and AQI conditions.
6. Estimated CO2 emissions are calculated for the selected vehicle type.
7. Routes are compared by estimated emissions, and the lowest-emission route is
   highlighted on an interactive map.
8. The interface displays distance, duration, estimated emissions, weather,
   AQI category, and available pollutant information so that the recommendation
   is understandable rather than a black box.

The current emission model is deliberately transparent: it uses vehicle-specific
base factors and a congestion multiplier. This makes the prototype easy to
understand and extend with measured fuel-consumption data, live traffic speeds,
vehicle load, road grade, or a trained emissions model.

## Main benefits

### For commuters

- Makes the environmental trade-off between route alternatives visible.
- Helps users choose a route that balances travel time and estimated emissions.
- Provides air-quality context at both the origin and destination.

### For fleet and delivery operations

- Supports lower-emission route planning for repeated trips.
- Can help identify routes where congestion causes avoidable fuel waste.
- Provides a base for fleet dashboards, trip histories, and carbon reporting.

### For communities and city planners

- Demonstrates how traffic, weather, and pollution data can be combined for
  location-aware mobility decisions.
- Can support future studies of congestion hotspots and emissions reduction.
- Provides an extensible platform for integrating predictive traffic models and
  additional city datasets.

## Features

- Delhi-focused Streamlit web application.
- Start and destination location input.
- Petrol, diesel, CNG, and electric vehicle options.
- Multiple alternative driving routes from OSRM.
- Route geometry rendered on an interactive map.
- Distance and duration comparison for every route.
- Estimated CO2 output in grams and kilograms.
- Weather-aware congestion adjustment using temperature, rain, and visibility.
- Optional AQI and pollutant lookup through AQICN/World Air Quality Index.
- AQI category and health guidance for the start and end locations.
- Traffic prediction, data-processing, visualization, and report-generation
  workflows in the `models/` and project scripts.

## How the recommendation works

For each route, the application estimates average speed from route distance and
duration. It derives a base congestion value and adds adjustments from available
weather and AQI data. The emission calculator then applies the resulting factor
to a vehicle-specific base emission rate:

```text
estimated CO2 = distance × vehicle base factor × congestion factor
```

The route with the smallest estimated CO2 value is marked as the recommended
green route. This is an estimate for decision support, not a certified
measurement of actual vehicle emissions. Results can vary with vehicle
condition, driving style, traffic changes, fuel quality, and data availability.

## Repository structure

```text
.
├── app.py                         # Streamlit application
├── src/
│   ├── api/                       # Weather and AQI integrations
│   ├── config/                    # Environment and secret loading
│   ├── emission/                  # Vehicle emission calculations
│   ├── ml/                        # Synthetic data/model utilities
│   ├── routing/                   # Geocoding and route retrieval
│   └── visualization/             # Interactive map generation
├── models/                        # Traffic analysis and report workflows
├── data/                          # Local input and processed datasets
├── reports/                       # Generated analysis outputs
├── requirements.txt               # Application dependencies
└── .env.example                   # Environment variable template
```

Large raw datasets, local environments, secrets, caches, and generated artifacts
are excluded from version control where appropriate. They may need to be
downloaded or generated locally before running the analysis workflows.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd delhi-green-route-optimizer
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you are running the model and reporting workflows, also install the
model-specific dependencies:

```bash
pip install -r models/requirements.txt
```

## Configuration

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Then set:

| Variable | Required | Purpose |
| --- | --- | --- |
| `AQICN_API_TOKEN` | Optional | Enables AQI and pollutant lookups from AQICN/WAQI. |

The app can run without the AQI token; AQI sections will show that data is
unavailable, while routing and emission comparison can still be used. Never
commit `.env`, API tokens, or other credentials to GitHub.

## Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, enter two Delhi locations, choose a
vehicle type, and select **Find Green Route**.

The application uses external services for geocoding, routing, weather, and
optional AQI data. Their availability, rate limits, and response quality can
affect results. An internet connection is therefore required for live route
lookups.

## Analysis and research workflows

In addition to the interactive demo, the repository contains scripts and
notebooks-style workflows for:

- data cleaning and preprocessing;
- traffic congestion analysis;
- traffic prediction experiments;
- feature analysis and visualizations;
- synthetic-data generation;
- comparative model evaluation; and
- report and research-paper generation.

Review the scripts in the repository and the documentation files such as
`ASSIGNMENT_SUMMARY.md`, `COMPARATIVE_ANALYSIS_README.md`, and
`DELIVERY_PACKAGE_INDEX.md` for the available analysis outputs.

## Limitations and future improvements

This project is a research and demonstration prototype. Important next steps
include:

- replacing estimated congestion with a live traffic feed;
- calibrating emission factors using real vehicle and fuel data;
- adding route-level pollution exposure instead of using endpoint AQI only;
- supporting walking, cycling, public transport, and multimodal trips;
- adding historical traffic forecasting and peak-hour predictions;
- validating recommendations against measured fuel consumption and trip data;
- adding caching, retries, and clearer service-status reporting for external APIs;
- providing fleet, accessibility, and city-planning dashboards.

## Responsible use

The recommended route should be treated as an estimate and not as a guarantee
of the lowest real-world emissions or safest journey. Users should follow local
traffic rules, current road closures, weather warnings, and public-health advice.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Keep secrets and large private datasets out of Git.
2. Update documentation when behavior or setup changes.
3. Test the affected workflow locally.
4. Explain changes to data sources, assumptions, or emission calculations.
