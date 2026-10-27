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

      {/* Partners (Complete) */}
      <AffiliationsSection
        eyebrow="Memberships"
        title="Member Organizations or Affiliations"
        description="GSM is a member of a variety of local professional and civic organizations, as well as statewide organizations such as the Kankakee & Momence Chamber of Commerce, Intersect For Ability, United Way of Kankakee County, Special Olympics & ARC of IL."
        links={[
          { label: 'ARC of Illinois', to: '#' },
          { label: 'Intersect For Ability', to: '#' },
        ]}
      />

      {/* Accessibility (Complete) */}
      <SplitSection
        id="accessibility"
        eyebrow="Accessibility Statement"
        title="Website Accessibility Statement"
        flip
        alt
        imageSrc={stockImages.accessibility}
        imageAlt="People working together at a laptop"
        linkTo="/contact"
        linkLabel="Contact Us for More Information"
      >
        <p>
          Good Shepherd Manor is committed to treating every person with dignity and respect. In keeping with our mission of providing high-quality, compassionate care to men with intellectual and developmental disabilities, we strive to make our website accessible and welcoming to people of all abilities.

          Our goal is to continually improve the accessibility and usability of our website so everyone can learn about our programs, access resources, and connect with our mission.
        </p>
        <p>
          If you experience difficulty accessing any part of our website or need information in an alternative format, please contact us at 815-472-3700 or info@goodshepherdmanor.org. Please include the page address and a brief description of the difficulty so we can better assist you.

          We welcome your feedback as we work toward a more accessible online experience.
        </p>
      </SplitSection>
    </article>
  )
}

export default AboutPage
