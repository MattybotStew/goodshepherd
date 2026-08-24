import DonateCta from '../components/DonateCta'
import ImpactSection from '../components/ImpactSection'
import PageHero from '../components/PageHero'
import StoriesSection from '../components/StoriesSection'
import { newsItems } from '../data/site'
import { LOREM_LONG } from '../data/placeholders'

function NewsPage() {
  return (
    <article>
      <PageHero
        align="left"
        crumbs={[{ label: 'News' }]}
        title="News & Updates"
        lede={LOREM_LONG}
      />

      <ImpactSection
        variant="stories"
        title="The impact we have made in our community"
      />

      <DonateCta variant="split" />

      <StoriesSection
        items={newsItems}
        title="What’s Happening at GSM"
        align="center"
      />
    </article>
  )
}

export default NewsPage
