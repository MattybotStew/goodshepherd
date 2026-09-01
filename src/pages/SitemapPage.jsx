import './SitemapPage.css'

const navGroups = [
  { name: 'About', pages: [
    { name: 'About Us', page: 2, sections: ['Our History', 'Mission, Vision & Values', 'Affiliations', 'Accessibility Statement'] },
  ]},
  { name: 'Programs & Services', pages: [
    { name: 'Programs & Services', page: 3, note: 'Landing' },
    { name: 'Community Day Services', page: 4, sections: ['Digital Den'] },
    { name: 'Vocational Program', page: 5, note: 'TBD' },
    { name: 'Special Olympics', page: 6, note: 'New — Erin feedback' },
    { name: 'Residential Living', page: 7 },
    { name: 'Health & Well Being', page: 8, sections: ['Nursing Services', 'On-site Clinic', 'Pharmacy Services', 'Community Supports', 'Transportation Assistance'] },
  ]},
  { name: 'Support GSM', pages: [
    { name: 'Support GSM Foundation', page: 9, note: 'Merged: GSM Foundation + Ways to Give' },
    { name: 'Shepherd Endowment Society', page: 10 },
    { name: 'Events', page: 11, sections: ['Fall Festival', 'Brunch Auction', 'Golf Invitational', 'Family Events'] },
  ]},
  { name: 'News', pages: [
    { name: 'News & Updates', page: 12, note: 'Blog / press' },
    { name: 'Newsletters & Family Resources', page: 13, sections: ['Archive + signup'] },
  ]},
  { name: 'Careers', pages: [
    { name: 'Careers', page: 14, sections: ['Job Openings (DSP hiring)', 'Benefits'] },
  ]},
  { name: 'Contact', pages: [
    { name: 'Contact Us', page: 15, sections: ['Contact form', 'Staff directory', 'Map', 'Thank a Staff Member'] },
  ]},
]

const globalElements = [
  'Header with logo + navigation',
  'Support GSM button (header)',
  '"Now Hiring" banner',
  'Footer with contact info',
  'Newsletter signup (footer)',
  'Social link (Facebook)',
  'Privacy Policy link',
  'Accessibility Statement link',
]

function Box({ name, note, page, variant }) {
  return (
    <div className={`box box--${variant}`}>
      <span className="box__name">{name}</span>
      <span className="box__page">Page {page}</span>
      {note && <span className="box__note">{note}</span>}
    </div>
  )
}

function PageItem({ item }) {
  return (
    <div className="page-item">
      <Box name={item.name} note={item.note} page={item.page} variant="page" />
      {item.sections && item.sections.length > 0 && (
        <div className="section-list">
          {item.sections.map((s) => (
            <span key={s} className="section-pill">{s}</span>
          ))}
        </div>
      )}
    </div>
  )
}

