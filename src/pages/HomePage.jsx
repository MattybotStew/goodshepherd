import { Link } from "react-router-dom";
import AboutMissionSection from "../components/AboutMissionSection";
import HomeIntroStrip from "../components/HomeIntroStrip";
import ImpactSection from "../components/ImpactSection";
import ProgramsServicesSection from "../components/ProgramsServicesSection";
import {
  theme04About,
  theme04Hero,
  theme04Impact,
  theme04Stories,
} from "../data/theme04Home";
import { lifeImages } from "../data/lifeImages";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="home">
      <section className="home-hero">
        <div
          className="home-hero__photo home-hero__photo--image"
          style={{ "--hero-photo": `url(${lifeImages.hero})` }}
          aria-hidden="true"
        />
        <div className="home-hero__inner">
          <h1>{theme04Hero.title}</h1>
          <p>{theme04Hero.lede}</p>
          <Link to={theme04Hero.ctaPath} className="home-btn home-btn--blue">
            {theme04Hero.ctaLabel}
          </Link>
        </div>
      </section>

      <HomeIntroStrip variant="home" />

      <ImpactSection title={theme04Impact.title} lede={theme04Impact.lede} />

      <ProgramsServicesSection />

      <AboutMissionSection
        showReadMore
        eyebrow={theme04About.eyebrow}
        title={theme04About.title}
        paragraphs={theme04About.paragraphs}
        mosaicImages={lifeImages.aboutMosaic}
      />

      {/* What's Happening at GSM — two event cards */}
      <section
        className="support-gsm-foundation"
        aria-labelledby="home-events-heading"
      >
        <div className="support-gsm-foundation__inner">
          <h2 id="home-events-heading">{theme04Stories.title}</h2>
          <p className="support-gsm-foundation__lede">{theme04Stories.lede}</p>
          <Link
            to={theme04Stories.moreTo}
            className="support-gsm-foundation__cta"
          >
            {theme04Stories.moreLabel}
          </Link>
          <div className="support-gsm-foundation__grid support-gsm-foundation__grid--events">
            {theme04Stories.items.map((item) => (
              <Link to={item.path} className="support-card" key={item.path}>
                <h3>{item.title}</h3>
                <p>{item.excerpt}</p>
                <span className="support-card__link">{item.linkLabel}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

    </div>
  );
}

export default HomePage;
