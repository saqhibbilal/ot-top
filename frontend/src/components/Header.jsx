function Header({ statusCounts, totalMachines }) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">OT Analytics Dashboard</h1>
            <p className="mt-1 text-sm text-gray-500">Real-time factory machine monitoring</p>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="text-center">
              <div className="text-2xl font-semibold text-gray-900">{totalMachines}</div>
              <div className="text-xs text-gray-500 uppercase tracking-wide">Machines</div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="text-sm text-gray-600">{statusCounts.info || 0}</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span className="text-sm text-gray-600">{statusCounts.warning || 0}</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span className="text-sm text-gray-600">{statusCounts.critical || 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
