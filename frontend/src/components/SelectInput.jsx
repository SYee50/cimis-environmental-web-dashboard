function SelectInput({
    id,
    label,
    value,
    onChange,
    options,
    placeholder
                     }) {
    return (
        <div className="mb-3">
            <label htmlFor={id} className="form-label">
                {label}
            </label>

            <select
                id={id}
                className="form-select"
                value={value}
                onChange={(event) => onChange(event.target.value)}
            >
                {placeholder && (
                    <option value="">
                        {placeholder}
                    </option>
                )}

                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    )
}

export default SelectInput