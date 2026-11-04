import { NavLink } from 'react-router-dom'
import { programs } from '../data/site'
import './ArticleSidebar.css'

function ArticleSidebar() {
  return (
    <aside className="article-sidebar">
      <nav aria-label="Programs">
        <p className="article-sidebar__label">Programs</p>
        <ul className="article-sidebar__list">
          {programs.map((p) => (
            <li key={p.path}>
              <NavLink
                to={p.path}
                className={({ isActive }) => (isActive ? 'is-active' : undefined)}
              >
                {p.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}

export default ArticleSidebar