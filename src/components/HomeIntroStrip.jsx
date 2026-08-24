import { Link } from 'react-router-dom'
import './HomeIntroStrip.css'

const HOME_COLUMNS = [
  {
    num: '01.',
    title: 'Projects',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.',
    path: '/programs',
  },
  {
    num: '02.',
    title: 'Get Involved',
    description:
      'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.',
    path: '/support-gsm',
  },
  {
    num: '03.',
    title: 'Donate',
    description:
      'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
    path: '/ways-to-give',
  },
]

const INVOLVED_COLUMNS = [
  {
    num: '01.',
    title: 'Donate',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.',
    path: '/ways-to-give',
  },
  {
    num: '02.',
    title: 'Volunteer',
    description:
      'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.',
    path: '/events',
  },
  {
    num: '03.',
    title: 'Give for Good',
    description:
      'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
    path: '/shepherd-endowment-society',
  },
]

const COLUMNS_BY_VARIANT = {
  home: HOME_COLUMNS,
  about: HOME_COLUMNS,
  page: HOME_COLUMNS,
  involved: INVOLVED_COLUMNS,
}

export default function HomeIntroStrip({ variant = 'home' }) {
  const columns = COLUMNS_BY_VARIANT[variant] || HOME_COLUMNS

  return (
    <section
      className={`home-intro home-intro--${variant}`}
      aria-label="Ways to engage"
    >
      <div className="home-intro__card">
        {columns.map((col) => (
          <article className="home-intro__col" key={col.num}>
            <p className="home-intro__num">{col.num}</p>
            <h2>{col.title}</h2>
            <p>{col.description}</p>
            <Link to={col.path}>Learn more &rarr;</Link>
          </article>
        ))}
      </div>
    </section>
  )
}
