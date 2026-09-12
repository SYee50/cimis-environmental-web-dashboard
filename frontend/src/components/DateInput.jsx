function DateInput({
    id,
    label,
    value,
    onChange
}) {
    return (
        <div className="mb-3">
            <label htmlFor={id} className={"form-label"}>
                {label}
            </label>

            <input
                id={id}
                type="date"
                className="form-control"
                value={value}
                onChange={(event) => onChange(event.target.value)}
            />
        </div>
    )
}

export default DateInput