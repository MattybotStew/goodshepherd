/** Non-Profit Organization 04 demo structure — body copy is placeholder lorem. */

import { LOREM, LOREM_EXTRA, LOREM_LONG, LOREM_SHORT } from './placeholders'

export const theme04Hero = {
  title: 'Empowering Change, One Step at a Time',
  lede: LOREM,
  ctaLabel: 'Donate Now',
  ctaPath: '/ways-to-give',
}

export const theme04IntroColumns = [
  {
    num: '01.',
    title: 'Causes',
    description: LOREM_SHORT,
    path: '/programs',
    linkLabel: 'See Proof',
  },
  {
    num: '02.',
    title: 'Get involved',
    description: LOREM_SHORT,
    path: '/support-gsm',
    linkLabel: 'Learn More',
  },
  {
    num: '03.',
    title: 'Donation',
    description: LOREM_SHORT,
    path: '/ways-to-give',
    linkLabel: 'Donate Now',
  },
]

export const theme04About = {
  eyebrow: 'About Us',
  title: 'Our journey of compassion and hope',
  paragraphs: [LOREM_LONG, LOREM_EXTRA],
}

export const theme04Impact = {
  eyebrow: 'Our Impact',
  title: 'The impact we have made in our community',
  lede: LOREM_LONG,
  stats: [
    { value: '2M+', label: 'People served worldwide' },
    { value: '500+', label: 'Projects funded' },
    { value: '1M', label: 'People to take action' },
    { value: '50+', label: 'Partner organizations' },
  ],
}

export const theme04GetInvolved = {
  eyebrow: 'Get Involved',
  title: 'Join our movement for change',
  paragraphs: [LOREM_LONG, LOREM],
  linkPath: '/events',
  linkLabel: 'Register Now',
}

export const theme04Stories = {
  title: 'Inspiring tales of transformation',
  lede: LOREM,
  items: [
    {
      title: 'The Special One',
      excerpt: LOREM,
      path: '/news',
    },
    {
      title: 'A Better Education for Everyone',
      excerpt: LOREM,
      path: '/news',
    },
  ],
}

export const theme04DonateCta = {
  title: 'We can create a better tomorrow',
  lede: LOREM,
}
