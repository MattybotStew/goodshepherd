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
    flip: true,
    linkTo: '/ways-to-give',
    linkLabel: 'Ways to Give →',
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
    title: 'Fall Festival, Golf Invitational, and family events',
    paragraphs: [LOREM_LONG],
    listItems: ['Fall Festival', 'Golf Invitational', 'Family Events'],
    flip: true,
    softImage: true,
    linkTo: '/events',
    linkLabel: 'See all events →',
  },
]

/** Short endowment teaser copy for other pages if needed */
export const endowmentTeaser = endowmentIntro

