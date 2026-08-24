import { impactStats } from '../data/site'
import { LOREM_LONG } from '../data/placeholders'
import './ImpactSection.css'

export default function ImpactSection({
  variant = 'home',
  eyebrow,
  title = 'Our Mission & Vision: Serving with Dignity',
}) {
  const stories = variant === 'stories'

  return (
    <section className={`home-impact${stories ? ' home-impact--stories' : ''}`}>
      <div className="home-impact__container">
        <div className="home-impact__intro">
          {stories ? (
            <div className="home-impact__header home-impact__header--stories">
              <p className="home-impact__label">{eyebrow || 'Our Impact'}</p>
              <div className="home-impact__col">
                <h2>{title}</h2>
                <p>{LOREM_LONG}</p>
              </div>
            </div>
          ) : (
            <div className="home-impact__header">
              <div className="home-impact__col">
                <h2>{title}</h2>
              </div>
              <div className="home-impact__col">
                <p>{LOREM_LONG}</p>
              </div>
            </div>
          )}
        </div>

        {stories && (
          <div className="home-impact__mosaic" aria-hidden="true">
            <div className="home-impact__ph home-impact__ph--wide" />
            <div className="home-impact__ph home-impact__ph--tall" />
            <div className="home-impact__ph home-impact__ph--tall" />
          </div>
        )}

        <div className="home-impact__stats">
          {impactStats.map((stat, idx) => (
            <div className="home-impact__stat" key={idx}>
              <p className="home-impact__value">{stat.value}</p>
              <p className="home-impact__stat-label">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
