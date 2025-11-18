import React, { useState, useEffect } from 'react'
import FilterBar from '../components/FilterBar'
import { getSalaryByRole, getSalaryByLocation, getTopSkills } from '../api/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, Cell } from 'recharts'
import './SalaryOverview.css'

function SalaryOverview() {
  const [filters, setFilters] = useState({})
  const [salaryByRole, setSalaryByRole] = useState([])
  const [salaryByLocation, setSalaryByLocation] = useState([])
  const [topSkills, setTopSkills] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [filters])

  const loadData = async () => {
    setLoading(true)
    try {
      const [roleRes, locationRes, skillsRes] = await Promise.all([
        getSalaryByRole(),
        getSalaryByLocation(),
        getTopSkills()
      ])
      
      setSalaryByRole(roleRes.data)
      setSalaryByLocation(locationRes.data)
      setTopSkills(skillsRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading salary data...</div>
  }

  return (
    <div className="salary-overview-page">
      <div className="page-header">
        <h1>Salary Overview</h1>
        <p>Market Salary Insights by Role, Location, and Skills</p>
      </div>

      <FilterBar onFilterChange={setFilters} filters={filters} />

      <div className="charts-grid">
        {/* Salary by Role */}
        <div className="chart-card full-width">
          <h3>Average Salary by Role</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={salaryByRole.slice(0, 15)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="JobTitle" 
                angle={-45} 
                textAnchor="end" 
                height={120}
              />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Legend />
              <Bar dataKey="average" fill="#1f77b4" name="Average" />
              <Bar dataKey="median" fill="#2ca02c" name="Median" />
              <Bar dataKey="min" fill="#ff7f0e" name="Min" />
              <Bar dataKey="max" fill="#d62728" name="Max" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Salary by Location */}
        <div className="chart-card">
          <h3>Average Salary by Location</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salaryByLocation}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Location" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Bar dataKey="average" fill="#1f77b4" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Skills by Salary Impact */}
        <div className="chart-card">
          <h3>Top Skills by Average Salary</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topSkills.slice(0, 10)} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="skill" type="category" width={120} />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Bar dataKey="average_salary" fill="#9467bd" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default SalaryOverview



