# CIMIS Environmental Web Dashboard

An interactive full-stack web dashboard for exploring California weather and reference evapotranspiration data from California Irrigation Management Information System (CIMIS) weather stations.

The dashboard allows users to filter observations by station and date range, aggregate data at daily, monthly, or annual levels, view summary statistics, and compare environmental variables across multiple stations.

## Demo

<!-- TODO: Replace this placeholder with the recorded demo GIF. -->

![CIMIS Environmental Dashboard Demo](docs/demo.gif)

## Features

* Select from five CIMIS weather stations
* Filter data by date range
* View daily, monthly, or annual aggregations
* View summary statistics for:

    * Average daily reference evapotranspiration (ETo)
    * Total reference evapotranspiration (ETo)
    * Total precipitation
    * Average temperature
* Interactive Plotly visualizations
* Visualize environmental variables including:

  * Reference evapotranspiration (ETo)
  * Average air temperature
  * Precipitation
  * Solar radiation
* Compare multiple weather stations
* FastAPI REST API
* Automated backend tests with pytest
* React frontend with Vite build tooling
* Responsive Bootstrap layout

## Dashboard

The dashboard provides two main views.

### Station Analysis

Users can select a station, date range, and aggregation level to explore individual station data and summary statistics.

The summary cards display:

* Average daily ETo
* Total ETo
* Total precipitation
* Average temperature

The dashboard also provides interactive visualizations for environmental variables including ETo, temperature, precipitation, and solar radiation.

### Station Comparison

Multiple CIMIS stations can be selected to compare environmental variables over the same date range.

Comparison visualizations include:

* ETo
* Average air temperature
* Precipitation
* Solar radiation

## Technology Stack

### Frontend

* React
* JavaScript
* Bootstrap
* Plotly.js
* Vite
* npm

### Backend

* Python
* FastAPI
* pandas
* NumPy
* Uvicorn

### Testing

* pytest
* httpx

### Data

* CIMIS daily weather observations
* Five California weather stations
* Reference evapotranspiration (ETo)
* Precipitation
* Solar radiation
* Vapor pressure
* Maximum, minimum, and average air temperature
* Maximum, minimum, and average relative humidity
* Dew point
* Wind speed

## Architecture

```text
React Frontend
    │
    │ HTTP requests
    ▼
FastAPI REST API
    │
    ▼
Data Services
    │
    ├── Filtering
    ├── Aggregation
    └── Summary Statistics
    │
    ▼
CIMIS Dataset
```

The frontend is responsible for user interaction and visualization, while the FastAPI backend handles data filtering, aggregation, summary calculations, and station comparisons.

## Project Structure

```text
cimis-environmental-web-dashboard/
├── backend/
│   ├── api/
│   │   ├── compare.py
│   │   ├── data.py
│   │   ├── stations.py
│   │   └── summary.py
│   ├── services/
│   │   ├── aggregation_service.py
│   │   └── data_service.py
│   ├── tests/
│   │   ├── test_aggregation.py
│   │   ├── test_api.py
│   │   ├── test_comparison.py
│   │   └── test_data_service.py
│   └── main.py
│
├── data/
│   └── cimis_daily_clean.csv
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DateInput.jsx
│   │   │   ├── MultiSelectInput.jsx
│   │   │   ├── SelectInput.jsx
│   │   │   └── SummaryCard.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── README.md
└── requirements.txt
```

## API Endpoints

### Get Available Stations

```text
GET /stations
```

Returns the available CIMIS weather stations.

### Get Station Data

```text
GET /data
```

Parameters:

* `station`
* `start_date`
* `end_date`
* `aggregation`

Example:

```text
/data?station=Davis&start_date=2020-01-01&end_date=2020-12-31&aggregation=monthly
```

### Get Summary Statistics

```text
GET /summary
```

Returns summary statistics for a selected station and date range.

Example:

```text
/summary?station=Davis&start_date=2020-01-01&end_date=2020-12-31
```

### Compare Stations

```text
GET /compare
```

Compare multiple stations over a specified date range.

Example:

```text
/compare?stations=Davis,Bishop&start_date=2020-01-01&end_date=2020-12-31&aggregation=monthly
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SYee50/cimis-environmental-web-dashboard.git
cd cimis-environmental-web-dashboard
```

### 2. Create and activate the Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
```

## Running the Application

The backend and frontend run separately.

### Start the backend

From the project root:

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload
```

The FastAPI server will run at:

```text
http://127.0.0.1:8000
```

### Start the Frontend

Open a second terminal:

```bash
cd frontend
npm run dev
```

The Vite development server will run at:

```text
http://localhost:5173
```

Open the displayed URL in a browser.

### Testing

Backend tests are written with pytest.

From the project root:

```bash
python -m pytest
```

The current test suite contains 43 tests covering API endpoints, data filtering, aggregation, summary calculations, and station comparisons.

## Production Build

To create a production build of the React frontend:

```bash
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

## Data Processing

The dashboard uses a cleaned daily CIMIS dataset containing weather and reference evapotranspiration measurements.

The backend performs filtering and aggregation dynamically rather than requiring separate datasets for each aggregation level.

For monthly and annual views:

* ETo and precipitation are summed
* Maximum and minimum temperature values use their respective extremes
* Average environmental measurements use their mean

## Future Improvements

Potential future improvements include:

* Additional CIMIS stations
* Additional environmental variables and visualization types
* More advanced date and station filtering
* Improved chart configuration and accessibility
* Deployment to a cloud platform
* Integration of ETo prediction models from the companion machine learning project
* Interactive prediction error analysis and model comparison

## Motivation

I became interested in exploring environmental datasets and understanding how weather conditions relate to reference evapotranspiration (ETo). This project was built as a companion to my [CIMIS ETo Machine Learning project](https://github.com/SYee50/cimis-eto-ml), which uses the same underlying environmental data to develop and evaluate machine learning models for ETo prediction.

While the machine learning project focuses on prediction and model evaluation, this dashboard focuses on exploring the underlying data through filtering, aggregation, summary statistics, and interactive visualizations.

Building both projects also gave me an opportunity to develop full-stack software engineering skills, including data processing, REST API development, React frontend development, interactive visualization, automated testing, and Git-based development.
