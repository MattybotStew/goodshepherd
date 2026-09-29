import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { resolveMeta } from '../data/meta'

function setDescription(content) {
  let tag = document.querySelector('meta[name="description"]')
  if (!tag) {
    tag = document.createElement('meta')
    tag.setAttribute('name', 'description')
    document.head.appendChild(tag)
  }
  tag.setAttribute('content', content)
}

/**
 * Keeps <title> and the meta description in sync with the current route.
 * Rendered once inside the router so every route is covered.
 */
export default function RouteMeta() {
  const { pathname } = useLocation()

  useEffect(() => {
    const { title, description } = resolveMeta(pathname)
    document.title = title
    setDescription(description)
  }, [pathname])

  return null
}
