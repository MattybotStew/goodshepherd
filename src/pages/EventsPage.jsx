import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

const events = [
  { id: 'fall-festival', title: 'Fall Festival', when: 'October 2026' },
  { id: 'brunch-auction', title: 'Brunch Auction', when: 'Spring' },
  { id: 'golf', title: 'Golf Invitational', when: 'Summer' },
  { id: 'family', title: 'Family Events', when: 'Year-round' },
]

function EventsPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Support GSM', to: '/support-gsm' }, { label: 'Events' }]}
        title="Events"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="involved" />

      <div className="page-body">
        {events.map((e) => (
          <section className="rte anchor" id={e.id} key={e.id}>
            <h2>{e.title}</h2>
            <p>{e.when}</p>
            <p>{LOREM_LONG}</p>
          </section>
        ))}
      </div>
    </article>
  )
}

export default EventsPage
