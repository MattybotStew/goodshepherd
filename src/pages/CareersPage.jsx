import { Link } from 'react-router-dom'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { jobs } from '../data/site'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function CareersPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Careers' }]}
        title="Careers"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="page" />

      <div className="page-body">
        <section className="rte">
          <h2>Benefits</h2>
          <p>{LOREM}</p>
          <ul>
            <li>Lorem ipsum dolor sit amet</li>
            <li>Consectetur adipiscing elit sed do eiusmod</li>
            <li>Tempor incididunt ut labore et dolore</li>
            <li>Magna aliqua ut enim ad minim veniam</li>
          </ul>
        </section>

        <section className="rte" id="openings">
          <h2>Job openings</h2>
          <ul className="rte-links">
            {jobs.map((job, i) => (
              <li key={`${job.title}-${job.type}-${i}`}>
                <h3>{job.title}</h3>
                <p>{job.type}. {job.note}</p>
                <Link to="/contact" className="text-link">
                  Apply for {job.title}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </article>
  )
}

export default CareersPage
