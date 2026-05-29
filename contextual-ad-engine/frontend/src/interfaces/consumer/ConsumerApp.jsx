import { Routes, Route } from 'react-router-dom';
import { PersonaProvider } from '../../context/PersonaContext';
import FeedPage from './pages/FeedPage';

export default function ConsumerApp() {
  return (
    <PersonaProvider>
      <Routes>
        <Route index element={<FeedPage />} />
      </Routes>
    </PersonaProvider>
  );
}
