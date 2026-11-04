import { Link } from 'react-router-dom'
import AboutMissionSection from '../components/AboutMissionSection'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SplitSection from '../components/SplitSection'
import {
  careersApply,
  careersBenefits,
  careersCulture,
  careersIntro,
  careersIntroColumns,
  careersJobs,
  careersOpenings,
} from '../data/careers'
import { stockImages } from '../data/stockImages'
import '../styles/starter.css'

function CareersPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'Careers' }]}
        title="Careers"
        lede="Build a career with purpose at Good Shepherd Manor. Join a caring team that supports men with intellectual and developmental disabilities in living full, meaningful lives."
      />

      {/* Intro / culture — mirrors About's mission section */}
      <AboutMissionSection
        showReadMore={false}
        overlapHero
        compactBottom
        eyebrow={careersIntro.eyebrow}
        title={careersIntro.title}
        paragraphs={careersIntro.paragraphs}
        mosaicImages={stockImages.careersMosaic}
      />

      <HomeIntroStrip variant="page" columns={careersIntroColumns} />

      {/* Benefits */}
      <SplitSection
        id={careersBenefits.id}
        eyebrow={careersBenefits.eyebrow}
        title={careersBenefits.title}
        imageSrc={stockImages.careers}
        imageAlt="Coworkers talking together in a bright office"
      >
        {careersBenefits.paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
        <ul>
          {careersBenefits.listItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </SplitSection>

      {/* Culture */}
      <SplitSection
        id={careersCulture.id}
        eyebrow={careersCulture.eyebrow}
        title={careersCulture.title}
        flip
        alt
        imageSrc={stockImages.culture}
        imageAlt="A team collaborating around a table"
      >
        {careersCulture.paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </SplitSection>

      {/* Job openings */}
      <SplitSection
        id={careersOpenings.id}
        eyebrow={careersOpenings.eyebrow}
        title={careersOpenings.title}
        imageSrc={stockImages.openings}
        imageAlt="Staff meeting in a workplace"
      >
        <p>{careersOpenings.lede}</p>
        <ul className="rte-links">
          {careersJobs.map((job) => (
            <li key={job.title}>
              <h3>{job.title}</h3>
              <p>{job.body}</p>
              <Link to={job.applyTo} className="text-link">
                {job.applyLabel}
              </Link>
            </li>
          ))}
        </ul>
        <p>
          Apply online at{' '}
          <a
            href={careersOpenings.indeedUrl}
            target="_blank"
            rel="noreferrer"
            className="text-link"
          >
            Indeed.com
          </a>
          , or call or text{' '}
          <a href={careersOpenings.phoneHref} className="text-link">
            {careersOpenings.phone}
          </a>
          .
        </p>
      </SplitSection>

      {/* Closing CTA */}
      <SplitSection
        id={careersApply.id}
        eyebrow={careersApply.eyebrow}
        title={careersApply.title}
        alt
        imageSrc={stockImages.apply}
        imageAlt="Colleagues walking and talking together"
        linkTo={careersApply.linkTo}
        linkLabel={careersApply.linkLabel}
      >
        {careersApply.paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </SplitSection>
    </article>
  )
}

export default CareersPage
