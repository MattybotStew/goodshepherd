import {
  LOREM,
  LOREM_EXTRA,
  LOREM_LONG,
  LOREM_SHORT,
  LOREM_XL,
  LOREM_XXL,
} from './placeholders'

/**
 * News articles — shaped exactly like program data so they render through the
 * same ArticleDetailPage template as the program detail pages.
 * Body copy is lorem placeholder pending client review (per AGENTS.md).
 */
export const newsArticles = [
  {
    slug: '35th-annual-fall-festival',
    date: 'Aug 2026',
    tag: 'Events',
    title: "GSM's 35th Annual Fall Festival",
    lede: LOREM_LONG,
    overview: {
      blocks: [
        { type: 'p', text: LOREM_XXL },
        { type: 'p', text: LOREM_XL },
        {
          type: 'figure',
          caption: 'Placeholder photo — the Fall Festival on the Momence campus.',
        },
        { type: 'p', text: LOREM_LONG },
      ],
    },
    sections: [
      {
        id: 'festival-day',
        title: 'A day of celebration',
        blocks: [
          { type: 'p', text: LOREM_XXL },
          {
            type: 'ul',
            items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
          },
          {
            type: 'quote',
            text: LOREM_LONG,
            cite: 'Placeholder quote',
          },
        ],
      },
      {
        id: 'how-to-join',
        title: 'How to join us',
        blocks: [
          { type: 'p', text: LOREM_XL },
          {
            type: 'ol',
            items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
          },
          {
            type: 'callout',
            title: 'Event details',
            text: LOREM,
          },
          { type: 'link', to: '/contact', label: 'Ask about the Fall Festival' },
        ],
      },
    ],
  },
  {
    slug: 'digital-den-community-day',
    date: 'Jul 2026',
    tag: 'Programs',
    title: 'GSM’s New Digital Den in Community Day Services',
    lede: LOREM_LONG,
    overview: {
      blocks: [
        { type: 'p', text: LOREM_XXL },
        { type: 'p', text: LOREM_XL },
        {
          type: 'figure',
          caption: 'Placeholder photo — the new Digital Den.',
        },
        { type: 'p', text: LOREM_LONG },
      ],
    },
    sections: [
      {
        id: 'whats-inside',
        title: 'What’s inside the Digital Den',
        blocks: [
          { type: 'p', text: LOREM_XXL },
          {
            type: 'ul',
            items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
          },
        ],
      },
      {
        id: 'why-it-matters',
        title: 'Why it matters',
        blocks: [
          { type: 'p', text: LOREM_XL },
          {
            type: 'quote',
            text: LOREM_LONG,
            cite: 'Placeholder quote',
          },
        ],
      },
    ],
  },
  {
    slug: '30th-golf-invitational',
    date: 'Jun 2026',
    tag: 'Events',
    title: '30th Anniversary Golf Invitational Sponsors',
    lede: LOREM_LONG,
    overview: {
      blocks: [
        { type: 'p', text: LOREM_XXL },
        { type: 'p', text: LOREM_XL },
        {
          type: 'figure',
          caption: 'Placeholder photo — the Golf Invitational.',
        },
        { type: 'p', text: LOREM_LONG },
      ],
    },
    sections: [
      {
        id: 'our-sponsors',
        title: 'Thank you to our sponsors',
        blocks: [
          { type: 'p', text: LOREM_XXL },
          {
            type: 'ul',
            items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
          },
        ],
      },
      {
        id: 'get-involved',
        title: 'Sponsor next year’s event',
        blocks: [
          { type: 'p', text: LOREM_XL },
          {
            type: 'callout',
            title: 'Sponsorship',
            text: LOREM,
          },
          { type: 'link', to: '/contact', label: 'Inquire about sponsorship' },
        ],
      },
    ],
  },
]

export const getNewsArticle = (slug) =>
  newsArticles.find((a) => a.slug === slug)
