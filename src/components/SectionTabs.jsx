import { useEffect, useState } from 'react'
import './SectionTabs.css'

/**
 * Tab-style jump bar that scrolls to stacked anchor sections instead of
 * hiding content. All sections stay visible; the active tab highlights as
 * you scroll (IntersectionObserver scroll-spy). Clicking a tab smooth-scrolls
 * to its `#id` target via a native anchor link (CSS scroll-behavior + scroll-margin).
 */
export default function SectionTabs({ sections }) {
  const [activeId, setActiveId] = useState(sections[0]?.id)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting)
        if (!visible.length) return
        // Active = the visible section closest to the top of the viewport.
        const top = visible.reduce((a, b) =>
          a.boundingClientRect.top <= b.boundingClientRect.top ? a : b
        )
        setActiveId(top.target.id)
      },
      { rootMargin: '-10% 0px -60% 0px', threshold: 0 }
    )

    sections.forEach((section) => {
      const el = document.getElementById(section.id)
      if (el) observer.observe(el)
    })
    return () => observer.disconnect()
  }, [sections])

  return (
    <nav className="section-tabs" aria-label="Ways to get involved">
      <div className="section-tabs__list">
        {sections.map((section) => (
          <a
            key={section.id}
            href={`#${section.id}`}
            className={
              activeId === section.id
                ? 'section-tabs__tab is-active'
                : 'section-tabs__tab'
            }
            onClick={() => setActiveId(section.id)}
            aria-current={activeId === section.id ? 'true' : undefined}
          >
            {section.eyebrow}
          </a>
        ))}
      </div>
    </nav>
  )
}
