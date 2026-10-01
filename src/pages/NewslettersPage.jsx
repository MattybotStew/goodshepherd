import FormStatus from '../components/FormStatus'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { useFormSubmit } from '../lib/forms'
import { LOREM, LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

const issues = [
  { date: 'Summer 2026', title: 'Summer family update' },
  { date: 'Spring 2026', title: 'Spring family update' },
  { date: 'Winter 2025', title: 'Winter family update' },
]

function NewslettersPage() {
  const signupForm = useFormSubmit()

  return (
    <article>
      <PageHero
        crumbs={[{ label: 'News', to: '/news' }, { label: 'Newsletters' }]}
        title="Newsletters & Family Resources"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="page" />

      <div className="page-body">
        <section className="rte">
          <h2>Stay in the loop</h2>
          <p>{LOREM}</p>
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
          <h2>Past issues</h2>
          <ul className="rte-links">
            {issues.map((issue) => (
              <li key={issue.title}>
                <h3>{issue.title}</h3>
                <p>{issue.date}. {LOREM}</p>
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
