import { Link } from "react-router-dom";
import AboutMissionSection from "../components/AboutMissionSection";
import HomeIntroStrip from "../components/HomeIntroStrip";
import ImpactSection from "../components/ImpactSection";
import ProgramsServicesSection from "../components/ProgramsServicesSection";
import {
  theme04About,
  theme04Hero,
  theme04Impact,
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

      {/* Support GSM Foundation section — replaces StoriesSection */}
      <section
        className="support-gsm-foundation"
        aria-labelledby="support-gsm-foundation-heading"
      >
        <div className="support-gsm-foundation__inner">
          <h2 id="support-gsm-foundation-heading">Support GSM Foundation</h2>
          <div className="support-gsm-foundation__grid">
            <Link to="/support-gsm" className="support-card">
              <span className="support-card__num">01.</span>
              <h3>GSM Foundation</h3>
              <p>Supporting the Manor for over 40 years.</p>
              <span className="support-card__link">Learn more &rarr;</span>
            </Link>
            <Link to="/events" className="support-card">
              <span className="support-card__num">02.</span>
              <h3>Events</h3>
              <p>Fall Festival, Brunch Auction, Golf Invitational, and more.</p>
              <span className="support-card__link">Learn more &rarr;</span>
            </Link>
            <Link to="/shepherd-endowment-society" className="support-card">
              <span className="support-card__num">03.</span>
              <h3>Shepherd Endowment Society</h3>
              <p>Stewardship that outlives a gift.</p>
              <span className="support-card__link">Learn more &rarr;</span>
            </Link>
            <Link to="/support-gsm#memorial-tribute" className="support-card">
              <span className="support-card__num">04.</span>
              <h3>Memorial or Tribute</h3>
              <p>Honor a loved one through giving.</p>
              <span className="support-card__link">Learn more &rarr;</span>
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}

export default HomePage;
