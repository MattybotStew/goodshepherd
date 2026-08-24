import { useParams } from 'react-router-dom'
import ArticleDetailPage, { RichSection } from '../components/ArticleDetailPage'
import NewsSidebar from '../components/NewsSidebar'
import { getNewsArticle } from '../data/news'
import { LOREM_LONG } from '../data/placeholders'

function NewsArticlePage() {
  const { slug } = useParams()
  const article = getNewsArticle(slug)

  if (!article) {
    return (
      <ArticleDetailPage
        crumbs={[
          { label: 'News', to: '/news' },
          { label: 'Article' },
        ]}
        title="Article not found"
        lede={LOREM_LONG}
      >
        <section className="rte">
          <p>We couldn&rsquo;t find that article. Please visit the News page.</p>
        </section>
      </ArticleDetailPage>
    )
  }

  return (
    <ArticleDetailPage
      align="left"
      compact
      crumbs={[
        { label: 'News', to: '/news' },
        { label: article.title },
      ]}
      title={article.title}
      lede={article.lede}
      sidebar={<NewsSidebar />}
      gallery
    >
      {article.overview && (
        <RichSection title="Overview" blocks={article.overview.blocks} />
      )}
      {article.sections.map((s) => (
        <RichSection key={s.id} id={s.id} title={s.title} blocks={s.blocks} />
      ))}
    </ArticleDetailPage>
  )
}

export default NewsArticlePage
