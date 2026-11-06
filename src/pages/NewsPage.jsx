import DonateCta from '../components/DonateCta'
import ImpactSection from '../components/ImpactSection'
import PageHero from '../components/PageHero'
import StoriesSection from '../components/StoriesSection'
import { newsItems } from '../data/site'

const newsImpactStats = [
  { value: '55', label: 'Years serving our community' },
  { value: '100+', label: 'Men supported daily' },
  { value: '2', label: 'Core programs offered' },
  { value: '1971', label: 'Founded in Momence, IL' },
]

function NewsPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'News & Updates' }]}
        title="News & Updates"
        lede="Stay connected with the men and life at GSM. Find latest updates, event news, and stories from our community, along with The Messenger, our twice-yearly newsletter celebrating the people of the Manor."
      />

      <ImpactSection
        variant="stories"
        eyebrow="Our Impact"
        title="Helping men with disabilities thrive"
        lede="With compassionate care, welcoming homes, and meaningful opportunities, GSM helps each man build independence, form friendships, explore interests, and enjoy a life of dignity, purpose, and belonging."
        stats={newsImpactStats}
      />

      <DonateCta
        variant="split"
        title="Help Make Home Happen"
        lede="Give now to help men with disabilities have compassionate care, meaningful lives, and a home at GSM."
        ctaLabel="Donate Now"
        ctaTo="/support-gsm#ways-to-give"
      />

      <StoriesSection
        items={newsItems}
        title="What’s Happening at GSM"
        lede="See how the men of GSM are learning, connecting, and thriving. Explore the new stories, events, and everyday moments your support helps make possible."
        align="center"
      />
    </article>
  )
}

export default NewsPage
