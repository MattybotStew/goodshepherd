import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { programs } from '../data/site'
import { LOREM, LOREM_SHORT } from '../data/placeholders'
import communityDayIcon from '../assets/programs/community-day.svg'
import vocationalIcon from '../assets/programs/vocational.svg'
import specialOlympicsIcon from '../assets/programs/special-olympics.svg'
import residentialIcon from '../assets/programs/residential.svg'
import healthIcon from '../assets/programs/health.svg'
import '../styles/starter.css'
import './ProgramsServicesSection.css'

const PROGRAM_ICONS = {
  '/programs/community-day-services': communityDayIcon,
  '/programs/vocational': vocationalIcon,
  '/programs/special-olympics': specialOlympicsIcon,
  '/programs/residential-living': residentialIcon,
  '/programs/health-well-being': healthIcon,
}

export default function ProgramsServicesSection({ showViewAll = true }) {
  const scrollRef = useRef(null)
  const barRef = useRef(null)
  const [thumb, setThumb] = useState({ width: 100, left: 0 })

  useEffect(() => {
    const el = scrollRef.current
    if (!el) return

    const update = () => {
      const max = el.scrollWidth - el.clientWidth
      if (max <= 0) {
        setThumb({ width: 100, left: 0 })
        return
      }
      const width = Math.max(10, (el.clientWidth / el.scrollWidth) * 100)
      setThumb({ width, left: (el.scrollLeft / max) * (100 - width) })
    }

    update()
    el.addEventListener('scroll', update, { passive: true })
    window.addEventListener('resize', update)
    return () => {
      el.removeEventListener('scroll', update)
      window.removeEventListener('resize', update)
    }
  }, [])

  const scrollToPointer = (clientX) => {
    const el = scrollRef.current
    const bar = barRef.current
    if (!el || !bar) return
    const rect = bar.getBoundingClientRect()
    const ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width))
    el.scrollLeft = ratio * (el.scrollWidth - el.clientWidth)
  }

  const handleBarPointerDown = (e) => {
    scrollToPointer(e.clientX)
    const onMove = (ev) => scrollToPointer(ev.clientX)
    const onUp = () => {
      window.removeEventListener('pointermove', onMove)
      window.removeEventListener('pointerup', onUp)
    }
    window.addEventListener('pointermove', onMove)
    window.addEventListener('pointerup', onUp)
  }

  return (
    <section className="programs-services">
      <div className="programs-services__container">
        <div className="programs-services__header">
          <div className="programs-services__intro">
            <h2>Our Programs &amp; Services</h2>
            <p>{LOREM}</p>
          </div>
          {showViewAll && (
            <Link to="/programs" className="programs-services__more">
              View all programs &rarr;
            </Link>
          )}
        </div>
        <div className="programs-services__track">
          <div
            className="programs-services__grid timeline-scroll"
            ref={scrollRef}
            role="region"
            aria-label="Program cards — scroll horizontally for more"
            tabIndex={0}
          >
            {programs.map((p) => (
              <article className="programs-services__card" key={p.path}>
                <div className="programs-services__icon" aria-hidden="true">
                  {PROGRAM_ICONS[p.path] && (
                    <img src={PROGRAM_ICONS[p.path]} alt="" />
                  )}
                </div>
                <h3>{p.homeName || p.name}</h3>
                <p>{LOREM_SHORT}</p>
                <Link to={p.path} className="programs-services__link">
                  Learn more &rarr;
                </Link>
              </article>
            ))}
          </div>
          <div
            className="timeline-bar programs-services__scroll-bar"
            ref={barRef}
            onPointerDown={handleBarPointerDown}
            aria-hidden="true"
          >
            <div
              className="timeline-bar__thumb"
              style={{ width: `${thumb.width}%`, left: `${thumb.left}%` }}
            />
          </div>
        </div>
      </div>
    </section>
  )
}
