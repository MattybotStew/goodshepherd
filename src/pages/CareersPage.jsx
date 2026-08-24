import { Link } from 'react-router-dom'
import AboutMissionSection from '../components/AboutMissionSection'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SplitSection from '../components/SplitSection'
import { jobs } from '../data/site'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function CareersPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'Careers' }]}
        title="Careers"
        lede={LOREM_LONG}
      />

      {/* Intro / culture — mirrors About's mission section */}
      <AboutMissionSection
        showReadMore={false}
        overlapHero
        compactBottom
        placeholderCopy
        eyebrow="Careers at Good Shepherd Manor"
        title="Build a career with purpose"
      />

      <HomeIntroStrip variant="page" />

      {/* Benefits */}
      <SplitSection id="benefits" eyebrow="Benefits" title="Rewards that support you">
        <p>{LOREM_LONG}</p>
        <p>{LOREM}</p>
        <ul>
          <li>Lorem ipsum dolor sit amet</li>
          <li>Consectetur adipiscing elit sed do eiusmod</li>
          <li>Tempor incididunt ut labore et dolore</li>
          <li>Magna aliqua ut enim ad minim veniam</li>
        </ul>
      </SplitSection>

      {/* Culture */}
      <SplitSection
        id="culture"
        eyebrow="Our Culture"
        title="A workplace that cares"
        flip
        alt
        softImage
      >
        <p>{LOREM_LONG}</p>
        <p>{LOREM}</p>
      </SplitSection>

      {/* Job openings */}
      <SplitSection id="openings" eyebrow="Job Openings" title="Join our team">
        <p>{LOREM}</p>
        <ul className="rte-links">
          {jobs.map((job, i) => (
            <li key={`${job.title}-${job.type}-${i}`}>
              <h3>{job.title}</h3>
              <p>
                {job.type}. {job.note}
              </p>
              <Link to="/contact" className="text-link">
                Apply for {job.title}
              </Link>
            </li>
          ))}
        </ul>
      </SplitSection>

      {/* Closing CTA */}
      <SplitSection
        id="apply"
        eyebrow="Apply Today"
        title="Ready to make a difference?"
        alt
        softImage
        linkTo="/contact"
        linkLabel="Contact us to apply →"
      >
        <p>{LOREM_LONG}</p>
        <p>{LOREM}</p>
      </SplitSection>
    </article>
  )
}

export default CareersPage

