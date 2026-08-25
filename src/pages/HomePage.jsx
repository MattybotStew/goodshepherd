import { Link } from "react-router-dom";
import AboutMissionSection from "../components/AboutMissionSection";
import DonateCta from "../components/DonateCta";
import HomeIntroStrip from "../components/HomeIntroStrip";
import ImpactSection from "../components/ImpactSection";
import SplitSection from "../components/SplitSection";
import StoriesSection from "../components/StoriesSection";
import {
  theme04About,
  theme04DonateCta,
  theme04GetInvolved,
  theme04Hero,
  theme04Impact,
  theme04Stories,
} from "../data/theme04Home";
import { lifeImages } from "../data/lifeImages";
import "./HomePage.css";

const storyItems = theme04Stories.items.map((item, index) => ({
  ...item,
  image: lifeImages.stories[index],
}));

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

      <HomeIntroStrip variant="theme04" />

      <AboutMissionSection
        showReadMore
        eyebrow={theme04About.eyebrow}
        title={theme04About.title}
        paragraphs={theme04About.paragraphs}
        mosaicImages={lifeImages.aboutMosaic}
      />

      <ImpactSection
        eyebrow={theme04Impact.eyebrow}
        title={theme04Impact.title}
        lede={theme04Impact.lede}
        stats={theme04Impact.stats}
      />

      <DonateCta title={theme04DonateCta.title} lede="" />

      <SplitSection
        eyebrow={theme04GetInvolved.eyebrow}
        title={theme04GetInvolved.title}
        flip
        imageSrc={lifeImages.getInvolved}
        linkTo={theme04GetInvolved.linkPath}
        linkLabel={`${theme04GetInvolved.linkLabel} →`}
      >
        {theme04GetInvolved.paragraphs.map((text) => (
          <p key={text.slice(0, 24)}>{text}</p>
        ))}
      </SplitSection>

      <StoriesSection
        items={storyItems}
        title={theme04Stories.title}
        lede={theme04Stories.lede}
        align="center"
      />
    </div>
  );
}

export default HomePage;
