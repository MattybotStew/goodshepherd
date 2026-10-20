/** Homepage wireframe (Figma 9137:3182) — body copy is placeholder lorem. */

import { LOREM, LOREM_EXTRA, LOREM_LONG, LOREM_SHORT } from './placeholders'

export const theme04Hero = {
  title: 'A Community of Compassion, Dignity, and Purpose.',
  lede: 'Supporting men with intellectual and developmental disabilities through compassionate care, meaningful opportunities, and a life rich with possibility',
  ctaLabel: 'Learn more',
  ctaPath: '/about',
}

export const theme04IntroColumns = [
  {
    num: '01.',
    title: 'Get Involved',
    description:
      'Share your time and talents, join an event, or volunteer to make a meaningful difference in the lives of the men at GSM.',
    path: '/events',
    linkLabel: 'Learn more',
  },
  {
    num: '02.',
    title: 'Donate',
    description:
      'Help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home.',
    path: '/support-gsm',
    linkLabel: 'Learn more',
  },
]

export const theme04About = {
  eyebrow: 'About Us',
  title: 'A community of care, growth, and dignity for over 55 years.',
  paragraphs: [
    'Founded in 1971 by families seeking a brighter future for their sons, Good Shepherd Manor carries forward a legacy of faith and compassionate care. Today, we support men with intellectual and developmental disabilities build community, discover possibilities, and live with dignity and purpose.',
  ],
}

export const theme04Impact = {
  title: 'Our Mission & Vision: Serving with Dignity',
  lede:
    'We honor the dignity of every man we serve, providing compassionate care, encouraging personal growth, and creating a welcoming community where men with disabilities feel valued, supported, and at home.',
}

export const theme04Stories = {
  title: "What's Happening at GSM",
  lede: 'GSM brings our men and community together through a wide variety of activities & events.',
  moreTo: '/events',
  moreLabel: 'See all events',
  items: [
    {
      title: "GSM's Annual Fall Festival",
      excerpt:
        'An annual celebration of family fun, community spirit, and support for the men of GSM.',
      linkLabel: 'Read More',
      path: '/events#fall-festival',
    },
    {
      title: 'GSM Family Cookouts & More',
      excerpt:
        'Celebrating 35 years of family fun, community spirit, and support for the men of GSM.',
      linkLabel: 'Read More',
      path: '/events#family',
    },
  ],
}
