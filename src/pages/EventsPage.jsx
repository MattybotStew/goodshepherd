import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { eventsIntroColumns } from '../data/getInvolved'
import '../styles/starter.css'

const events = [
  {
    id: 'fall-festival',
    title: 'Fall Festival',
    when: 'September 2027',
    body: 'Join us on the second Saturday of September for GSM’s beloved 36th Annual Fall Festival! Enjoy food, bingo, entertainment, and family fun for everyone while supporting the mission of the Manor.',
  },
  {
    id: 'golf',
    title: 'Golf Invitational',
    when: 'June 28, 2027',
    body: 'Tee off for a great cause at GSM’s 31st Annual Golf Invitational! Enjoy a day of golf, food, and camaraderie while raising funds for compassionate care and meaningful opportunities for the men of Good Shepherd Manor. Join us on the course to do good.',
  },
  {
    id: 'brunch-auction',
    title: 'Brunch Auction',
    when: 'April 18, 2027',
    body: 'Join GSM’s 52nd Brunch Auction for live & silent auctions, & Meet A Manor Need - which funds a specific need for the men. Past MAMN’s include the Digital Den, CHAIR the Love and a paratransit vehicle. This event makes such an impact on GSM’s mission!',
  },
  {
    id: 'family',
    title: 'Community & Family Events',
    when: 'All Year',
    body: 'Building community at GSM! Enjoy free events: the 5th Annual Touch A Truck on October 2, Twelfth Night Bonfire in early January 2027, and summer Community Movie Nights. Our monthly summer Friends & Family cookouts offer extra ways to connect.',
  },
]

function EventsPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'Support GSM', to: '/support-gsm' }, { label: 'Events' }]}
        title="Events"
        lede="GSM’s events raise funds to bridge the gap between state funding and the care the men need. They bring people together, introduce our mission to new supporters, and build lasting relationships that sustain the Foundation’s work and enrich daily life."
      />

      {/* Numbered cards — 01 Donate / 02 Volunteer / 03 Make A Lasting Impact */}
      <HomeIntroStrip variant="involved" columns={eventsIntroColumns} />

      <div className="page-body">
        {events.map((e) => (
          <section className="rte anchor" id={e.id} key={e.id}>
            <h2>{e.title}</h2>
            <p>{e.when}</p>
            <p>{e.body}</p>
          </section>
        ))}
      </div>
    </article>
  )
}

export default EventsPage
