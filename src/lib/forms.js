import { useState } from 'react'

/**
 * Destination for all site forms. Set VITE_FORM_ENDPOINT to a real handler
 * (e.g. a Formspree/SureForms endpoint) to enable delivery. Until then the
 * wire resolves locally so the flow is demonstrable without sending anything.
 */
export const FORM_ENDPOINT = import.meta.env.VITE_FORM_ENDPOINT || ''

export async function submitForm(payload) {
  if (!FORM_ENDPOINT) {
    await new Promise((resolve) => setTimeout(resolve, 400))
    return { ok: true, demo: true }
  }

  const response = await fetch(FORM_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return { ok: true, demo: false }
}

/**
 * Handles a form's submit event: prevents the default navigation, posts the
 * named fields, and exposes idle / submitting / success / error state.
 */
export function useFormSubmit() {
  const [state, setState] = useState({ status: 'idle', error: null, demo: false })

  async function handleSubmit(event) {
    event.preventDefault()
    const form = event.currentTarget
    const values = Object.fromEntries(new FormData(form))
    setState({ status: 'submitting', error: null, demo: false })

    try {
      const result = await submitForm(values)
      form.reset()
      setState({ status: 'success', error: null, demo: result.demo })
    } catch (error) {
      setState({ status: 'error', error: error.message, demo: false })
    }
  }

  return { ...state, handleSubmit }
}
