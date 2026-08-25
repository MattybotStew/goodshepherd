import { Link } from 'react-router-dom'
import { lifeImages } from '../data/lifeImages'

function PageHero({ crumbs = [], title, lede, align = 'center', compact = false }) {
  const alignClass = align === 'left' ? ' home-hero--left' : ''
  const sizeClass = compact ? ' home-hero--compact' : ''

  return (
    <section className={`home-hero home-hero--page${alignClass}${sizeClass}`}>
      <div
        className="home-hero__photo home-hero__photo--image"
        style={{ '--hero-photo': `url(${lifeImages.hero})` }}
        aria-hidden="true"
      />
      <div className="home-hero__inner">
        {crumbs.length > 0 && (
          <nav className="page-hero__crumbs" aria-label="Breadcrumb">
            <Link to="/">Home</Link>
            {crumbs.map((c) => (
              <span key={c.label}>
                <span aria-hidden="true"> › </span>
                {c.to ? <Link to={c.to}>{c.label}</Link> : <span>{c.label}</span>}
              </span>
            ))}
          </nav>
        )}
        <h1>{title}</h1>
        {lede && <p>{lede}</p>}
      </div>
    </section>
  )
}

export default PageHero
