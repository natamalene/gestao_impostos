import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import { Dashboard } from './pages/Dashboard'
import { Properties } from './pages/Properties'
import { PropertyDetails } from './pages/PropertyDetails'
import { TaxCalculator } from './pages/TaxCalculator'
import { PropertyRegistration } from './pages/PropertyRegistration'
import { TaxSimulation } from './pages/TaxSimulation'
import { DataImport } from './pages/DataImport'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/properties" element={<Properties />} />
            <Route path="/properties/:id" element={<PropertyDetails />} />
            <Route path="/calculator" element={<TaxCalculator />} />
            <Route path="/register" element={<PropertyRegistration />} />
            <Route path="/simulation" element={<TaxSimulation />} />
            <Route path="/import" element={<DataImport />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
