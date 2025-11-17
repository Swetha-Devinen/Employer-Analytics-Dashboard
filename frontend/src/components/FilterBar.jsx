import React, { useState, useEffect } from 'react'
import { getRoles, getLocations, getCompensationTypes } from '../api/api'
import './FilterBar.css'

function FilterBar({ onFilterChange, filters = {} }) {
  const [localFilters, setLocalFilters] = useState({
    role: filters.role || '',
    location: filters.location || '',
    compensation_type: filters.compensation_type || ''
  })
  
  const [options, setOptions] = useState({
    roles: [],
    locations: [],
    compensationTypes: []
  })

  useEffect(() => {
    // Load filter options
    Promise.all([
      getRoles(),
      getLocations(),
      getCompensationTypes()
    ]).then(([rolesRes, locationsRes, compTypesRes]) => {
      setOptions({
        roles: rolesRes.data,
        locations: locationsRes.data,
        compensationTypes: compTypesRes.data
      })
    })
  }, [])

  const handleFilterChange = (key, value) => {
    const newFilters = { ...localFilters, [key]: value }
    setLocalFilters(newFilters)
    onFilterChange(newFilters)
  }

  const clearFilters = () => {
    const cleared = { role: '', location: '', compensation_type: '' }
    setLocalFilters(cleared)
    onFilterChange(cleared)
  }

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label>Role</label>
        <select
          value={localFilters.role}
          onChange={(e) => handleFilterChange('role', e.target.value)}
        >
          <option value="">All Roles</option>
          {options.roles.map(role => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <label>Location</label>
        <select
          value={localFilters.location}
          onChange={(e) => handleFilterChange('location', e.target.value)}
        >
          <option value="">All Locations</option>
          {options.locations.map(location => (
            <option key={location} value={location}>{location}</option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <label>Compensation Type</label>
        <select
          value={localFilters.compensation_type}
          onChange={(e) => handleFilterChange('compensation_type', e.target.value)}
        >
          <option value="">All Types</option>
          {options.compensationTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>
      
      <button className="clear-filters" onClick={clearFilters}>
        Clear Filters
      </button>
    </div>
  )
}

export default FilterBar


