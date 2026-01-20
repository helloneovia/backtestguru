// Configuration de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000')

export const API_URL = API_BASE_URL
