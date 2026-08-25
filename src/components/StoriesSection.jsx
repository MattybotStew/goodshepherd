import { Link } from 'react-router-dom'
import { stories as defaultStories } from '../data/site'
import { LOREM, LOREM_SHORT } from '../data/placeholders'
import readMoreArrow from '../assets/home-stories/read-more-arrow.svg'
import './StoriesSection.css'

function chunk(items, size) {
  const rows = []
  for (let i = 0; i < items.length; i += size) {
    rows.push(items.slice(i, i + size))
  }
  return rows
}

function StoryCard({ item, side }) {
  return (
    <article className={`home-stories__card home-stories__card--${side}`}>
      <div className="home-stories__card-inner">
        {item.image ? (
          <img src={item.image} alt="" className="home-stories__photo" />
        ) : (
          <div className="home-stories__photo" aria-hidden="true" />
        )}
        <div className="home-stories__copy">
          <h3>{item.title}</h3>
          <p>{item.excerpt || LOREM_SHORT}</p>
        </div>
        <Link to={item.path} className="home-stories__link">
          Read More
          <img
            className="home-stories__link-icon"
            src={readMoreArrow}
            alt=""
            aria-hidden="true"
          />
        </Link>
      </div>
    </article>
  )
}

export default function StoriesSection({
  items = defaultStories,
  title = 'What’s Happening at GSM',
  lede = LOREM,
  moreTo,
  moreLabel,
  align = 'start',
}) {
  const rows = chunk(items, 2)

  return (
    <section className="home-stories" aria-label="Stories">
      <div className="home-stories__inner">
        <header className={`home-stories__header${align === 'center' ? ' home-stories__header--center' : ''}`}>
          <div className="home-stories__intro">
            <h2>{title}</h2>
            <p>{lede}</p>
          </div>
          {moreTo && (
            <Link to={moreTo} className="home-stories__more">
              {moreLabel}
            </Link>
          )}
        </header>

        <div className="home-stories__rows">
          {rows.map((row) => (
            <div className="home-stories__cards" key={row.map((item) => item.path).join('-')}>
              {row.map((item, index) => (
                <StoryCard
                  item={item}
                  key={item.path}
                  side={index === 0 ? 'left' : 'right'}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
