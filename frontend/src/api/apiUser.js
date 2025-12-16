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