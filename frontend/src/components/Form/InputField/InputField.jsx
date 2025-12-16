import React from 'react'

const InputField = ({
  label,
  type = 'text',
  id,
  name,
  register,
  error }) => {
  return (
    <div className="form-labels">
      <label htmlFor={id}>{label}</label>
      <input
        type={type}
        id={id}
        {...register(name)}
        className={error ? 'error' : ''} />

      {error && <p className="form-error">{error.message}</p>}
      
    </div>
  )
}

export default InputField