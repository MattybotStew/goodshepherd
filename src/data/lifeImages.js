/**
 * Adobe Stock comps (1000px previews) of adult men in community, work, home, and recreation.
 * License the originals on stock.adobe.com before production. File numbers:
 *   hero              546456873
 *   mosaic-workshop   229113684
 *   mosaic-kitchen    320793293
 *   mosaic-garden     219036747
 *   mosaic-porch      680452499
 *   involved-art      200746843
 *   donate            383620177
 *   story-work        614843776
 *   story-recreation  765214175
 *   globalCta         530691361
 */

import hero from '../assets/life/hero.jpg'
import mosaicWorkshop from '../assets/life/mosaic-workshop.jpg'
import mosaicKitchen from '../assets/life/mosaic-kitchen.jpg'
import mosaicGarden from '../assets/life/mosaic-garden.jpg'
import mosaicPorch from '../assets/life/mosaic-porch.jpg'
import involvedArt from '../assets/life/involved-art.jpg'
import donatePicnic from '../assets/life/donate-picnic.jpg'
import storyWork from '../assets/life/story-work.jpg'
import storyRecreation from '../assets/life/story-recreation.jpg'
import ctaGreenhouse from '../assets/life/cta-greenhouse.jpg'

export const lifeImages = {
  hero,
  aboutMosaic: [mosaicWorkshop, mosaicKitchen, mosaicGarden, mosaicPorch],
  getInvolved: involvedArt,
  donate: donatePicnic,
  stories: [storyWork, storyRecreation],
  globalCta: ctaGreenhouse,
}
