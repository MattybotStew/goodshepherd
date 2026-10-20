/**
 * GSM Facebook photos (goodshepherdmanormomence/photos), downloaded for the wire.
 * Mosaic + CTA slots use real campus photos. Other slots still Adobe Stock
 * comps until swapped — license those originals on stock.adobe.com before production.
 *   hero              Figma 9195:584 (stadium crop)
 *   mosaic-*          Facebook (gym, outdoor picnic, campus gathering)
 *   donate            Adobe 383620177
 *   globalCta         Figma 9195:1352 (two men outdoors)
 */

import hero from '../assets/life/hero.jpg'
import aboutHero from '../assets/life/about-hero.jpg'
import aboutMission from '../assets/life/about-mission.jpg'
import aboutTimeline from '../assets/life/about-timeline.jpg'
import aboutAffiliations from '../assets/life/about-affiliations.jpg'
import mosaicWorkshop from '../assets/life/mosaic-workshop.jpg'
import mosaicKitchen from '../assets/life/mosaic-kitchen.jpg'
import mosaicGarden from '../assets/life/mosaic-garden.jpg'
import mosaicPorch from '../assets/life/mosaic-porch.jpg'
import donatePicnic from '../assets/life/donate-picnic.jpg'
import ctaGreenhouse from '../assets/life/cta-greenhouse.jpg'

export const lifeImages = {
  hero,
  aboutHero,
  aboutMission,
  aboutTimeline,
  aboutAffiliations,
  aboutMosaic: [mosaicWorkshop, mosaicKitchen, mosaicGarden, mosaicPorch],
  donate: donatePicnic,
  globalCta: ctaGreenhouse,
}
