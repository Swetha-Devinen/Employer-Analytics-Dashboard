import React, { useState, useEffect } from 'react'
import KPICard from '../components/KPICard'
import FilterBar from '../components/FilterBar'
import { getOverviewKPIs, getTopSkills, getSalaryByRole, getSalaryTrends } from '../api/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, Cell } from 'recharts'
import './Home.css'

function Home() {
  const [filters, setFilters] = useState({})
  const [kpis, setKpis] = useState(null)
  const [topSkills, setTopSkills] = useState([])
  const [salaryByRole, setSalaryByRole] = useState([])
  const [salaryTrends, setSalaryTrends] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [filters])

  const loadData = async () => {
    setLoading(true)
    try {
      const [kpisRes, skillsRes, roleRes, trendsRes] = await Promise.all([
        getOverviewKPIs(filters),
        getTopSkills(filters),
        getSalaryByRole(filters),
        getSalaryTrends(filters)
      ])
      
      setKpis(kpisRes.data)
      setTopSkills(skillsRes.data.slice(0, 10))
      setSalaryByRole(roleRes.data.slice(0, 10))
      setSalaryTrends(trendsRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
      // Show error message to user
      if (error.response) {
        console.error('API Error:', error.response.status, error.response.data)
      } else if (error.request) {
        console.error('Network Error: Backend may not be running')
      }
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']

  if (loading) {
    return (
      <div className="loading">
        <div>Loading dashboard...</div>
        <div style={{ fontSize: '0.9rem', color: '#7f8c8d', marginTop: '1rem' }}>
          If this takes too long, check that the backend is running on port 5000
        </div>
      </div>
    )
  }

  // Show error if no data loaded
  if (!kpis && !salaryByRole.length && !topSkills.length) {
    return (
      <div className="loading">
        <div style={{ color: '#d62728', fontSize: '1.2rem', marginBottom: '1rem' }}>
          ⚠️ Unable to load data
        </div>
        <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>
          Please check:
          <ul style={{ textAlign: 'left', display: 'inline-block', marginTop: '0.5rem' }}>
            <li>Backend server is running (http://localhost:5000)</li>
            <li>Check browser console (F12) for errors</li>
            <li>Check Network tab for failed API calls</li>
          </ul>
        </div>
      </div>
    )
  }

  return (
    <div className="home-page">
      <div className="page-header">
        <h1>Dashboard Overview</h1>
        <p>Salary & Compensation Intelligence at a Glance</p>
      </div>

      <FilterBar onFilterChange={setFilters} filters={filters} />

      {/* KPI Cards */}
      <div className="kpi-grid">
        <KPICard
          title="Total Jobs"
          value={kpis?.total_jobs || 0}
          subtitle="Distinct job postings"
          icon="📋"
          color="blue"
          format="number"
        />
        <KPICard
          title="Highest Paying Role"
          value={kpis?.highest_paying_role || 'N/A'}
          subtitle={kpis?.highest_paying_salary ? `$${Math.round(kpis.highest_paying_salary).toLocaleString()}/year` : 'No data'}
          icon="💎"
          color="green"
          format="text"
        />
        <KPICard
          title="Average Salary"
          value={kpis?.average_salary || 0}
          subtitle="Yearly compensation (filtered)"
          icon="💰"
          color="orange"
          format="currency"
        />
        <KPICard
          title="Average Experience Level"
          value={kpis?.average_experience_level ? kpis.average_experience_level.toFixed(1) : '0'}
          subtitle="On a scale of 1-5"
          icon="📊"
          color="purple"
          format="number"
        />
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Salary Distribution by Role */}
        <div className="chart-card">
          <h3>Top 10 Roles by Salary</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salaryByRole}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="JobTitle" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Legend />
              <Bar dataKey="average" fill="#1f77b4" name="Average Salary" />
              <Bar dataKey="median" fill="#2ca02c" name="Median Salary" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top 10 Skills by Demand */}
        <div className="chart-card">
          <h3>Top 10 Skills by Demand</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={topSkills} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis 
                dataKey="skill" 
                type="category" 
                width={150}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                formatter={(value, name) => [
                  `${value} jobs`,
                  'Job Count'
                ]}
                labelFormatter={(label) => `Skill: ${label}`}
              />
              <Bar dataKey="frequency" fill="#2ca02c" name="Job Count">
                {topSkills.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          {/* Skills Summary Table */}
          {topSkills.length > 0 && (
            <div className="skills-summary">
              <table className="skills-summary-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Skill</th>
                    <th>Job Count</th>
                    <th>Avg Salary</th>
                  </tr>
                </thead>
                <tbody>
                  {topSkills.map((skill, index) => (
                    <tr key={skill.skill}>
                      <td><strong>#{index + 1}</strong></td>
                      <td>{skill.skill}</td>
                      <td>{skill.frequency.toLocaleString()}</td>
                      <td>${skill.average_salary ? Math.round(skill.average_salary).toLocaleString() : 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Salary Trends Over Time */}
        <div className="chart-card full-width">
          <h3>Salary Trends Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={salaryTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="YearMonth" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Legend />
              <Line type="monotone" dataKey="average" stroke="#1f77b4" strokeWidth={2} name="Average Salary" />
              <Line type="monotone" dataKey="median" stroke="#2ca02c" strokeWidth={2} name="Median Salary" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default Home


