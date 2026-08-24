import { Link } from 'react-router-dom'
import PageHero from './PageHero'
import '../styles/starter.css'

/**
 * Shared article-detail template — the layout used by program detail pages
 * (hero + optional side nav + rich-text sections + photo gallery). News
 * articles reuse the exact same template so the whole site keeps one
 * inner-page layout (per AGENTS.md).
 */

export function RichBlocks({ blocks = [] }) {
  return blocks.map((block, i) => {
    switch (block.type) {
      case 'h3':
        return <h3 key={i}>{block.text}</h3>
      case 'p':
        return <p key={i}>{block.text}</p>
      case 'ul':
        return (
          <ul key={i}>
            {block.items.map((item, j) => (
              <li key={j}>{item}</li>
            ))}
          </ul>
        )
      case 'ol':
        return (
          <ol key={i}>
            {block.items.map((item, j) => (
              <li key={j}>{item}</li>
            ))}
          </ol>
        )
      case 'quote':
        return (
          <blockquote key={i}>
            <p>{block.text}</p>
            {block.cite && <cite>{block.cite}</cite>}
          </blockquote>
        )
      case 'figure':
        return (
          <figure className="rte-figure" key={i}>
            <div className="img-ph" aria-hidden="true" />
            {block.caption && <figcaption>{block.caption}</figcaption>}
          </figure>
        )
      case 'callout':
        return (
          <aside className="rte-callout" key={i}>
            {block.title && <strong>{block.title}</strong>}
            <p>{block.text}</p>
          </aside>
        )
      case 'link':
        return (
          <p key={i}>
            <Link to={block.to} className="text-link">
              {block.label}
            </Link>
          </p>
        )
      default:
        return null
    }
  })
}

export function RichSection({ id, title, blocks = [] }) {
  return (
    <section className="rte anchor" id={id || undefined}>
      <h2>{title}</h2>
      <RichBlocks blocks={blocks} />
    </section>
  )
}

export function PhotoGallery() {
  return (
    <section className="rte-gallery" aria-label="Photo gallery">
      <h2>Photo gallery</h2>
      <div className="gallery">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div className="img-ph gallery__item" key={i} aria-hidden="true" />
        ))}
      </div>
    </section>
  )
}

export default function ArticleDetailPage({
  crumbs = [],
  title,
  lede,
  align = 'left',
  compact = true,
  sidebar,
  children,
  gallery = false,
}) {
  return (
    <article>
      <PageHero
        align={align}
        compact={compact}
        crumbs={crumbs}
        title={title}
        lede={lede}
      />

      <div className={sidebar ? 'page-body page-body--with-nav' : 'page-body'}>
        {sidebar}
        <div>
          {children}
          {gallery && <PhotoGallery />}
        </div>
      </div>
    </article>
  )
}
