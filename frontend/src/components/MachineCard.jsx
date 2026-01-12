function MachineCard({ machine }) {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'border-red-500 bg-red-50'
      case 'warning':
        return 'border-yellow-500 bg-yellow-50'
      default:
        return 'border-green-500 bg-green-50'
    }
  }

  const getSeverityDot = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-500'
      case 'warning':
        return 'bg-yellow-500'
      default:
        return 'bg-green-500'
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleTimeString()
  }

  const formatValue = (value) => {
    if (typeof value === 'boolean') {
      return value ? 'Yes' : 'No'
    }
    return value
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border-2 ${getSeverityColor(machine.latest_severity)} hover:shadow-md transition-shadow duration-200`}>
      <div className="p-5">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{machine.machine_id}</h3>
            <p className="text-sm text-gray-500 mt-1">{machine.machine_type}</p>
          </div>
          <div className={`w-3 h-3 rounded-full ${getSeverityDot(machine.latest_severity)}`}></div>
        </div>

        <div className="space-y-3">
          <div>
            <div className="text-xs text-gray-500 uppercase tracking-wide mb-1">
              {machine.latest_metric}
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {formatValue(machine.latest_value)}
            </div>
          </div>

          <div className="pt-3 border-t border-gray-200">
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-500">Status</span>
              <span className={`font-medium capitalize ${
                machine.latest_severity === 'critical' ? 'text-red-600' :
                machine.latest_severity === 'warning' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {machine.latest_severity}
              </span>
            </div>
            <div className="flex items-center justify-between text-xs mt-2">
              <span className="text-gray-500">Updated</span>
              <span className="text-gray-600">{formatDate(machine.last_update)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MachineCard
