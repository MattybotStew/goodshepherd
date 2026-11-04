/**
 * Careers page — client content matrix, 2026-11-04.
 * Images marked In-Progress on the matrix still use stand-in stock photos.
 */

export const careersIntroColumns = [
  {
    num: '01.',
    title: 'Programs & Services',
    description:
      'Personalized programs and compassionate services help each man learn, connect, and thrive.',
    path: '/programs',
    linkLabel: 'Learn more',
  },
  {
    num: '02.',
    title: 'Get Involved',
    description:
      'Discover ways to support the Manor through giving, events and sharing your time and talent.',
    path: '/support-gsm',
    linkLabel: 'Learn more',
  },
  {
    num: '03.',
    title: 'News You Can Use',
    description:
      'Get connected with Manor news, newsletters, useful updates and resources for GSM families.',
    path: '/news',
    linkLabel: 'Learn more',
  },
]

export const careersIntro = {
  eyebrow: 'Careers at Good Shepherd Manor',
  title: 'Build a career with purpose',
  paragraphs: [
    'At Good Shepherd Manor, your work makes a difference in the lives of the men we serve. Whether providing direct care or supporting our programs and operations, you’ll be part of a team that values dignity, compassion and connection.',
    'Bring your talents, grow your skills and find purpose in work that helps others enjoy meaningful lives. Explore career opportunities at GSM.',
  ],
}

export const careersBenefits = {
  id: 'benefits',
  eyebrow: 'Benefits',
  title: 'Caring for Our Team',
  paragraphs: [
    'At Good Shepherd Manor, we value the people who make our mission possible. Our benefits are designed to support your health, financial well-being and time away from work, so you can care for yourself and those who matter to you.',
    'Benefits may include health and dental insurance, paid time off and retirement plan options. Eligibility varies by position.',
  ],
  listItems: [
    'Competitive pay and benefits package',
    'Comprehensive paid training provided',
    'Flexible shifts and shift differentials',
    'Paid time off and holiday premium pay',
  ],
}

export const careersCulture = {
  id: 'culture',
  eyebrow: 'Our Culture',
  title: 'A team that cares',
  paragraphs: [
    'At Good Shepherd Manor, caring for others is a team effort. Our staff bring their talents, compassion and dedication together to support the men we serve and create a welcoming community.',
    'From everyday moments to milestones, we support one another and celebrate the difference we make together.',
  ],
}

export const careersOpenings = {
  id: 'openings',
  eyebrow: 'Job Openings',
  title: 'Join our team',
  lede: 'Bring your talents and compassion to Good Shepherd Manor, where your work can make a difference in the lives of the men we serve.',
  // Application route as published on the live goodshepherdmanor.org site (2026-11).
  indeedUrl: 'https://www.indeed.com/',
  phone: '815-592-7423',
  phoneHref: 'tel:+18155927423',
}

export const careersJobs = [
  {
    title: 'Direct Service Provider (DSP)',
    body: 'As a Direct Support Professional, you will provide compassionate, personalized support.',
    applyLabel: 'Apply for Direct Service Provider →',
    applyTo: '/contact',
  },
  {
    title: 'Supervisor (Residential Services Director) RSD',
    body: 'RSD directs and trains staff, coordinates care, and supports residents.',
    applyLabel: 'Apply for Clinical Service Provider →',
    applyTo: '/contact',
  },
]

export const careersApply = {
  id: 'apply',
  eyebrow: 'Apply Today',
  title: 'Ready to make a difference?',
  paragraphs: [
    'At Good Shepherd Manor, meaningful work begins with everyday connections. Get to know the men, encourage new interests, and celebrate each achievement. Bring your strengths to a team that works together to make each home welcoming and each day count.',
    'Benefits include health, dental, and life insurance, paid time off, a referral program, and a 403(b) plan with matching to help you build your future.',
  ],
  linkTo: '/contact',
  linkLabel: 'Contact us to apply →',
}
