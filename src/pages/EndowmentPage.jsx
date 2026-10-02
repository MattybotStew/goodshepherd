import { Link } from 'react-router-dom'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import SplitSection from '../components/SplitSection'
import {
  currentGifts,
  deferredGifts,
  endowmentDisbursement,
  endowmentIntro,
  endowmentQuote,
  giftOptionsIntro,
  membershipIntro,
  membershipLevels,
  membershipOutro,
} from '../data/endowment'
import '../styles/starter.css'

function EndowmentPage() {
  return (
    <article>
      <PageHero
        crumbs={[
          { label: 'Support GSM', to: '/support-gsm' },
          { label: 'Shepherd Endowment Society' },
        ]}
        title="Shepherd Endowment Society"
        lede="Stewardship that outlives a gift"
      />

      <HomeIntroStrip variant="involved" />

      <SplitSection
        id="overview"
        eyebrow="Shepherd Endowment Society"
        title="Income for the Manor, in perpetuity"
      >
        {endowmentIntro.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
        <p>{endowmentDisbursement}</p>
      </SplitSection>

      <div className="page-body">
        <section className="rte">
          <blockquote>
            <p>&ldquo;{endowmentQuote.text}&rdquo;</p>
            <cite>{endowmentQuote.cite}</cite>
          </blockquote>
        </section>

        <section className="rte anchor" id="gift-options">
          <h2>So How Can You Ensure More Tomorrows?</h2>
          {giftOptionsIntro.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
          <div className="rte-grid">
            <div>
              <h3>Current Gifts</h3>
              <ul>
                {currentGifts.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3>Deferred Gifts</h3>
              <ul>
                {deferredGifts.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="rte anchor" id="membership">
          <h2>Membership</h2>
          <p>{membershipIntro}</p>
          <table className="rte-table">
            <thead>
              <tr>
                <th scope="col">Member Levels</th>
                <th scope="col">Current Gift</th>
                <th scope="col">Deferred Gift</th>
              </tr>
            </thead>
            <tbody>
              {membershipLevels.map((row) => (
                <tr key={row.level}>
                  <th scope="row">{row.level}</th>
                  <td>{row.current}</td>
                  <td>{row.deferred}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p>{membershipOutro}</p>
          <Link to="/contact" className="text-link">
            Ask about joining &rarr;
          </Link>
        </section>
      </div>
    </article>
  )
}

export default EndowmentPage
