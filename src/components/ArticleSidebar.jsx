import { Link, NavLink, useLocation } from 'react-router-dom'
import { healthData } from '../data/health'
import { communityDay, communityEngagement, residential } from '../data/programs'
import { programs } from '../data/site'
import './ArticleSidebar.css'

const SECTIONS_BY_PATH = {
  '/programs/community-day-services': communityDay.sections,
  '/programs/special-olympics': communityEngagement.sections,
  '/programs/residential-living': residential.sections,
  '/programs/health-well-being': healthData.sections,
}

function ArticleSidebar() {
  const { pathname, hash } = useLocation()

  return (
    <aside className="article-sidebar">
      <nav aria-label="Programs">
        <p className="article-sidebar__label">Programs</p>
        <ul className="article-sidebar__list">
          {programs.map((p) => {
            const sections = pathname === p.path ? SECTIONS_BY_PATH[p.path] : null
            return (
              <li key={p.path}>
                <NavLink
                  to={p.path}
                  className={({ isActive }) => (isActive ? 'is-active' : undefined)}
                >
                  {p.name}
                </NavLink>
                {sections?.length > 0 && (
                  <ul className="article-sidebar__sections">
                    {sections.map((s) => (
                      <li key={s.id}>
                        <Link
                          to={`${p.path}#${s.id}`}
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

export default ArticleSidebar