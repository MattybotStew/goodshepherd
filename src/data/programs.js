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
  tagline: "Classes explore vocational skills, economics, personal living skills, technology and more, with hands-on activities tailored to each resident’s needs.",
  overview: {
    blocks: [
      {
        type: 'p',
        text: "Community Day Services at Good Shepherd Manor provide a dynamic, engaging environment where men with intellectual and developmental disabilities can learn, grow, and build meaningful connections. Our structured classes and hands-on activities are tailored to each individual’s interests and abilities, with a focus on building practical skills for greater independence and confidence in daily life. From vocational training and technology to personal living skills and economics, each day offers opportunities to discover strengths and try new things in a supportive, caring atmosphere.",
      },
      {
        type: 'p',
        text: "Beyond the classroom, community engagement is a key part of our program. Men enjoy outings for shopping, attending Mass, participating in Special Olympics, and taking part in events throughout the Momence community. Through these experiences, friendships grow, social skills strengthen, and a sense of belonging flourishes both on campus and beyond.",
      },
      {
        type: 'h3',
        text: 'A Typical Day',
      },
      {
        type: 'p',
        text: "Each day is thoughtfully structured to balance learning and recreation. The morning may begin with classroom instruction or skill-building activities, followed by hands-on projects or community outings. Afternoons often include time for hobbies, physical activity, or specialized programs like our Digital Den. Throughout the day, caring staff provide encouragement, guidance, and support, ensuring that every man has the chance to participate at his own pace and according to his interests.",
      },
      {
        type: 'ul',
        items: [
          'Skill-building classes in technology, budgeting, cooking, and personal care',
          'Vocational experiences that prepare for meaningful work opportunities',
          'Community outings to local businesses, churches, and events',
          'Active participation in Special Olympics and recreational activities',
        ],
      },
      {
        type: 'p',
        text: "At the heart of Community Day Services is our belief that every man has gifts to share. By nurturing those gifts in a welcoming, family-like environment, we help each individual build confidence, develop independence, and enjoy a full, purposeful life.",
      },
      {
        type: 'figure',
        caption: 'Learning and connecting through hands-on activities on the GSM campus.',
      },
    ],
  },
  sections: [
    {
      id: 'digital-den',
      title: 'Digital Den',
      blocks: [
        {
          type: 'p',
          text: "The Digital Den is a dedicated space where men at Good Shepherd Manor can build computer literacy and explore the world of technology in a fun, supportive setting. With guidance from trained staff, individuals learn essential skills like typing, navigating the internet safely, using word processing and spreadsheet programs, and communicating through email or video calls to stay connected with loved ones.",
        },
        {
          type: 'quote',
          text: "Technology opens new doors to learning, independence, and connection.",
          cite: 'GSM Community Day Services',
        },
        {
          type: 'h3',
          text: 'What the Space Is For',
        },
        {
          type: 'p',
          text: "The Digital Den is more than a computer lab—it’s a place of creativity and discovery. Men can work on personal projects, explore educational games, research topics of interest, or learn practical skills they’ll use in everyday life. Lessons are individualized to match each person’s goals and skill level, allowing for growth at a comfortable, encouraging pace.",
        },
        {
          type: 'ol',
          items: [
            'Building digital literacy for everyday tasks',
            'Staying connected with family and friends',
            'Exploring hobbies, music, photos, and creative projects',
          ],
        },
        {
          type: 'p',
          text: "Whether learning to send an email for the first time or mastering a new program, time in the Digital Den helps build confidence and independence—skills that carry over into the wider community.",
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
