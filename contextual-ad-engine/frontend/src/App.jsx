import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ConsumerApp from './interfaces/consumer/ConsumerApp.jsx'
import BrandApp from './interfaces/brand/BrandApp.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/consumer/*" element={<ConsumerApp />} />
        <Route path="/brand/*" element={<BrandApp />} />
        <Route path="/" element={<Navigate to="/consumer" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
