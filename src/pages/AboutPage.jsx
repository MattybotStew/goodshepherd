import AboutMissionSection from '../components/AboutMissionSection'
import AffiliationsSection from '../components/AffiliationsSection'
import HistoryTimelineSection from '../components/HistoryTimelineSection'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SplitSection from '../components/SplitSection'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function AboutPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'About Us' }]}
        title="About Us"
        lede="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi."
      />

      <AboutMissionSection showReadMore={false} overlapHero compactBottom placeholderCopy />

      <HomeIntroStrip variant="about" />

      <SplitSection id="mission" eyebrow="Mission, Vision & Values" title="Why we exist">
        <p>{LOREM_LONG}</p>
        <p>{LOREM}</p>
      </SplitSection>

      <HistoryTimelineSection />

      <AffiliationsSection />

      <SplitSection
        id="accessibility"
        eyebrow="Accessibility Statement"
        title="This site should work for everyone"
        flip
        alt
        softImage
        linkTo="/contact"
        linkLabel="Contact us about accessibility →"
      >
        <p>{LOREM}</p>
        <p>{LOREM}</p>
      </SplitSection>
    </article>
  )
}

export default AboutPage
