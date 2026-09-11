function SummaryCard({ title, value, unit }) {
    return (
        <div className="col-md-3">
            <div className="card h-100">
                <div className="card-body">
                    <h5 className="card-title">{title}</h5>

                    <p className="card-text">
                        {value} {unit}
                    </p>
                </div>
            </div>
        </div>
    )
}

export default SummaryCard