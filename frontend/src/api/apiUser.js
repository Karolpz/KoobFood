import apiClient from './apiClient'

// Création d'un nouveau utilisateur \\
export const signupUser = async (credentials) => {
    try {
        const response = await apiClient.post('/users/api/signup/', credentials)
        return response.data
    } catch (error) {
        console.error('Error API signing up user:', error)
        throw error
    }
}

// Connexion d'un utilisateur existant \\
export const loginUser = async (credentials) => {
    try {
        const response = await apiClient.post('/users/api/token/', credentials)
        localStorage.setItem('access_token', response.data.access)
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        localStorage.setItem('refresh_token', response.data.refresh)
        return response.data
    } catch (error) {
        console.error('Error API logging in user:', error)
        throw error
    }
}

//Déconnexion d'un utilisateur \\
export const logoutUser = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete apiClient.defaults.headers.common['Authorization']
}