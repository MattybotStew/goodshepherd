/**
 * Stand-in photos from Unsplash (free to use) until GSM supplies finals.
 * https://unsplash.com/license
 */

import mission from '../assets/stock/mission.jpg'
import timeline from '../assets/stock/timeline.jpg'
import sports from '../assets/stock/sports.jpg'
import accessibility from '../assets/stock/accessibility.jpg'
import foundation from '../assets/stock/foundation.jpg'
import giving from '../assets/stock/giving.jpg'
import endowment from '../assets/stock/endowment.jpg'
import events from '../assets/stock/events.jpg'
import memorial from '../assets/stock/memorial.jpg'
import careers from '../assets/stock/careers.jpg'
import culture from '../assets/stock/culture.jpg'
import apply from '../assets/stock/apply.jpg'
import garden from '../assets/stock/garden.jpg'
import kitchen from '../assets/stock/kitchen.jpg'
import workshop from '../assets/stock/workshop.jpg'
import home from '../assets/stock/home.jpg'
import meal from '../assets/stock/meal.jpg'

export const stockImages = {
  mission,
  timeline,
  affiliations: sports,
  accessibility,
  foundation,
  giving,
  endowment,
  events,
  memorial,
  careers,
  culture,
  openings: careers,
  apply,
  careersMosaic: [careers, culture, workshop, meal],
  gallery: [garden, kitchen, workshop, home, sports, meal, events, foundation],
}
