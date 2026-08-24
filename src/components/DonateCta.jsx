import { Link } from 'react-router-dom'
import { LOREM } from '../data/placeholders'
import './DonateCta.css'

export default function DonateCta({ variant = 'center' }) {
  const split = variant === 'split'

  return (
    <section className={`home-donate-cta${split ? ' home-donate-cta--split' : ''}`}>
      <div className="home-donate-cta__inner">
        <div className="home-donate-cta__copy">
          <h2>We can create a better tomorrow</h2>
          <p>{LOREM}</p>
        </div>
        <Link
          to="/ways-to-give"
          className={split ? 'home-btn home-btn--white' : 'home-btn home-btn--blue'}
        >
          Donate Now
        </Link>
      </div>
    </section>
  )
}
