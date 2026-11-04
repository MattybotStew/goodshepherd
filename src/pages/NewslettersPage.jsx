import FormStatus from '../components/FormStatus'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { useFormSubmit } from '../lib/forms'
import '../styles/starter.css'

const ARCHIVE_DESCRIPTION =
  'Explore stories, photos, and updates celebrating the men of GSM and the community that helps them flourish.'

const issues = [
  { title: 'The Messenger Fall 2026' },
  { title: 'The Messenger Spring 2026' },
  { title: 'The Messenger Fall 2025' },
]

function NewslettersPage() {
  const signupForm = useFormSubmit()

  return (
    <article>
      <PageHero
        crumbs={[{ label: 'News', to: '/news' }, { label: 'Newsletters' }]}
        title="Newsletters & Family Resources"
        lede="Discover stories, photos and updates from life at GSM in The Messenger, our twice-yearly newsletter."
      />

      <HomeIntroStrip variant="page" />

      <div className="page-body">
        <section className="rte">
          <h2>Get The Messenger straight to your inbox</h2>
          <p>
            Discover stories, photos and updates from life at GSM in The Messenger, our
            twice-yearly newsletter.
          </p>
          <form onSubmit={signupForm.handleSubmit}>
            <div className="field">
              <label htmlFor="nl-email">Email address</label>
              <input id="nl-email" type="email" name="email" autoComplete="email" required />
            </div>
            <button
              type="submit"
              className="btn btn--primary"
              disabled={signupForm.status === 'submitting'}
            >
              {signupForm.status === 'submitting' ? 'Signing up…' : 'Sign up'}
            </button>
            <FormStatus {...signupForm} />
          </form>
        </section>

        <section className="rte">
          <h2>Recent Issues</h2>
          <ul className="rte-links">
            {issues.map((issue) => (
              <li key={issue.title}>
                <h3>{issue.title}</h3>
                <p>{ARCHIVE_DESCRIPTION}</p>
                <span className="text-link">PDF placeholder</span>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </article>
  )
}

export default NewslettersPage
