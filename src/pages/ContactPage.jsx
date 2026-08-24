import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function ContactPage() {
  function onSubmit(e) {
    e.preventDefault()
  }

  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Contact' }]}
        title="Contact Us"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="page" />

      <div className="page-body">
        <div className="form-grid">
          <form onSubmit={onSubmit} id="visit">
            <div className="rte">
              <h2>Send a message</h2>
              <p>{LOREM}</p>
            </div>
            <div className="field">
              <label htmlFor="name">Name</label>
              <input id="name" name="name" autoComplete="name" required />
            </div>
            <div className="field">
              <label htmlFor="email">Email</label>
              <input id="email" name="email" type="email" autoComplete="email" required />
            </div>
            <div className="field">
              <label htmlFor="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autoComplete="tel" />
            </div>
            <div className="field">
              <label htmlFor="reason">I am writing about</label>
              <select id="reason" name="reason" defaultValue="visit">
                <option value="visit">Schedule a visit</option>
                <option value="programs">Programs</option>
                <option value="jobs">Careers</option>
                <option value="give">Giving / Foundation</option>
                <option value="other">Something else</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="message">Message</label>
              <textarea id="message" name="message" required />
            </div>
            <button type="submit" className="btn btn--primary">Send</button>
          </form>

          <aside className="contact-aside">
            <h3>Good Shepherd Manor</h3>
            <p>
              (815) 472-3700<br />
              P.O. Box 260<br />
              4129 N. State Route 1-17<br />
              Momence, IL 60954
            </p>
            <h3>Hours</h3>
            <p>{LOREM}</p>
            <h3>Map</h3>
            <div className="map-ph" aria-label="Map placeholder" />
          </aside>
        </div>

        <section className="rte anchor" id="staff">
          <h2>Staff directory</h2>
          <ul className="rte-links">
            <li>
              <h3>Front office</h3>
              <p>{LOREM} (815) 472-3700</p>
            </li>
            <li>
              <h3>GSM Foundation</h3>
              <p>{LOREM}</p>
            </li>
            <li>
              <h3>Careers</h3>
              <p>{LOREM}</p>
            </li>
          </ul>
        </section>

        <section className="rte anchor" id="thank">
          <h2>Thank a staff member</h2>
          <p>{LOREM}</p>
          <form onSubmit={onSubmit}>
            <div className="field">
              <label htmlFor="thank-from">Your name</label>
              <input id="thank-from" name="from" required />
            </div>
            <div className="field">
              <label htmlFor="thank-staff">Staff member</label>
              <input id="thank-staff" name="staff" required />
            </div>
            <div className="field">
              <label htmlFor="thank-note">Note</label>
              <textarea id="thank-note" name="note" required />
            </div>
            <button type="submit" className="btn btn--primary">Send thanks</button>
          </form>
        </section>
      </div>
    </article>
  )
}

export default ContactPage
