import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Job Postings
export const getJobPostings = (filters = {}) => {
  return api.get('/job-postings', { params: filters })
}

// Predictions
export const getPredictions = (filters = {}) => {
  return api.get('/predictions', { params: filters })
}

// Analytics
export const getSalarySummary = (filters = {}) => {
  return api.get('/analytics/salary-summary', { params: filters })
}

export const getOverviewKPIs = (filters = {}) => {
  return api.get('/analytics/overview-kpis', { params: filters })
}

export const getPredictionAccuracy = (filters = {}) => {
  return api.get('/analytics/prediction-accuracy', { params: filters })
}

export const getCompensationDistribution = () => {
  return api.get('/analytics/compensation-distribution')
}

export const getSalaryByRole = (filters = {}) => {
  return api.get('/analytics/salary-by-role', { params: filters })
}

export const getSalaryByLocation = (filters = {}) => {
  return api.get('/analytics/salary-by-location', { params: filters })
}

export const getSalaryTrends = (filters = {}) => {
  return api.get('/analytics/salary-trends', { params: filters })
}

export const getPredictionGaps = (filters = {}) => {
  return api.get('/analytics/prediction-gaps', { params: filters })
}

export const getBenchmarking = () => {
  return api.get('/analytics/benchmarking')
}

export const getTopSkills = (filters = {}) => {
  return api.get('/analytics/top-skills', { params: filters })
}

// Filters
export const getRoles = () => {
  return api.get('/filters/roles')
}

export const getLocations = () => {
  return api.get('/filters/locations')
}

export const getCompensationTypes = () => {
  return api.get('/filters/compensation-types')
}

// Predict
export const predictSalary = (data) => {
  return api.post('/predict', data)
}

export default api

