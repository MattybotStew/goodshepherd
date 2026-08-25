import { Link } from 'react-router-dom'
import { programs } from '../data/site'
import { LOREM, LOREM_SHORT } from '../data/placeholders'
import communityDayIcon from '../assets/programs/community-day.svg'
import vocationalIcon from '../assets/programs/vocational.svg'
import residentialIcon from '../assets/programs/residential.svg'
import healthIcon from '../assets/programs/health.svg'
import './ProgramsServicesSection.css'

const PROGRAM_ICONS = {
  '/programs/community-day-services': communityDayIcon,
  '/programs/vocational': vocationalIcon,
  '/programs/residential-living': residentialIcon,
  '/programs/health-well-being': healthIcon,
}

export default function ProgramsServicesSection({ showViewAll = true }) {
  return (
    <section className="programs-services">
      <div className="programs-services__container">
        <div className="programs-services__header">
          <div className="programs-services__intro">
            <h2>Our Programs &amp; Services</h2>
            <p>{LOREM}</p>
          </div>
          {showViewAll && (
            <Link to="/programs" className="programs-services__more">
              View all programs &rarr;
            </Link>
          )}
        </div>
        <div className="programs-services__grid">
          {programs.map((p) => (
            <article className="programs-services__card" key={p.path}>
              <div className="programs-services__icon" aria-hidden="true">
                {PROGRAM_ICONS[p.path] && (
                  <img src={PROGRAM_ICONS[p.path]} alt="" />
                )}
              </div>
              <h3>{p.homeName || p.name}</h3>
              <p>{LOREM_SHORT}</p>
              <Link to={p.path} className="programs-services__link">
                Learn more &rarr;
              </Link>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
