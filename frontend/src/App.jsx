import { useEffect, useState } from 'react'
import Plot from 'react-plotly.js'

import SummaryCard from "./components/SummaryCard.jsx"
import SelectInput from "./components/SelectInput.jsx"
import DateInput from "./components/DateInput.jsx"
import MultiSelectInput from "./components/MultiSelectInput.jsx";


function App() {
    // list of available stations from CIMIS dataset
    const [stations, setStations] = useState([])
    // station user selects
    const [selectedStation, setSelectedStation] = useState("")
    // stations user selects for comparison
    const [selectedStations, setSelectedStations] = useState([])
    // CIMIS observation data
    const [data, setData] = useState([])
    // CIMIS observation data for stations selected for comparison
    const [comparisonData, setComparisonData] = useState({})
    // start date user selects
    const [startDate, setStartDate] = useState("")
    // end date user selects
    const [endDate, setEndDate] = useState("")
    // aggregation user selects
    const [aggregation, setAggregation] = useState("daily")
    // summary data
    const [summary, setSummary] = useState({})

    const [error, setError] = useState("")

    useEffect(() => {
        setError("")

        fetch('http://127.0.0.1:8000/stations')
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load weather stations.")
                }

                return response.json()
            })
            .then((data) => {
                setStations(data.stations)
            })
            .catch(() => {
                setError(
                    "Unable to connect to the dashboard server. " +
                    "Please make sure the FastAPI server is running."
                )
                setStations([])
            })
    }, [])

    useEffect(() => {
        if (!selectedStation) {
            return
        }

        setError("")

        Promise.all([
            fetch(
            `http://127.0.0.1:8000/data?station=${encodeURIComponent(selectedStation)}&start_date=${startDate}&end_date=${endDate}&aggregation=${aggregation}`
            ),
            fetch(
            `http://127.0.0.1:8000/summary?station=${encodeURIComponent(selectedStation)}&start_date=${startDate}&end_date=${endDate}`
            )
        ])
            .then(async ([dataResponse, summaryResponse]) =>{
                if (!dataResponse.ok || !summaryResponse.ok) {
                    throw new Error("Failed to load dashboard data.")
                }

                const dataResult = await dataResponse.json()
                const summaryResult = await summaryResponse.json()

                setData(dataResult)
                setSummary(summaryResult)
            })
            .catch((error) => {
                setError(error.message)
                setData([])
                setSummary({})
            })
    }, [selectedStation, startDate, endDate, aggregation])

    return (
        <div className="container mt-5">
            <h1 className="text-primary">CIMIS Environmental Dashboard</h1>

            <p className="lead">
                Explore California weather and evapotranspiration data.
            </p>

            {/*Station drop-down*/}
            <SelectInput
                id="station-select"
                label="Weather Station"
                value={selectedStation}
                onChange={setSelectedStation}
                placeholder="Select a station"
                options={stations.map((station) => ({
                    value: station,
                    label: station
                }))}
            />

            {/*Multi-select station menu*/}
            <MultiSelectInput
                label="Select Stations to Compare"
                value={selectedStations}
                onChange={setSelectedStations}
                options={stations.map((station) => ({
                    value: station,
                    label: station
                }))}
            />

            {/*Aggregation drop down menu*/}
            <SelectInput
                id="aggregation-select"
                label="Aggregation"
                value={aggregation}
                onChange={setAggregation}
                options={[
                    {value: "daily", label: "Daily"},
                    {value: "monthly", label: "Monthly"},
                    {value: "annual", label: "Annual"}
                ]}
            />

            {/*Date range drop-down menus*/}
            <div className="row mb-3">
                <DateInput
                    id="start-date"
                    label="Start Date"
                    value={startDate}
                    onChange={setStartDate}
                />

                <DateInput
                    id="end-date"
                    label="End Date"
                    value={endDate}
                    onChange={setEndDate}
                />
            </div>

            {/*Display error message*/}
            {error && (
                <div className="alert alert-danger">
                    {error}
                </div>
            )}

            {/*Don't display cards or charts after an error*/}
            {!error && data.length > 0 && (
                <>
                    {/*Summary cards*/}
                    <div className="row mb-4">
                        <SummaryCard
                            title="Average Daily ETo"
                            value={summary.eto?.average_daily?.toFixed(2)}
                            unit="mm"
                        />

                        <SummaryCard
                            title="Total ETo"
                            value={summary.eto?.total?.toFixed(2)}
                            unit="mm"
                        />

                        <SummaryCard
                            title="Total Precipitation"
                            value={summary.precipitation?.total?.toFixed(2)}
                            unit="mm"
                        />

                        <SummaryCard
                            title="Average Temperature"
                            value={summary.temperature?.average?.toFixed(2)}
                            unit="°C"
                        />
                    </div>

                    {/*Line graph of ETo over time for selected station and date range*/}
                    <Plot
                        data={[{
                            x: data.map((record) => record.Date),
                            y: data.map((record) => record["ETo (mm)"]),
                            type: "scatter",
                            mode: "lines"
                        }]}

                        layout={{
                            title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Evapotranspiration`},
                            xaxis: {title: {text: "Date"}},
                            yaxis: {title: {text: "ETo (mm)"}},
                            height: 500,
                            margin: {l: 100, r: 50, t: 100, b: 100}
                        }}
                    />

                    {/* Line graph of average temperature over time for selected station and date range */}
                    <Plot
                        data={[{
                            x: data.map((record) => record.Date),
                            y: data.map((record) => record["Avg Air Temp (°C)"]),
                            type: "scatter",
                            mode: "lines"
                        }]}

                        layout={{
                            title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Average Temperature`},
                            xaxis: {title: {text: "Date"}},
                            yaxis: {title: {text: "Temperature (°C)"}},
                            height: 500,
                            margin: {l: 100, r: 50, t: 100, b: 100}
                        }}
                    />
                </>
            )}

        </div>
    )
}


export default App