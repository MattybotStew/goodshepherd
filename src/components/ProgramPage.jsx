import ArticleDetailPage, { RichSection } from './ArticleDetailPage'
import ArticleSidebar from './ArticleSidebar'

function ProgramPage({ data }) {
  const { name, tagline, overview, sections = [] } = data

  return (
    <ArticleDetailPage
      align="left"
      compact
      crumbs={[
        { label: 'Programs & Services', to: '/programs' },
        { label: name },
      ]}
      title={name}
      lede={tagline}
      sidebar={<ArticleSidebar />}
      gallery
    >
      {overview && (
        <RichSection title="Overview" blocks={overview.blocks} />
      )}
      {sections.map((s) => (
        <RichSection
          key={s.id}
          id={s.id}
          title={s.title}
          blocks={s.blocks}
        />
      ))}
    </ArticleDetailPage>
  )
}

export default ProgramPage
