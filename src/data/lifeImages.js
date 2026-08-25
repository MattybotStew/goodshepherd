/**
 * GSM Facebook photos (goodshepherdmanormomence/photos), downloaded for the wire.
 * Mosaic + event/story cards use real campus photos. Other slots still Adobe Stock
 * comps until swapped — license those originals on stock.adobe.com before production.
 *   hero              Figma 9195:584 (stadium crop)
 *   mosaic-*          Facebook (gym, outdoor picnic, campus gathering)
 *   involved-art      Adobe 200746843
 *   donate            Adobe 383620177
 *   stories           Facebook (gym activity, pavilion cookout)
 *   globalCta         Figma 9195:1352 (two men outdoors)
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
