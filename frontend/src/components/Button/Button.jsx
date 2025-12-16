import React from 'react'

const Button = ({ text, type = "button", className = "", ...props }) => {
    return (
        <button type={type} className={`btn ${className}`} {...props}>
            {text}
        </button>
    )
}

export default Button