import { Link } from "react-router-dom";
import { stories } from "../data/site";
import { LOREM, LOREM_LONG, LOREM_SHORT } from "../data/placeholders";
import AboutMissionSection from "../components/AboutMissionSection";
import HomeIntroStrip from "../components/HomeIntroStrip";
import ImpactSection from "../components/ImpactSection";
import ProgramsServicesSection from "../components/ProgramsServicesSection";
import readMoreArrow from "../assets/home-stories/read-more-arrow.svg";
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

      <section className="home-donate-cta">
        <div className="home-donate-cta__inner">
          <h2>We can create a better tomorrow</h2>
          <p>{LOREM}</p>
          <Link to="/ways-to-give" className="home-btn home-btn--blue">
            Donate Now
          </Link>
        </div>
      </section>

      <ProgramsServicesSection />

      <section className="home-stories" aria-label="Stories">
        <div className="home-stories__inner">
          <header className="home-stories__header">
            <div className="home-stories__intro">
              <h2>What&rsquo;s Happening at GSM</h2>
              <p>{LOREM}</p>
            </div>
            <Link to="/events" className="home-stories__more">
              See all events &rarr;
            </Link>
          </header>

          <div className="home-stories__cards">
            {stories.map((story, index) => (
              <article
                className={`home-stories__card${index === 0 ? " home-stories__card--left" : " home-stories__card--right"}`}
                key={story.path}
              >
                <div className="home-stories__card-inner">
                  <div className="home-stories__photo" aria-hidden="true" />
                  <div className="home-stories__copy">
                    <h3>{story.title}</h3>
                    <p>{LOREM_SHORT}</p>
                  </div>
                  <Link to={story.path} className="home-stories__link">
                    Read More
                    <img
                      className="home-stories__link-icon"
                      src={readMoreArrow}
                      alt=""
                      aria-hidden="true"
                    />
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
