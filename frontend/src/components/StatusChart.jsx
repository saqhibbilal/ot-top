import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

function StatusChart({ machines }) {
  // Calculate status distribution
  const statusCounts = { info: 0, warning: 0, critical: 0 }
  
  machines.forEach(m => {
    statusCounts[m.latest_severity] = (statusCounts[m.latest_severity] || 0) + 1
  })

  const data = [
    { name: 'Info', value: statusCounts.info, color: '#10b981' },
    { name: 'Warning', value: statusCounts.warning, color: '#eab308' },
    { name: 'Critical', value: statusCounts.critical, color: '#ef4444' }
  ]

  const COLORS = ['#10b981', '#eab308', '#ef4444']

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Status Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export default StatusChart
