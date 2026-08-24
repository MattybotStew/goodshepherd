import { Link, NavLink, useLocation } from 'react-router-dom'
import { newsArticles } from '../data/news'
import './ArticleSidebar.css'

function NewsSidebar() {
  const { pathname, hash } = useLocation()

  return (
    <aside className="article-sidebar">
      <nav aria-label="News">
        <p className="article-sidebar__label">News</p>
        <ul className="article-sidebar__list">
          {newsArticles.map((article) => {
            const active = pathname === `/news/${article.slug}`
            return (
              <li key={article.slug}>
                <NavLink
                  to={`/news/${article.slug}`}
                  className={({ isActive }) => (isActive ? 'is-active' : undefined)}
                >
                  {article.title}
                </NavLink>
                {active && article.sections.length > 0 && (
                  <ul className="article-sidebar__sections">
                    {article.sections.map((s) => (
                      <li key={s.id}>
                        <Link
                          to={`/news/${article.slug}#${s.id}`}
                          className={hash === `#${s.id}` ? 'is-active' : undefined}
                        >
                          {s.title}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

export default NewsSidebar
