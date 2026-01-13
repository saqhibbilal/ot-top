function StatsTable({ machines }) {
  // Calculate aggregated statistics
  const stats = {
    total: machines.length,
    byType: {},
    bySeverity: { info: 0, warning: 0, critical: 0 },
    byMetric: {}
  }

  machines.forEach(machine => {
    // Count by type
    stats.byType[machine.machine_type] = (stats.byType[machine.machine_type] || 0) + 1
    
    // Count by severity
    stats.bySeverity[machine.latest_severity] = (stats.bySeverity[machine.latest_severity] || 0) + 1
    
    // Count by metric type
    stats.byMetric[machine.latest_metric] = (stats.byMetric[machine.latest_metric] || 0) + 1
  })

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-50'
      case 'warning': return 'text-yellow-600 bg-yellow-50'
      default: return 'text-green-600 bg-green-50'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 className="text-lg font-semibold text-gray-900">Aggregated Statistics</h2>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* By Severity */}
          <div>
            <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">By Severity</h3>
            <div className="space-y-2">
              {Object.entries(stats.bySeverity).map(([severity, count]) => (
                <div key={severity} className="flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getSeverityColor(severity)}`}>
                    {severity}
                  </span>
                  <span className="text-lg font-semibold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* By Machine Type */}
          <div>
            <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">By Machine Type</h3>
            <div className="space-y-2">
              {Object.entries(stats.byType).map(([type, count]) => (
                <div key={type} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">{type}</span>
                  <span className="text-lg font-semibold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* By Metric Type */}
          <div>
            <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">Top Metrics</h3>
            <div className="space-y-2">
              {Object.entries(stats.byMetric)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([metric, count]) => (
                  <div key={metric} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 truncate">{metric.replace('_', ' ')}</span>
                    <span className="text-lg font-semibold text-gray-900">{count}</span>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Summary Row */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-500">Total Machines</span>
            <span className="text-2xl font-bold text-gray-900">{stats.total}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsTable
