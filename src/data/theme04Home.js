/** Homepage wireframe (Figma 9137:3182) — body copy is placeholder lorem. */

import { LOREM, LOREM_EXTRA, LOREM_LONG, LOREM_SHORT } from './placeholders'

export const theme04Hero = {
  title: 'A Community of Compassion, Dignity, and Purpose.',
  lede: LOREM,
  ctaLabel: 'Now Hiring! Apply Today',
  ctaPath: '/careers',
}

export const theme04IntroColumns = [
  {
    num: '01.',
    title: 'Projects',
    description: LOREM_SHORT,
    path: '/programs',
    linkLabel: 'Learn more',
  },
  {
    num: '02.',
    title: 'Support GSM',
    description: LOREM_SHORT,
    path: '/support-gsm',
    linkLabel: 'Learn more',
  },
  {
    num: '03.',
    title: 'Donate',
    description: LOREM_SHORT,
    path: '/support-gsm',
    linkLabel: 'Learn more',
  },
]

export const theme04About = {
  eyebrow: 'About Us',
  title: 'A community of care, growth, and dignity for over 50 years.',
  paragraphs: [LOREM_LONG, LOREM_EXTRA],
}

export const theme04Impact = {
  title: 'Our Mission & Vision: Serving with Dignity',
  lede: LOREM_LONG,
}

export const theme04Stories = {
  title: "What's Happening at GSM",
  lede: LOREM,
  moreTo: '/events',
  moreLabel: 'See all events \u2192',
  items: [
    {
      title: "GSM's 35th Annual Fall Festival",
      excerpt: LOREM_SHORT,
      path: '/events#fall-festival',
    },
    {
      title: 'GSM Family Cookouts & MORE — Join us!',
      excerpt: LOREM_SHORT,
      path: '/events#family',
    },
  ],
}
