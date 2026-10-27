import { Link } from 'react-router-dom'
import FormStatus from '../components/FormStatus'
import PageHero from '../components/PageHero'
import { useFormSubmit } from '../lib/forms'
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
  const contactForm = useFormSubmit()
  const thankForm = useFormSubmit()

  return (
    <article className="contact-page">
      <PageHero
        align="left"
        crumbs={[{ label: 'Contact' }]}
        title="Contact Us"
        lede="Have a question about Good Shepherd Manor, our services or ways to get involved? Connect with our team to learn more, thank a staff member or find the information you need. We’d love to hear from you!"
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
            <p className="contact-bar__label">Need Assistance?</p>
            <p className="contact-bar__value">
              <a href="#thank">Our Team Is Here to Help</a>
            </p>
          </article>
        </div>
      </section>

      <section className="contact-touch" id="visit">
        <div className="contact-touch__inner">
          <div className="contact-touch__copy">
            <p className="contact-touch__eyebrow">Get in touch</p>
            <h2>How can we help you?</h2>
            <p>
              Whether you’re exploring care for a loved one, sharing feedback or recognizing someone who made a difference, we’re here to listen and help you take the next step.
            </p>

            <div className="contact-offices" id="staff">
              <div className="contact-office">
                <h3>Main Office</h3>
                <p>(815) 472-3700</p>
                <p>4129 N. State Route 1-17, Momence, IL 60954</p>
                <p>P.O. Box 260, Momence, IL 60954</p>
              </div>
              <div className="contact-office">
                <h3>Careers</h3>
                <Link to="/careers" className="contact-office__link">
                  View openings →
                </Link>
              </div>
            </div>

            <div className="contact-follow">
              <h3>Follow us on:</h3>
              <a
                className="contact-follow__link"
                href={FACEBOOK}
                target="_blank"
                rel="noreferrer"
              >
                <img src={facebookIcon} alt="" aria-hidden="true" />
                Facebook
              </a>
              <a
                className="contact-follow__link"
                href={FACEBOOK}
                target="_blank"
                rel="noreferrer"
              >
                Instagram
              </a>
              <a
                className="contact-follow__link"
                href={FACEBOOK}
                target="_blank"
                rel="noreferrer"
              >
                LinkedIn
              </a>
            </div>
          </div>

          <form className="contact-form" onSubmit={contactForm.handleSubmit}>
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
            <button
              type="submit"
              className="btn btn--primary"
              disabled={contactForm.status === 'submitting'}
            >
              {contactForm.status === 'submitting' ? 'Sending…' : 'Send Message'}
            </button>
            <FormStatus {...contactForm} />
          </form>
        </div>
      </section>

      <section className="contact-map" aria-label="Map">
        <div className="contact-map__photo" aria-hidden="true" />
        <div className="contact-map__copy">
          <p className="contact-map__eyebrow">Our Location</p>
          <h2>
            <a href="https://maps.google.com/?q=4129+N.+State+Route+1-17,+Momence,+IL+60954" target="_blank" rel="noreferrer">
              Rooted in Momence. Connected by Care.
            </a>
          </h2>
        </div>
      </section>

      <section className="contact-touch contact-touch--thank" id="thank">
        <div className="contact-touch__inner">
          <div className="contact-touch__copy">
            <p className="contact-touch__eyebrow">THANK A STAFF MEMBER</p>
            <h2>Make Their Day</h2>
            <p>
              Has a GSM staff member made a difference? Share your appreciation and let them know how much their kindness and dedication mean to you.
            </p>
          </div>
          <form className="contact-form" onSubmit={thankForm.handleSubmit}>
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
            <button
              type="submit"
              className="btn btn--primary"
              disabled={thankForm.status === 'submitting'}
            >
              {thankForm.status === 'submitting' ? 'Sending…' : 'Send thanks'}
            </button>
            <FormStatus {...thankForm} />
          </form>
        </div>
      </section>
    </article>
  )
}

export default ContactPage
