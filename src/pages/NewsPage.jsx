import { Link } from 'react-router-dom'
import HomeIntroStrip from '../components/HomeIntroStrip'
import PageHero from '../components/PageHero'
import { newsItems } from '../data/site'
import { LOREM_LONG } from '../data/placeholders'
import '../styles/starter.css'

function NewsPage() {
  return (
    <article>
      <PageHero
        crumbs={[{ label: 'News' }]}
        title="News & Updates"
        lede={LOREM_LONG}
      />

      <HomeIntroStrip variant="page" />

      <div className="page-body">
        <section className="rte">
          <h2>What is happening at GSM</h2>
          <ul className="rte-links">
            {newsItems.map((item) => (
              <li key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.date} · {item.tag}</p>
                <p>{item.excerpt}</p>
                <Link to={item.path} className="text-link">
                  {item.title}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </article>
  )
}

export default NewsPage
