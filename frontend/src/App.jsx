import { useEffect, useState } from 'react'
import Plot from 'react-plotly.js'

import SummaryCard from "./components/SummaryCard.jsx"
import SelectInput from "./components/SelectInput.jsx"
import DateInput from "./components/DateInput.jsx"


function App() {
    // list of available stations from CIMIS dataset
    const [stations, setStations] = useState([])
    // station user selects
    const [selectedStation, setSelectedStation] = useState("")
    // CIMIS observation data
    const [data, setData] = useState([])
    // start date user selects
    const [startDate, setStartDate] = useState("")
    // end date user selects
    const [endDate, setEndDate] = useState("")
    // aggregation user selects
    const [aggregation, setAggregation] = useState("daily")
    // summary data
    const [summary, setSummary] = useState({})

    useEffect(() => {
        fetch('http://127.0.0.1:8000/stations')
            .then((response) => response.json())
            .then((data) => {
                setStations(data.stations)
            })
    }, [])

    useEffect(() => {
        if (!selectedStation) {
            return
        }

        fetch(
            `http://127.0.0.1:8000/data?station=${encodeURIComponent(selectedStation)}&start_date=${startDate}&end_date=${endDate}&aggregation=${aggregation}`
        )
            .then((response) => response.json())
            .then((data) => setData(data))

        fetch(
            `http://127.0.0.1:8000/summary?station=${encodeURIComponent(selectedStation)}&start_date=${startDate}&end_date=${endDate}`
        )
            .then((response) => response.json())
            .then((data) => setSummary(data))

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
                    title: {text: "Daily Evapotranspiration"},
                    xaxis: {title: {text: "Date"}},
                    yaxis: {title: {text: "ETo (mm)"}},
                    height: 500,
                    margin: {l: 100, r: 50, t: 100, b: 100}
                }}
            />
        </div>
    )
}


export default App