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
  mosaicImages,
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
  const mosaicCells = [
    { className: 'home-mission__ph--tall', src: mosaicImages?.[0] },
    { className: 'home-mission__ph--short', src: mosaicImages?.[1] },
    { className: 'home-mission__ph--short', src: mosaicImages?.[2] },
    { className: 'home-mission__ph--tall', src: mosaicImages?.[3] },
  ]

  function MosaicCell({ className, src }) {
    return src ? (
      <img src={src} alt="" className={`home-mission__ph ${className}`} />
    ) : (
      <div className={`home-mission__ph ${className}`} />
    )
  }

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
            <MosaicCell className="home-mission__ph--tall" src={mosaicCells[0].src} />
            <MosaicCell className="home-mission__ph--short" src={mosaicCells[1].src} />
          </div>
          <div className="home-mission__col home-mission__col--offset">
            <MosaicCell className="home-mission__ph--short" src={mosaicCells[2].src} />
            <MosaicCell className="home-mission__ph--tall" src={mosaicCells[3].src} />
          </div>
        </div>
      </div>
    </section>
  )
}
