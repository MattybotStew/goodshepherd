import AboutMissionSection from '../components/AboutMissionSection'
import AffiliationsSection from '../components/AffiliationsSection'
import HistoryTimelineSection from '../components/HistoryTimelineSection'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SplitSection from '../components/SplitSection'
import { lifeImages } from '../data/lifeImages'
import { stockImages } from '../data/stockImages'
import { LOREM } from '../data/placeholders'
import '../styles/starter.css'

/**
 * About Us — copy per client content matrix (2026-10).
 * Complete items are final production copy. Items still Assigned/In-Progress
 * render lorem + placeholder images and are flagged with TODO comments and
 * data-status attributes so they are easy to find.
 */
function AboutPage() {
  return (
    <article>
      {/* Hero (Complete) */}
      <PageHero
        align="left"
        crumbs={[{ label: 'About Us' }]}
        title="About Us"
        lede="Since 1971, Good Shepherd Manor has offered men with disabilities compassionate care, purpose, and a place to call home."
        photo={lifeImages.aboutHero}
      />

      {/* About Us Overview (Complete) — mosaic uses real GSM campus photos */}
      <AboutMissionSection
        showReadMore={false}
        overlapHero
        compactBottom
        eyebrow="About Us"
        title="A community of care, growth, and dignity for over 55 years."
        paragraphs={[
          'Rooted in compassion, we help men with disabilities lead meaningful lives through personalized support, lasting friendships and opportunities to grow.',
          'Our welcoming homes and dedicated staff create a family atmosphere where each man receives personalized support, builds daily living skills, and enjoys meaningful connections on campus and in the surrounding community.',
        ]}
        mosaicImages={lifeImages.aboutMosaic}
        mosaicAlts={[
          'A man working at a workbench in the GSM campus workshop',
          'Men preparing a meal together in a GSM group home kitchen',
          'A man tending plants in the GSM campus garden',
          'Men relaxing together on the porch of a GSM group home',
        ]}
      />

      {/* Feature Cards (Complete) — 01 Programs & Services / 02 Get Involved / 03 News You Can Use */}
      <HomeIntroStrip variant="about" />

      {/* Mission (Why We Exist) (Complete)
          TODO: Mission image pending (status: In-Progress) — SplitSection soft placeholder below */}
      <SplitSection
        id="mission"
        eyebrow="Who We Are"
        title="The Heart of Our Mission"
        imageSrc={lifeImages.aboutMission}
        imageAlt="Men from Good Shepherd Manor gathered together outdoors"
      >
        <p data-status="complete">
          Our Mission is to serve men with intellectual and developmental
          disabilities by providing high quality &amp; compassionate care. Our
          vision is to meet individual needs, build individual abilities, and
          make each day meaningful and rewarding.
        </p>
        <p data-status="complete">
          Our Values are guided by our legacy of compassion, honoring each
          man's dignity and envisioning a community where all feel valued,
          supported and truly at home.
        </p>
      </SplitSection>

      {/* Timeline (Complete) — decades as H3s, data in src/data/history.js */}
      <HistoryTimelineSection eyebrow="Our History" title="A Timeline of Care" />

      {/* Partners
          TODO: Partner paragraph needs final copy (status: Assigned) — lorem below
          TODO: Partner feature image needed (status: Assigned) — SplitSection placeholder right
          TODO: Brothers of Good Shepherd destination pending (status: Assigned) */}
      <AffiliationsSection
        eyebrow="Affiliations"
        title="Partners in care"
        description={LOREM}
        links={[
          { label: 'Brothers of Good Shepherd', to: '#' },
          { label: 'Special Olympics', to: '/programs/special-olympics' },
        ]}
      />

      {/* Accessibility
          TODO: Accessibility paragraph 1 needs copy (status: Assigned) — lorem below
          TODO: Accessibility paragraph 2 needs copy (status: Assigned) — lorem below
          TODO: Accessibility graphic needed (status: Assigned) — SplitSection soft placeholder right */}
      <SplitSection
        id="accessibility"
        eyebrow="Accessibility Statement"
        title="This site should work for everyone"
        flip
        alt
        imageSrc={stockImages.accessibility}
        imageAlt="People working together at a laptop"
        linkTo="/contact"
        linkLabel="Contact us about accessibility"
      >
        <p data-status="assigned">{LOREM}</p>
        <p data-status="assigned">{LOREM}</p>
      </SplitSection>
    </article>
  )
}

export default AboutPage
