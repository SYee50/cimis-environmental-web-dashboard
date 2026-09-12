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

    const [stationError, setStationError] = useState("")
    const [comparisonError, setComparisonError] = useState("")

    useEffect(() => {
        setStationError("")

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
                setStationError(
                    "Unable to connect to the dashboard server. " +
                    "Please make sure the FastAPI server is running."
                )
                setStations([])
            })
    }, [])

    useEffect(() => {
        if (selectedStations.length === 0) {
            setComparisonData({})
            setComparisonError("")
            return
        }

        setComparisonError("")

        fetch(
            `http://127.0.0.1:8000/compare?stations=${encodeURIComponent(selectedStations.join(","))}&start_date=${startDate}&end_date=${endDate}&aggregation=${aggregation}`
        )
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load comparison data.")
                }

                return response.json()
            })
            .then((data) => {
                setComparisonData(data)
            })
            .catch((error) => {
                setComparisonError(error.message)
                setComparisonData({})
            })
    }, [selectedStations, startDate, endDate, aggregation])

    useEffect(() => {
        if (!selectedStation) {
            setData([])
            setSummary({})
            setStationError("")
            return
        }

        setStationError("")

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
                setStationError(error.message)
                setData([])
                setSummary({})
            })
    }, [selectedStation, startDate, endDate, aggregation])

    return (
        <div className="container-fluid min-vh-100 px-3 py-3">
            <h1 className="text-primary">CIMIS Environmental Dashboard</h1>

            <p className="lead">
                Explore California weather and evapotranspiration data.
            </p>

            {/* Display error messages */}
            {(stationError || comparisonError) && (
                <div className="mb-4">

                    {stationError && (
                        <div className="alert alert-danger">
                            {stationError}
                        </div>
                    )}

                    {comparisonError && (
                        <div className="alert alert-danger">
                            {comparisonError}
                        </div>
                    )}

                </div>
            )}

            {/*Main Dashboard*/}
            <div className="row g-4">

                {/*Left Half*/}
                <div className="col-lg-6">
                    <div className="row g-4">

                        {/*Controls*/}
                        <div className="col-sm-6">
                            <div className="card h-100">
                                <div className="card-body">

                                    <h2 className="h5 mb-3">Controls</h2>

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

                                    {/*Date range inputs*/}
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
                            </div>
                        </div>

                        {/*Summary Cards*/}
                        {!stationError && data.length > 0 && (
                            <>
                            <div className="col-sm-6">
                                <div className="card h-100">
                                    <div className="card-body">

                                        <h2 className="h5 mb-3">Summary</h2>

                                        <div className="d-flex flex-column gap-3">
                                            {/*Summary cards*/}
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
                                    </div>
                                </div>
                            </div>
                            </>
                        )}
                    </div>
                </div>

                {/*Right Half*/}
                <div className="col-lg-6">
                    <div className="row g-4">

                        {/*Individual station ETo chart */}
                        {!stationError && data.length > 0 && (
                            <>
                            <div className="col-12">
                                <div className="card">
                                    <div className="card-body">
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
                                                height: 400,
                                                margin: {l: 100, r: 50, t: 100, b: 100}
                                            }}

                                            useResizeHandler={true}

                                            style={{width: "100%"}}
                                        />
                                    </div>
                                </div>
                            </div>
                            </>
                        )}

                        {/*Individual station temperature chart*/}
                        {!stationError && data.length > 0 && (
                            <>
                            <div className="col-12">
                                <div className="card">
                                    <div className="card-body">
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
                                                height: 400,
                                                margin: {l: 100, r: 50, t: 100, b: 100}
                                            }}

                                            useResizeHandler={true}

                                            style={{width: "100%"}}
                                        />
                                    </div>
                                </div>
                            </div>
                            </>
                        )}
                    </div>
                </div>
            </div>

            {/* Bar graph comparing precipitation across selected stations */}
            {!comparisonError && selectedStations.length > 0 && (
                <div className="row g-4 mt-2">

                    {/*ETo station comparison line graph*/}
                    <div className="col-lg-6">
                        <div className="card">
                            <div className="card-body">
                                <Plot
                                    data={selectedStations.map((station) => ({
                                        x: comparisonData[station]?.map((record) => record.Date),
                                        y: comparisonData[station]?.map((record) => record["ETo (mm)"]),
                                        type: "scatter",
                                        mode: "lines",
                                        name: station
                                    }))}

                                    layout={{
                                        title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} ETo Comparison`},
                                        xaxis: {title: {text: "Date"}},
                                        yaxis: {title: {text: "ETo (mm)"}},
                                        height: 400,
                                        margin: {l: 100, r: 50, t: 100, b: 100}
                                    }}

                                    useResizeHandler={true}

                                    style={{width: "100%"}}
                                />
                            </div>
                        </div>
                    </div>

                    {/*Average temperature station comparison line graph*/}
                    <div className="col-lg-6">
                        <div className="card">
                            <div className="card-body">
                                <Plot
                                    data={selectedStations.map((station) => ({
                                        x: comparisonData[station]?.map((record) => record.Date),
                                        y: comparisonData[station]?.map((record) => record["Avg Air Temp (°C)"]),
                                        type: "scatter",
                                        mode: "lines",
                                        name: station
                                    }))}

                                    layout={{
                                        title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Average Temperature Comparison`},
                                        xaxis: {title: {text: "Date"}},
                                        yaxis: {title: {text: "Average Temperature (°C)"}},
                                        height: 400,
                                        margin: {l: 100, r: 50, t: 100, b: 100}
                                    }}

                                    useResizeHandler={true}

                                    style={{width: "100%"}}
                                />
                            </div>
                        </div>
                    </div>

                    {/*Precipitation station comparison bar graph*/}
                    <div className="col-lg-6">
                        <div className="card">
                            <div className="card-body">
                                <Plot
                                    data={selectedStations.map((station) => ({
                                        x: comparisonData[station]?.map((record) => record.Date),
                                        y: comparisonData[station]?.map((record) => record["Precip (mm)"]),
                                        type: "bar",
                                        name: station
                                    }))}

                                    layout={{
                                        title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Precipitation Comparison`},
                                        xaxis: {title: {text: "Date"}},
                                        yaxis: {title: {text: "Precipitation (mm)"}},
                                        barmode: "group",
                                        height: 400,
                                        margin: {l: 100, r: 50, t: 100, b: 100}
                                    }}

                                    useResizeHandler={true}

                                    style={{width: "100%"}}
                                />
                            </div>
                        </div>
                    </div>

                    {/*Average solar radiation station comparison line graph*/}
                    <div className="col-lg-6">
                        <div className="card">
                            <div className="card-body">
                                <Plot
                                    data={selectedStations.map((station) => ({
                                        x: comparisonData[station]?.map((record) => record.Date),
                                        y: comparisonData[station]?.map((record) => record["Avg Sol Rad (W/m²)"]),
                                        type: "scatter",
                                        mode: "lines",
                                        name: station
                                    }))}

                                    layout={{
                                        title: {text: `${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Solar Radiation Comparison`},
                                        xaxis: {title: {text: "Date"}},
                                        yaxis: {title: {text: "Average Solar Radiation (W/m²)"}},
                                        height: 400,
                                        margin: {l: 100, r: 50, t: 100, b: 100}
                                    }}

                                    useResizeHandler={true}

                                    style={{width: "100%"}}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}

export default App