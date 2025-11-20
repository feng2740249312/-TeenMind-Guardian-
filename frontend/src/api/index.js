import axios from 'axios'

const api = axios.create({
  baseURL: import.meta?.env?.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => Promise.reject(err)
)

export const getDashboardData = (userId, days) => api.get(`/api/users/${userId}/dashboard`, { params: { days } })
export const analyzeEmotion = (text, userId) => api.post('/api/analysis/emotion', { text, user_id: userId })
export default api
