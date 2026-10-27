import { LOREM_LONG } from '../data/placeholders'
import './ProgramsIntroSection.css'

export default function ProgramsIntroSection() {
  return (
    <section className="programs-intro">
      <div className="wrap programs-intro__inner">
        <div className="programs-intro__header">
          <h2>Building Skills, Connections, and Confidence</h2>
          <div className="programs-intro__aside">
            <span className="programs-intro__rule" aria-hidden="true" />
            <p>
              Through personalized support and engaging experiences, each man discovers his strengths, develops everyday skills, builds lasting friendships, and gains confidence to try new things.
            </p>
          </div>
        </div>

        <div className="programs-intro__mosaic" aria-hidden="true">
          <div className="programs-intro__ph programs-intro__ph--tall" />
          <div className="programs-intro__ph programs-intro__ph--wide" />
          <div className="programs-intro__stack">
            <div className="programs-intro__ph programs-intro__ph--short" />
            <div className="programs-intro__ph programs-intro__ph--short" />
          </div>
        </div>
      </div>
    </section>
  )
}
