import { Link } from 'react-router-dom'
import ctaPhoto from '../assets/theme04/home-bg.jpg'
import './GetInvolvedCta.css'

const PATHWAYS = [
  {
    title: 'Donate',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.',
    linkLabel: 'Give now \u2192',
    path: '/ways-to-give',
  },
  {
    title: 'Volunteer',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.',
    linkLabel: 'Get involved \u2192',
    path: '/events',
  },
  {
    title: 'Careers',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.',
    linkLabel: 'View openings \u2192',
    path: '/careers',
  },
]

export default function GetInvolvedCta() {
  return (
    <section className="global-cta" aria-labelledby="global-cta-heading">
      <div
        className="global-cta__inner"
        style={{ '--cta-photo': `url(${ctaPhoto})` }}
      >
        <header className="global-cta__header">
          <h2 id="global-cta-heading">Get Involved</h2>
        </header>
        <div className="global-cta__grid">
          {PATHWAYS.map((item) => (
            <Link key={item.path} to={item.path} className="global-cta__card">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <span className="global-cta__link">{item.linkLabel}</span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
