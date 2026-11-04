import { Link } from 'react-router-dom'
import { LOREM } from '../data/placeholders'
import { lifeImages } from '../data/lifeImages'
import './DonateCta.css'

export default function DonateCta({
  variant = 'center',
  title = 'We can create a better tomorrow',
  lede = LOREM,
  ctaLabel = 'Support GSM',
  ctaTo = '/support-gsm',
}) {
  const split = variant === 'split'

  return (
    <section className={`home-donate-cta${split ? ' home-donate-cta--split' : ''}`}>
      <div
        className="home-donate-cta__inner"
        style={{ '--cta-photo': `url(${lifeImages.donate})` }}
      >
        <div className="home-donate-cta__copy">
          <h2>{title}</h2>
          {lede ? <p>{lede}</p> : null}
        </div>
        <Link to={ctaTo} className="home-btn home-btn--white">
          {ctaLabel}
        </Link>
      </div>
    </section>
  )
}
