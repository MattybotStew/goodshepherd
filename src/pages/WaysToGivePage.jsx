import { Link } from 'react-router-dom'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function WaysToGivePage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Support GSM', to: '/support-gsm' }, { label: 'Ways to Give' }]}
        title="Ways to Give"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="involved" />

      <div className="page-body">
        <section className="rte">
          <h2>Every gift stays on campus</h2>
          <p>{LOREM_LONG}</p>
          <p>{LOREM}</p>
        </section>

        <section className="rte">
          <h2>One-time gift</h2>
          <p>{LOREM}</p>
        </section>

        <section className="rte">
          <h2>Monthly giving</h2>
          <p>{LOREM}</p>
        </section>

        <section className="rte">
          <h2>Planned &amp; memorial gifts</h2>
          <p>{LOREM}</p>
          <Link to="/shepherd-endowment-society" className="text-link">
            Shepherd Endowment Society
          </Link>
        </section>
      </div>
    </article>
  )
}

export default WaysToGivePage
