import { endowmentIntro } from './endowment'
import { LOREM, LOREM_LONG } from './placeholders'

/** Get Involved landing jump-bar sections — Figma node 9179:32 */
export const getInvolvedSections = [
  {
    id: 'foundation',
    eyebrow: 'GSM Foundation',
    title: 'Supporting the Manor for over 40 years',
    paragraphs: [LOREM_LONG, LOREM],
  },
  {
    id: 'ways-to-give',
    eyebrow: 'Ways to Give',
    title: 'Every gift stays on campus',
    paragraphs: [LOREM_LONG, LOREM],
    listItems: ['One-time gift', 'Monthly giving', 'Planned & memorial gifts'],
    flip: true,
  },
  {
    id: 'endowment-society',
    eyebrow: 'Shepherd Endowment Society',
    title: 'Stewardship that outlives a gift',
    paragraphs: [LOREM_LONG, LOREM],
    linkTo: '/shepherd-endowment-society',
    linkLabel: 'Shepherd Endowment Society →',
  },
  {
    id: 'events',
    eyebrow: 'Events',
    title: 'Fall Festival, Brunch Auction, Golf Invitational, and family events',
    paragraphs: [LOREM_LONG],
    listItems: ['Fall Festival', 'Brunch Auction', 'Golf Invitational', 'Family Events'],
    flip: true,
    softImage: true,
    linkTo: '/events',
    linkLabel: 'See all events →',
  },
  {
    id: 'memorial-tribute',
    eyebrow: 'Memorial or Tribute',
    title: 'Honor a loved one through giving',
    paragraphs: [LOREM_LONG, LOREM],
  },
]

/** Short endowment teaser copy for other pages if needed */
export const endowmentTeaser = endowmentIntro
