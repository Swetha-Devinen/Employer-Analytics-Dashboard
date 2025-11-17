import React, { useState, useEffect } from 'react'
import FilterBar from '../components/FilterBar'
import { getPredictionAccuracy, getPredictionGaps, getPredictions } from '../api/api'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Cell, ComposedChart, Line } from 'recharts'
import './Predictions.css'

function Predictions() {
  const [filters, setFilters] = useState({})
  const [accuracy, setAccuracy] = useState(null)
  const [gaps, setGaps] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [filters])

  const loadData = async () => {
    setLoading(true)
    try {
      const [accuracyRes, gapsRes] = await Promise.all([
        getPredictionAccuracy(filters),
        getPredictionGaps(filters)
      ])
      
      setAccuracy(accuracyRes.data)
      setGaps(gapsRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  // Categorize gaps
  const gapCategories = {
    Overpaying: gaps.filter(g => g.Category === 'Overpaying').length,
    Competitive: gaps.filter(g => g.Category === 'Competitive').length,
    Underpaying: gaps.filter(g => g.Category === 'Underpaying').length
  }

  const categoryData = Object.entries(gapCategories).map(([name, value]) => ({ name, value }))

  // Scatter plot data (sample for performance)
  const scatterData = gaps.slice(0, 50).map(g => ({
    predicted: g.PredictedSalary,
    actual: g.SalaryMid,
    gap: g.Gap
  }))
  
  // Prepare line data for predicted and actual trends (sorted by predicted for smooth lines)
  const sortedData = [...scatterData].sort((a, b) => a.predicted - b.predicted)

  if (loading) {
    return <div className="loading">Loading predictions...</div>
  }

  return (
    <div className="predictions-page">
      <div className="page-header">
        <h1>Salary Predictions</h1>
      </div>

      <FilterBar onFilterChange={setFilters} filters={filters} />

      {/* Accuracy Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Mean Absolute Error</div>
          <div className="metric-value">${accuracy ? Math.round(accuracy.mae).toLocaleString() : 0}</div>
          <div className="metric-desc">Average prediction error</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Mean Absolute % Error</div>
          <div className="metric-value">{accuracy ? accuracy.mape.toFixed(2) : 0}%</div>
          <div className="metric-desc">Percentage error</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">R² Score</div>
          <div className="metric-value">{(accuracy ? accuracy.r2 * 100 : 0).toFixed(1)}%</div>
          <div className="metric-desc">Model accuracy</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Predictions</div>
          <div className="metric-value">{accuracy ? accuracy.count : 0}</div>
          <div className="metric-desc">Total predictions</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Predicted vs Actual Scatter */}
        <div className="chart-card full-width">
          <h3>Predicted vs Actual Salary</h3>
          <ResponsiveContainer width="100%" height={400}>
            <ComposedChart data={sortedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number" 
                dataKey="predicted" 
                name="Predicted"
                label={{ value: 'Predicted Salary ($)', position: 'insideBottom', offset: -5 }}
                domain={['dataMin', 'dataMax']}
              />
              <YAxis 
                type="number" 
                name="Actual"
                label={{ value: 'Actual Salary ($)', angle: -90, position: 'insideLeft' }}
                domain={['dataMin', 'dataMax']}
              />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }}
                formatter={(value, name) => [`$${value.toLocaleString()}`, name]}
              />
              <Legend />
              {/* Green line for Predicted trend */}
              <Line 
                type="monotone" 
                dataKey="predicted" 
                stroke="#2ca02c" 
                strokeWidth={2}
                dot={false}
                name="Predicted"
              />
              {/* Blue line for Actual trend */}
              <Line 
                type="monotone" 
                dataKey="actual" 
                stroke="#1f77b4" 
                strokeWidth={2}
                dot={false}
                name="Actual"
              />
              {/* Scatter points with original color coding */}
              <Scatter name="Predictions" dataKey="actual" fill="#1f77b4">
                {sortedData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.gap > 0 ? '#2ca02c' : entry.gap < -10000 ? '#d62728' : '#1f77b4'} />
                ))}
              </Scatter>
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* Gap Categories */}
        <div className="chart-card">
          <h3>Prediction Gap Categories</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#1f77b4">
                {categoryData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.name === 'Overpaying' ? '#2ca02c' : entry.name === 'Underpaying' ? '#d62728' : '#1f77b4'} 
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Gaps Table */}
      <div className="table-card">
        <h3>Top Prediction Gaps</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Role</th>
                <th>Location</th>
                <th>Predicted</th>
                <th>Actual</th>
                <th>Gap</th>
                <th>Gap %</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              {gaps
                .sort((a, b) => Math.abs(b.Gap) - Math.abs(a.Gap))
                .slice(0, 10)
                .map((gap, idx) => (
                  <tr key={idx}>
                    <td>{gap.JobTitle}</td>
                    <td>{gap.Location}</td>
                    <td>${gap.PredictedSalary.toLocaleString()}</td>
                    <td>${gap.SalaryMid.toLocaleString()}</td>
                    <td className={gap.Gap > 0 ? 'positive' : 'negative'}>
                      ${Math.abs(gap.Gap).toLocaleString()}
                    </td>
                    <td>{gap.GapPct.toFixed(1)}%</td>
                    <td>
                      <span className={`badge badge-${gap.Category.toLowerCase()}`}>
                        {gap.Category}
                      </span>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Predictions


