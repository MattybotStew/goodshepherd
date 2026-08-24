import { affiliations } from '../data/site'
import { LOREM } from '../data/placeholders'
import SplitSection from './SplitSection'

export default function AffiliationsSection({
  id = 'affiliations',
  eyebrow = 'Affiliations',
  title = 'Partners in care',
  description = LOREM,
  names = affiliations,
}) {
  return (
    <SplitSection id={id} eyebrow={eyebrow} title={title}>
      <p>{description}</p>
      <div className="partners">
        {names.map((name) => (
          <span className="partner-pill" key={name}>
            {name}
          </span>
        ))}
      </div>
    </SplitSection>
  )
}
