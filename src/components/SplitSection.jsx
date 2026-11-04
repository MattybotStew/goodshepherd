import { Link } from 'react-router-dom'
import '../styles/starter.css'

const isExternal = (to) => /^https?:\/\//.test(to)

export default function SplitSection({
  id,
  eyebrow,
  title,
  children,
  flip = false,
  alt = false,
  softImage = false,
  imageSrc,
  imageAlt = '',
  linkTo,
  linkLabel,
}) {
  const sectionClass = ['split', 'anchor', alt && 'band--alt'].filter(Boolean).join(' ')
  const innerClass = ['wrap', 'split__inner', flip && 'split--flip'].filter(Boolean).join(' ')
  const imageClass = ['img-ph', 'img-ph--tall', softImage && 'img-ph--soft', imageSrc && 'img-ph--photo']
    .filter(Boolean)
    .join(' ')

  return (
    <section className={sectionClass} id={id || undefined}>
      <div className={innerClass}>
        <div className="split__copy">
          {eyebrow && <span className="eyebrow">{eyebrow}</span>}
          {title && <h2>{title}</h2>}
          {children}
          {linkTo && linkLabel && isExternal(linkTo) ? (
            <a
              href={linkTo}
              className="text-link"
              target="_blank"
              rel="noreferrer"
            >
              {linkLabel}
            </a>
          ) : linkTo && linkLabel ? (
            <Link to={linkTo} className="text-link">
              {linkLabel}
            </Link>
          ) : null}
        </div>
        {imageSrc ? (
          <img src={imageSrc} alt={imageAlt} className={imageClass} />
        ) : (
          <div className={imageClass} aria-hidden="true" />
        )}
      </div>
    </section>
  )
}
