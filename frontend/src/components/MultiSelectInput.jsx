// function MultiSelectInput({
//     label,
//     value,
//     onChange,
//     options
// }) {
//     const handleChange = (station) => {
//         if (value.includes(station)) {
//             onChange(
//                 value.filter(
//                     (selectedStation) => selectedStation !== station
//                 )
//             )
//         } else {
//             onChange([...value, station])
//         }
//     }
//
//     return (
//         <div className="mb-3">
//             <label className="form-label">
//                 {label}
//             </label>
//
//             <div>
//                 {options.map((option) => {
//                     const isSelected = value.includes(option.value)
//
//                     return (
//                         <button
//                             key={option.value}
//                             type="button"
//                             className={
//                                 isSelected
//                                     ? "btn btn-primary me-2 mb-2"
//                                     : "btn btn-outline-primary me-2 mb-2"
//                             }
//                             onClick={() => handleChange(option.value)}
//                         >
//                             {option.label}
//                         </button>
//                     )
//                 })}
//             </div>
//         </div>
//     )
// }
//
// export default MultiSelectInput

import { useState } from "react"

function MultiSelectInput({
    label,
    value,
    onChange,
    options
}) {
    const [isOpen, setIsOpen] = useState(false)

    const handleChange = (station) => {
        if (value.includes(station)) {
            onChange(
                value.filter(
                    (selectedStation) => selectedStation !== station
                )
            )
        } else {
            onChange([...value, station])
        }
    }

    return (
        <div className="mb-3">
            <label className="form-label">
                {label}
            </label>

            <button
                type="button"
                className="form-select text-start"
                onClick={() => setIsOpen(!isOpen)}
            >
                {value.length > 0
                    ? value.join(", ")
                    : "Select stations"}
            </button>

            {isOpen && (
                <div className="border rounded bg-white p-2">
                    {options.map((option) => {
                        const isSelected = value.includes(option.value)

                        return (
                            <div
                                key={option.value}
                                className={
                                    isSelected
                                        ? "p-2 bg-primary text-white rounded"
                                        : "p-2"
                                }
                                onClick={() =>
                                    handleChange(option.value)
                                }
                            >
                                {option.label}
                            </div>
                        )
                    })}
                </div>
            )}
        </div>
    )
}

export default MultiSelectInput