function SitemapPage() {
  return (
    <div className="sitemap">
      <header className="sitemap__header">
        <h1 className="sitemap__title">Good Shepherd Manor — Sitemap</h1>
        <div className="sitemap__meta">
          <span>CloudMellow</span>
          <span>September 2026</span>
          <span>15 Pages</span>
        </div>
      </header>

      <p className="sitemap__subtitle">
        Website Redesign: Proposed page structure and navigation hierarchy — Updated per client feedback (Erin)
      </p>

      <hr className="sitemap__rule" />

      <div className="tree">
        <Box name="Home" page={1} variant="home" />
        <div className="line line--trunk" />
        <div className="tree__columns">
          {navGroups.map((group) => (
            <div className="tree__column" key={group.name}>
              <div className="line line--stub" />
              <div className="nav-label">{group.name}</div>
              <div className="line line--stub" />
              <div className="page-list">
                {group.pages.map((item) => (
                  <PageItem key={item.name} item={item} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <section className="global-elements">
        <h2 className="global-elements__heading">Global Elements (all pages)</h2>
        <ul className="global-elements__list">
          {globalElements.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
      <section className="consolidation-notes">
        <h2 className="consolidation-notes__heading">SOW Consolidation Notes</h2>
        <p className="consolidation-notes__lead">
          The combined client + Figma sitemap identified 19+ distinct pages. The SOW caps the project at <strong>15 main pages</strong>. Below is how we consolidated to fit — every page is counted honestly; only individual blog posts and newsletter archive items are exempt.
        </p>

        <div className="consolidation-notes__grid">
          <div className="consolidation-notes__col">
            <h3>What became sections</h3>
            <ul>
              <li><strong>Our History</strong> &rarr; section of <em>About Us</em></li>
              <li><strong>Mission, Vision &amp; Values</strong> &rarr; section of <em>About Us</em></li>
              <li><strong>Affiliations</strong> &rarr; section of <em>About Us</em></li>
              <li><strong>Accessibility Statement</strong> &rarr; section of <em>About Us</em> (also footer link)</li>
              <li><strong>Digital Den</strong> &rarr; section of <em>Community Day Services</em></li>
              <li><strong>Nursing / Clinic / Pharmacy / Supports / Transportation</strong> &rarr; sections of <em>Health &amp; Well Being</em></li>
              <li><strong>Fall Festival / Brunch Auction / Golf Invitational / Family Events</strong> &rarr; sections of <em>Events</em></li>
              <li><strong>Job Openings / Benefits</strong> &rarr; sections of <em>Careers</em></li>
              <li><strong>Contact form / Staff directory / Map / Thank a Staff Member</strong> &rarr; sections of <em>Contact Us</em></li>
            </ul>
          </div>

          <div className="consolidation-notes__col">
            <h3>The 15 main pages</h3>
            <ul>
              <li><strong>Home</strong> (1) — gateway</li>
              <li><strong>About Us</strong> (2) — 4 sections, anchor-linked</li>
              <li><strong>Programs &amp; Services</strong> (3) — landing</li>
              <li><strong>Community Day Services</strong> (4)</li>
              <li><strong>Vocational Program</strong> (5) — TBD</li>
              <li><strong>Special Olympics</strong> (6) — new per client feedback</li>
              <li><strong>Residential Living</strong> (7)</li>
              <li><strong>Health &amp; Well Being</strong> (8)</li>
              <li><strong>Support GSM Foundation</strong> (9) — merged GSM Foundation + Ways to Give</li>
              <li><strong>Shepherd Endowment Society</strong> (10)</li>
              <li><strong>Events</strong> (11) — includes Brunch Auction section</li>
              <li><strong>News &amp; Updates</strong> (12)</li>
              <li><strong>Newsletters &amp; Family Resources</strong> (13)</li>
              <li><strong>Careers</strong> (14)</li>
              <li><strong>Contact Us</strong> (15)</li>
            </ul>
          </div>
          <div className="consolidation-notes__col">
            <h3>Key decisions &amp; rationale</h3>
            <ul>
              <li><strong>About collapsed 4→1</strong> — static reference content; one page with anchor links saves slots</li>
              <li><strong>SOW counting</strong> — hub pages (News, Careers, Contact) count toward the 15; only individual posts/archive items are exempt</li>
              <li><strong>Contact = Page 15</strong> — primary conversion path; belongs in top-level nav</li>
              <li><strong>Newsletters &amp; Family Resources</strong> — combined newsletter archive and family communication into single page</li>
              <li><strong>Events with sub-sections</strong> — Fall Festival, Brunch Auction, Golf Invitational, and Family Events as anchor-linked sections</li>
              <li><strong>Vocational TBD</strong> — client flagged it; cheapest release valve if scope tightens</li>
              <li><strong>Support GSM merged</strong> — GSM Foundation + Ways to Give combined into one page (page 9) per Erin's feedback. The "Get Involved" nav renamed to "Support GSM."</li>
              <li><strong>Special Olympics added</strong> — new program page after Vocational, keeping total at 15 by merging Foundation + Donate</li>
              <li><strong>Phase-2 promotion</strong> — any section can become a page without breaking URLs; keep teaser anchors when promoting</li>
            </ul>
          </div>
        </div>

        <div className="consolidation-notes__footer">
          <p>
            Every topic from both the Figma sitemap and the client&rsquo;s wireframe is represented. <strong>Dark blue boxes</strong> are the 15 main pages. <strong>Light pills</strong> are sections within those pages. Total: exactly 15 — SOW compliant.
          </p>
        </div>
      </section>

      <footer className="sitemap__footer">
        <div className="legend">
          <span className="legend__item">
            <span className="legend__swatch legend__swatch--home" />
            Home
          </span>
          <span className="legend__item">
            <span className="legend__swatch legend__swatch--page" />
            Main page (15 total)
          </span>
          <span className="legend__item">
            <span className="legend__swatch legend__swatch--section" />
            Section within page
          </span>
        </div>
        <p className="sitemap__note">
          Max 15 main pages per SOW.
          <br />
          Blog posts and newsletter archive items are not counted as main pages.
        </p>
      </footer>
    </div>
  )
}

export default SitemapPage
