import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Upload from './components/Upload'
import Dashboard from './components/Dashboard'
import AnalysisResults from './components/AnalysisResults'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analysis/:fileId" element={<AnalysisResults />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
