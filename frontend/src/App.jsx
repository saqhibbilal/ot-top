import { useState, useEffect } from 'react'
import axios from 'axios'
import MachineCard from './components/MachineCard'
import Header from './components/Header'
import StatsTable from './components/StatsTable'
import StatusChart from './components/StatusChart'
import MachineTypeChart from './components/MachineTypeChart'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [machines, setMachines] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchMachines = async () => {
    try {
      const response = await axios.get(`${API_URL}/machines`)
      setMachines(response.data.machines || [])
      setError(null)
    } catch (err) {
      setError('Failed to fetch machines')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMachines()
    // Refresh every 5 seconds
    const interval = setInterval(fetchMachines, 5000)
    return () => clearInterval(interval)
  }, [])

  const getStatusCounts = () => {
    const counts = { info: 0, warning: 0, critical: 0 }
    machines.forEach(m => {
      counts[m.latest_severity] = (counts[m.latest_severity] || 0) + 1
    })
    return counts
  }

  const statusCounts = getStatusCounts()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header statusCounts={statusCounts} totalMachines={machines.length} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600">Loading machines...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {!loading && !error && machines.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No machines found</p>
          </div>
        )}

        {!loading && !error && machines.length > 0 && (
          <>
            {/* Charts Section */}
            <div className="mb-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StatusChart machines={machines} />
              <MachineTypeChart machines={machines} />
            </div>

            {/* Stats Table */}
            <div className="mb-8">
              <StatsTable machines={machines} />
            </div>

            {/* Machine Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {machines.map((machine) => (
                <MachineCard key={machine.machine_id} machine={machine} />
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default App
