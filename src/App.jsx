import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import SitemapPage from './pages/SitemapPage'
import AboutPage from './pages/AboutPage'
import ProgramsPage from './pages/ProgramsPage'
import CommunityDayPage from './pages/CommunityDayPage'
import VocationalPage from './pages/VocationalPage'
import SpecialOlympicsPage from './pages/SpecialOlympicsPage'
import ResidentialPage from './pages/ResidentialPage'
import HealthWellBeingPage from './pages/HealthWellBeingPage'
import FoundationPage from './pages/FoundationPage'
import EndowmentPage from './pages/EndowmentPage'
import EventsPage from './pages/EventsPage'
import NewsPage from './pages/NewsPage'
import NewsArticlePage from './pages/NewsArticlePage'
import NewslettersPage from './pages/NewslettersPage'
import CareersPage from './pages/CareersPage'
import ContactPage from './pages/ContactPage'
import PrivacyPage from './pages/PrivacyPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Routes>
        <Route path="/sitemap" element={<SitemapPage />} />
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/programs" element={<ProgramsPage />} />
          <Route path="/programs/community-day-services" element={<CommunityDayPage />} />
          <Route path="/programs/vocational" element={<VocationalPage />} />
          <Route path="/programs/special-olympics" element={<SpecialOlympicsPage />} />
          <Route path="/programs/residential-living" element={<ResidentialPage />} />
          <Route path="/programs/health-well-being" element={<HealthWellBeingPage />} />
          <Route path="/support-gsm" element={<FoundationPage />} />
          <Route path="/shepherd-endowment-society" element={<EndowmentPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/news" element={<NewsPage />} />
          <Route path="/news/:slug" element={<NewsArticlePage />} />
          <Route path="/newsletters" element={<NewslettersPage />} />
          <Route path="/careers" element={<CareersPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
