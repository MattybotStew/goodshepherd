import PageHero from '../components/PageHero'
import ProgramsIntroSection from '../components/ProgramsIntroSection'
import ProgramsServicesSection from '../components/ProgramsServicesSection'
import { LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function ProgramsPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'Programs & Services' }]}
        title="Programs & Services"
        lede="From welcoming homes and engaging day programs to personalized health and wellness support, we help each man build skills, explore interests, form friendships, and enjoy a meaningful, fulfilling life."
      />

      <ProgramsIntroSection />

      <ProgramsServicesSection showViewAll={false} />
    </article>
  )
}

export default ProgramsPage
