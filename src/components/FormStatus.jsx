import './FormStatus.css'

/**
 * Renders the result of a form submission. Uses role=status for success and
 * role=alert for errors so assistive tech announces the change.
 */
export default function FormStatus({ status, error, demo }) {
  if (status === 'success') {
    return (
      <p className="form-status form-status--success" role="status">
        {demo
          ? 'Thanks! This is a prototype — the form is not connected to a destination yet.'
          : "Thanks — we'll be in touch soon."}
      </p>
    )
  }

  if (status === 'error') {
    return (
      <p className="form-status form-status--error" role="alert">
        {error ? `Something went wrong: ${error}. Please try again.` : 'Something went wrong. Please try again.'}
      </p>
    )
  }

  return null
}
