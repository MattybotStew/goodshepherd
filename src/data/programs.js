import {
  LOREM,
  LOREM_EXTRA,
  LOREM_LONG,
  LOREM_SHORT,
  LOREM_XL,
  LOREM_XXL,
} from './placeholders'

export const communityDay = {
  name: 'Community Day Services',
  tagline: LOREM_SHORT,
  overview: {
    blocks: [
      { type: 'p', text: LOREM_XXL },
      { type: 'p', text: LOREM_XL },
      { type: 'h3', text: 'A typical day' },
      { type: 'p', text: LOREM_LONG },
      {
        type: 'ul',
        items: [
          LOREM_SHORT,
          LOREM,
          LOREM_EXTRA,
          'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium.',
        ],
      },
      { type: 'p', text: LOREM_XL },
      {
        type: 'figure',
        caption: 'Placeholder photo — classrooms and shared spaces on campus.',
      },
      { type: 'p', text: LOREM_LONG },
    ],
  },
  sections: [
    {
      id: 'digital-den',
      title: 'Digital Den',
      blocks: [
        { type: 'p', text: LOREM_XXL },
        {
          type: 'quote',
          text: LOREM_LONG,
          cite: 'Placeholder quote',
        },
        { type: 'h3', text: 'What the space is for' },
        { type: 'p', text: LOREM_XL },
        {
          type: 'ol',
          items: [
            LOREM_SHORT,
            LOREM,
            LOREM_EXTRA,
          ],
        },
        { type: 'p', text: LOREM_LONG },
        {
          type: 'callout',
          title: 'Note',
          text: LOREM,
        },
      ],
    },
  ],
}

export const vocational = {
  name: 'Vocational Program',
  tagline: LOREM_SHORT,
  overview: {
    blocks: [
      { type: 'p', text: LOREM_XXL },
      { type: 'p', text: LOREM_XL },
      { type: 'h3', text: 'How work is structured' },
      { type: 'p', text: LOREM_LONG },
      {
        type: 'ol',
        items: [
          LOREM,
          LOREM_SHORT,
          LOREM_EXTRA,
          'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.',
        ],
      },
      {
        type: 'callout',
        title: 'Scope',
        text: 'This program page is a placeholder while vocational offerings are confirmed. Body copy is dummy text only.',
      },
      { type: 'h3', text: 'Skills and routines' },
      { type: 'p', text: LOREM_XXL },
      {
        type: 'ul',
        items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
      },
      {
        type: 'figure',
        caption: 'Placeholder photo — work settings and coaching.',
      },
      { type: 'p', text: LOREM_XL },
      {
        type: 'link',
        to: '/contact',
        label: 'Ask about vocational services',
      },
    ],
  },
  sections: [],
}

export const residential = {
  name: 'Residential Living',
  tagline: LOREM_SHORT,
  overview: {
    blocks: [
      { type: 'p', text: LOREM_XXL },
      {
        type: 'figure',
        caption: 'Placeholder photo — homes on the Momence campus.',
      },
      { type: 'p', text: LOREM_XL },
      { type: 'h3', text: 'Life in the houses' },
      { type: 'p', text: LOREM_LONG },
      {
        type: 'ul',
        items: [
          LOREM,
          LOREM_SHORT,
          LOREM_EXTRA,
          'At vero eos et accusamus et iusto odio dignissimos ducimus.',
        ],
      },
      {
        type: 'quote',
        text: LOREM_XL,
        cite: 'Placeholder quote',
      },
      { type: 'h3', text: 'Staffing and belonging' },
      { type: 'p', text: LOREM_XXL },
      { type: 'p', text: LOREM_LONG },
      {
        type: 'link',
        to: '/contact',
        label: 'Schedule a campus visit',
      },
    ],
  },
  sections: [],
}

export const specialOlympics = {
  name: 'Special Olympics',
  tagline: LOREM_SHORT,
  overview: {
    blocks: [
      { type: 'p', text: LOREM_XXL },
      { type: 'p', text: LOREM_XL },
      {
        type: 'callout',
        title: 'Program in development',
        text: 'Special Olympics programming is being planned. This page structure will be updated with final details.',
      },
      { type: 'h3', text: 'Athletic programs' },
      { type: 'p', text: LOREM_LONG },
      {
        type: 'ul',
        items: [LOREM_SHORT, LOREM, LOREM_EXTRA],
      },
      {
        type: 'figure',
        caption: 'Placeholder photo — athletics and community events.',
      },
      { type: 'p', text: LOREM_XL },
    ],
  },
  sections: [],
}
