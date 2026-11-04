import { stockImages } from './stockImages'

/**
 * Get Involved landing (Support GSM) — client content matrix, 2026-11-04.
 * Numbered cards sit between the hero and the jump bar; the four feature
 * blocks below are the stacked anchor sections the tabs scroll to.
 */
export const foundationIntroColumns = [
  {
    num: '01.',
    title: 'Donate',
    description:
      'Donate to help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home. Every gift makes a difference.',
    path: '#ways-to-give',
    linkLabel: 'Learn more',
  },
  {
    num: '02.',
    title: 'Volunteer',
    description:
      'Volunteer your time and talents to support GSM Foundation’s fundraisers to enrich the lives of the men.',
    path: '#events',
    linkLabel: 'Learn more',
  },
  {
    num: '03.',
    title: 'Make A Lasting Impact',
    description:
      'Formed in 2007, the Shepherds Endowment Fund provides income to support Good Shepherd Manor’s mission in perpetuity.',
    path: '/shepherd-endowment-society',
    linkLabel: 'Learn more',
  },
]

export const eventsIntroColumns = [
  {
    num: '01.',
    title: 'Donate',
    description:
      'Donate to help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home. Every gift makes a difference.',
    path: '/support-gsm#ways-to-give',
    linkLabel: 'Learn more',
  },
  {
    num: '02.',
    title: 'Volunteer',
    description:
      'Volunteer your time and talents to support GSM Foundation’s fundraisers to enrich the lives of the men.',
    path: '/support-gsm#events',
    linkLabel: 'Learn more',
  },
  {
    num: '03.',
    title: 'Make A Lasting Impact',
    description:
      'Formed in 2007, the Shepherds Endowment Fund provides income to support Good Shepherd Manor’s mission in perpetuity.',
    path: '/shepherd-endowment-society',
    linkLabel: 'Learn more',
  },
]

export const getInvolvedSections = [
  {
    id: 'foundation',
    eyebrow: 'GSM Foundation',
    title: 'Supporting the Manor for over 45 years',
    paragraphs: [
      'Then Board President William J. McAllister called the Foundation an important step toward financial stability and excellent care. Its goals included facility improvements, unbudgeted needs, and a permanent endowment that would take shape in later years.',
      'Today, the Foundation helps bridge a funding gap of more than $20,000 per man each year beyond state support, sustaining the daily care, programs, and services that enrich life at Good Shepherd Manor.',
    ],
    imageSrc: stockImages.foundation,
    imageAlt: 'Volunteers working together outdoors',
  },
  {
    id: 'ways-to-give',
    eyebrow: 'Ways to Give',
    title: 'Every gift stays on campus',
    paragraphs: [
      'Every gift, big or small, helps support the men of GSM. Give through our three signature events—the Brunch Auction, Golf Invitational, and Fall Festival—or our annual Christmas Appeal. You can also make a general gift to support the Foundation.',
      'Other opportunities to give are through the Family Donor Program, honoring someone special with a tribute, remember a loved one with a memorial gift, or supporting the Manor’s future through the Shepherds Endowment Society.',
    ],
    flip: true,
    imageSrc: stockImages.giving,
    imageAlt: 'Hands holding a small gift',
    // Qgiv giving form embedded on the live GSM Foundation donation page.
    linkTo: 'https://secure.qgiv.com/for/wdof/',
    linkLabel: 'Ways to Give →',
  },
  {
    id: 'endowment-society',
    eyebrow: 'Shepherds Endowment Society',
    title: 'Your Legacy. Their Future.',
    paragraphs: [
      'Established in 2007 within the Good Shepherd Manor Foundation, the Shepherds Endowment Society generates income for GSM in perpetuity. Endowment gifts are invested rather than spent, generating annual income that extends beyond the life of the donor.',
      'Investment income provides a stable source of funding for GSM’s future operating expenses. Your legacy helps sustain compassionate care, meaningful opportunities, and a welcoming home for generations.',
    ],
    linkTo: '/shepherd-endowment-society',
    linkLabel: 'Explore the Shepherds Endowment Society →',
    imageSrc: stockImages.endowment,
    imageAlt: 'People reviewing plans together at a table',
  },
  {
    id: 'events',
    eyebrow: 'Events',
    title: 'Fall Festival, Golf Invitational, Brunch Auction, community & family events',
    paragraphs: [
      'GSM’s events raise needed funds for the Foundation while bringing people together. They introduce our mission, deepen community connections, and build lasting relationships that support meaningful lives for the men who call the Manor home.',
    ],
    listItems: ['Fall Festival', 'Golf Invitational', 'Brunch Auction', 'Community & Family Events'],
    flip: true,
    imageSrc: stockImages.events,
    imageAlt: 'A colorful outdoor celebration',
    linkTo: '/events',
    linkLabel: 'See all events →',
  },
]
