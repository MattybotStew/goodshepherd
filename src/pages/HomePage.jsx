import { Link } from "react-router-dom";
import { LOREM_LONG } from "../data/placeholders";
import AboutMissionSection from "../components/AboutMissionSection";
import DonateCta from "../components/DonateCta";
import HomeIntroStrip from "../components/HomeIntroStrip";
import ImpactSection from "../components/ImpactSection";
import ProgramsServicesSection from "../components/ProgramsServicesSection";
import StoriesSection from "../components/StoriesSection";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="home">
      <section className="home-hero">
        <div className="home-hero__photo" aria-hidden="true" />
        <div className="home-hero__inner">
          <h1>A Community of Compassion, Dignity, and Purpose.</h1>
          <p>{LOREM_LONG}</p>
          <Link to="/careers" className="home-btn home-btn--blue">
            Now Hiring! Apply Today
          </Link>
        </div>
      </section>

      <HomeIntroStrip variant="home" />

      <ImpactSection />

      <AboutMissionSection />

      <DonateCta />

      <ProgramsServicesSection />

      <StoriesSection
        moreTo="/events"
        moreLabel="See all events →"
      />
    </div>
  );
}

export default HomePage;
