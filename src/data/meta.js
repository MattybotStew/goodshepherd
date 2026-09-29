export const SITE_NAME = 'Good Shepherd Manor'

export const DEFAULT_DESCRIPTION =
  'Good Shepherd Manor is a residential care community in Momence, Illinois, supporting men with intellectual and developmental disabilities through community day services, vocational programs, residential living, and health and well-being supports.'

const PAGE_TITLES = {
  '/': 'Good Shepherd Manor — Compassionate Care Since 1971',
  '/about': 'About Us',
  '/programs': 'Programs & Services',
  '/programs/community-day-services': 'Community Day Services',
  '/programs/vocational': 'Vocational Program',
  '/programs/special-olympics': 'Special Olympics',
  '/programs/residential-living': 'Residential Living',
  '/programs/health-well-being': 'Health & Well Being',
  '/support-gsm': 'Support GSM Foundation',
  '/shepherd-endowment-society': 'Shepherd Endowment Society',
  '/events': 'Events',
  '/news': 'News & Updates',
  '/newsletters': 'Newsletters & Family Resources',
  '/careers': 'Careers',
  '/contact': 'Contact Us',
  '/privacy': 'Privacy Policy',
  '/sitemap': 'Sitemap',
}

/**
 * Resolve the document title + meta description for a route path.
 * Falls back to News & Updates for article routes and Page Not Found otherwise.
 */
export function resolveMeta(pathname) {
  const key = pathname.length > 1 ? pathname.replace(/\/$/, '') : pathname
  let page = PAGE_TITLES[key]

  if (!page && key.startsWith('/news/')) page = 'News & Updates'
  if (!page) page = 'Page Not Found'

  const title = key === '/' ? page : `${page} — ${SITE_NAME}`
  return { title, description: DEFAULT_DESCRIPTION }
}
