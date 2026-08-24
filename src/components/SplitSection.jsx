import { Link } from 'react-router-dom'
import '../styles/starter.css'

export default function SplitSection({
  id,
  eyebrow,
  title,
  children,
  flip = false,
  alt = false,
  softImage = false,
  linkTo,
  linkLabel,
}) {
  const sectionClass = ['split', 'anchor', alt && 'band--alt'].filter(Boolean).join(' ')
  const innerClass = ['wrap', 'split__inner', flip && 'split--flip'].filter(Boolean).join(' ')
  const imageClass = ['img-ph', 'img-ph--tall', softImage && 'img-ph--soft']
    .filter(Boolean)
    .join(' ')

  return (
    <section className={sectionClass} id={id || undefined}>
      <div className={innerClass}>
        <div className="split__copy">
          {eyebrow && <span className="eyebrow">{eyebrow}</span>}
          {title && <h2>{title}</h2>}
          {children}
          {linkTo && linkLabel && (
            <Link to={linkTo} className="text-link">
              {linkLabel}
            </Link>
          )}
        </div>
        <div className={imageClass} aria-hidden="true" />
      </div>
    </section>
  )
}
