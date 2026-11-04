import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SectionTabs from '../components/SectionTabs'
import SplitSection from '../components/SplitSection'
import { foundationIntroColumns, getInvolvedSections } from '../data/getInvolved'
import '../styles/starter.css'

function FoundationPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Support GSM' }]}
        title="GSM Foundation"
        lede="Founded in 1981, GSM’s Foundation has provided continual support for the programs, services and operating costs of the Manor, allowing us to go above and beyond what the state mandates and provides."
      />

      {/* Numbered cards — 01 Donate / 02 Volunteer / 03 Make A Lasting Impact */}
      <HomeIntroStrip variant="involved" columns={foundationIntroColumns} />

      {/* Jump bar — tabs scroll to the stacked anchor sections below */}
      <SectionTabs sections={getInvolvedSections} />

      {getInvolvedSections.map((section) => (
        <SplitSection
          key={section.id}
          id={section.id}
          eyebrow={section.eyebrow}
          title={section.title}
          flip={section.flip}
          imageSrc={section.imageSrc}
          imageAlt={section.imageAlt}
          linkTo={section.linkTo}
          linkLabel={section.linkLabel}
        >
          {section.paragraphs.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
          {section.listItems && (
            <ul>
              {section.listItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          )}
        </SplitSection>
      ))}
    </article>
  )
}

export default FoundationPage
