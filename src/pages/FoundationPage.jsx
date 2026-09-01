import PageHero from '../components/PageHero'
import SectionTabs from '../components/SectionTabs'
import SplitSection from '../components/SplitSection'
import { getInvolvedSections } from '../data/getInvolved'
import { LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function FoundationPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Support GSM' }]}
        title="Support GSM Foundation"
        lede={LOREM_LONG}
      />

      {/* Jump bar — tabs scroll to the stacked anchor sections below */}
      <SectionTabs sections={getInvolvedSections} />

      {getInvolvedSections.map((section) => (
        <SplitSection
          key={section.id}
          id={section.id}
          eyebrow={section.eyebrow}
          title={section.title}
          flip={section.flip}
          softImage={section.softImage}
          linkTo={section.linkTo}
          linkLabel={section.linkLabel}
        >
          {section.paragraphs.map((paragraph) => (
            <p key={paragraph.slice(0, 32)}>{paragraph}</p>
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
