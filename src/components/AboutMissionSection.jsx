import { Link } from 'react-router-dom'
import { LOREM_EXTRA, LOREM_LONG } from '../data/placeholders'
import './AboutMissionSection.css'

const HOME_COPY = [
  LOREM_LONG,
  LOREM_EXTRA,
]

const ABOUT_COPY = [
  LOREM_LONG,
  LOREM_EXTRA,
]

export default function AboutMissionSection({
  showReadMore = true,
  overlapHero = false,
  compactBottom = false,
  placeholderCopy = false,
  eyebrow = 'About Us',
  title = 'A community of care, growth, and dignity for over 50 years.',
  paragraphs,
  id,
}) {
  const sectionClass = [
    'home-mission',
    overlapHero && 'home-mission--overlap',
    compactBottom && 'home-mission--compact-bottom',
  ]
    .filter(Boolean)
    .join(' ')

  const copy = paragraphs || (placeholderCopy ? HOME_COPY : ABOUT_COPY)

  return (
    <section className={sectionClass} id={id || undefined}>
      <div className="home-mission__inner">
        <div className="home-mission__copy">
          <p className="home-mission__eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
          {copy.map((text) => (
            <p key={text.slice(0, 24)}>{text}</p>
          ))}
          {showReadMore && (
            <Link to="/about" className="home-mission__btn">
              Read More
            </Link>
          )}
        </div>
        <div className="home-mission__mosaic" aria-hidden="true">
          <div className="home-mission__col">
            <div className="home-mission__ph home-mission__ph--tall" />
            <div className="home-mission__ph home-mission__ph--short" />
          </div>
          <div className="home-mission__col home-mission__col--offset">
            <div className="home-mission__ph home-mission__ph--short" />
            <div className="home-mission__ph home-mission__ph--tall" />
          </div>
        </div>
      </div>
    </section>
  )
}
