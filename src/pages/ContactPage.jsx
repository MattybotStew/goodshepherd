import { Link } from 'react-router-dom'
import PageHero from '../components/PageHero'
import facebookIcon from '../assets/footer/facebook.svg'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'
import './ContactPage.css'

const PHONE = '(815) 472-3700'
const FACEBOOK = 'https://www.facebook.com/goodshepherdmanormomence/'

const STAFF = [
  {
    title: 'Front office',
    lines: [PHONE, '4129 N. State Route 1-17', 'Momence, IL 60954'],
  },
  {
    title: 'GSM Foundation',
    lines: ['P.O. Box 260', 'Momence, IL 60954'],
  },
  {
    title: 'Careers',
    lines: [PHONE],
    linkTo: '/careers',
    linkLabel: 'View openings →',
  },
]

function ContactPage() {
  function onSubmit(event) {
    event.preventDefault()
  }

  return (
    <article className="contact-page">
      <PageHero
        align="left"
        crumbs={[{ label: 'Contact' }]}
        title="Contact Us"
        lede={LOREM_LONG}
      />

      <section className="contact-bar" aria-label="Contact details">
        <div className="contact-bar__card">
          <article className="contact-bar__col">
            <p className="contact-bar__label">Phone</p>
            <p className="contact-bar__value">
              Tel:{' '}
              <a href="tel:+18154723700">{PHONE}</a>
            </p>
          </article>
          <article className="contact-bar__col">
            <p className="contact-bar__label">Campus</p>
            <p className="contact-bar__value">
              P.O. Box 260<br />
              4129 N. State Route 1-17<br />
              Momence, IL 60954
            </p>
          </article>
          <article className="contact-bar__col">
            <p className="contact-bar__label">Need assistance?</p>
            <p className="contact-bar__value">
              <a href="#thank">Thank a staff member</a>
            </p>
          </article>
        </div>
      </section>

      <section className="contact-touch" id="visit">
        <div className="contact-touch__inner">
          <div className="contact-touch__copy">
            <p className="contact-touch__eyebrow">Get in touch</p>
            <h2>How can we help you?</h2>
            <p>{LOREM_LONG}</p>

            <div className="contact-offices" id="staff">
              {STAFF.map((office) => (
                <div className="contact-office" key={office.title}>
                  <h3>{office.title}</h3>
                  {office.lines.map((line) => (
                    <p key={line}>{line}</p>
                  ))}
                  {office.linkTo && (
                    <Link to={office.linkTo} className="contact-office__link">
                      {office.linkLabel}
                    </Link>
                  )}
                </div>
              ))}
            </div>

            <div className="contact-follow">
              <h3>Follow us on</h3>
              <a
                className="contact-follow__link"
                href={FACEBOOK}
                target="_blank"
                rel="noreferrer"
              >
                <img src={facebookIcon} alt="" aria-hidden="true" />
                Facebook
              </a>
            </div>
          </div>

          <form className="contact-form" onSubmit={onSubmit}>
            <div className="contact-field">
              <label htmlFor="name">
                Full Name <span aria-hidden="true">*</span>
              </label>
              <input id="name" name="name" autoComplete="name" required />
            </div>
            <div className="contact-field">
              <label htmlFor="email">
                Email <span aria-hidden="true">*</span>
              </label>
              <input id="email" name="email" type="email" autoComplete="email" required />
            </div>
            <div className="contact-field">
              <label htmlFor="subject">
                Subject <span aria-hidden="true">*</span>
              </label>
              <input id="subject" name="subject" required />
            </div>
            <div className="contact-field">
              <label htmlFor="message">Message</label>
              <textarea id="message" name="message" />
            </div>
            <button type="submit" className="btn btn--primary">
              Send Message
            </button>
          </form>
        </div>
      </section>

      <section className="contact-map" aria-label="Map">
        <div className="contact-map__photo" aria-hidden="true" />
        <div className="contact-map__copy">
          <p className="contact-map__eyebrow">Where we work</p>
          <h2>A community of care in Momence, Illinois.</h2>
        </div>
      </section>

      <section className="contact-touch contact-touch--thank" id="thank">
        <div className="contact-touch__inner">
          <div className="contact-touch__copy">
            <p className="contact-touch__eyebrow">Thank a staff member</p>
            <h2>Say thank you</h2>
            <p>{LOREM}</p>
          </div>
          <form className="contact-form" onSubmit={onSubmit}>
            <div className="contact-field">
              <label htmlFor="thank-from">
                Your name <span aria-hidden="true">*</span>
              </label>
              <input id="thank-from" name="from" required />
            </div>
            <div className="contact-field">
              <label htmlFor="thank-staff">
                Staff member <span aria-hidden="true">*</span>
              </label>
              <input id="thank-staff" name="staff" required />
            </div>
            <div className="contact-field">
              <label htmlFor="thank-note">
                Note <span aria-hidden="true">*</span>
              </label>
              <textarea id="thank-note" name="note" required />
            </div>
            <button type="submit" className="btn btn--primary">
              Send thanks
            </button>
          </form>
        </div>
      </section>
    </article>
  )
}

export default ContactPage
