import { useEffect, useRef, useState } from 'react'
import { history as defaultHistory } from '../data/history'
import '../styles/starter.css'

export default function HistoryTimelineSection({
  id = 'history',
  eyebrow = 'Our History',
  title = 'A Timeline of Caring',
  entries = defaultHistory,
}) {
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
  }, [entries])

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
    <section className="band band--alt anchor" id={id}>
      <div className="wrap">
        <div className="timeline__head">
          <div className="img-ph img-ph--soft timeline__photo" aria-hidden="true" />
          <div>
            <span className="eyebrow">{eyebrow}</span>
            <h2>{title}</h2>
          </div>
        </div>
        <div
          className="timeline-scroll"
          ref={scrollRef}
          role="region"
          aria-label={title}
          tabIndex={0}
        >
          <ol className="timeline">
            {entries.map((entry) => (
              <li className="timeline__item" key={entry.year}>
                <span className="timeline__year">{entry.year}</span>
                <p className="timeline__text">{entry.text}</p>
              </li>
            ))}
          </ol>
        </div>
        <div
          className="timeline-bar"
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
    </section>
  )
}
