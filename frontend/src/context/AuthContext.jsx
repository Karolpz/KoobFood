import { createContext, useState, useEffect } from 'react'
import { loginUser, logoutUser } from '../api/apiUser'
import apiClient from '../api/apiClient'

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const fetchUserProfile = async () => {
        try {
            const response = await apiClient.get('/users/api/me/')
            setUser(response.data)
        } catch (error) {
            console.error("Erreur profil:", error)
            logout()
        }
    }

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('access_token')
            if (token) {
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
                await fetchUserProfile()
            }
            setLoading(false)
        }
        checkAuth()
    }, [])

    const login = async (credentials) => {
        setLoading(true)
        setError(null)
        try {
            await loginUser(credentials)
            await fetchUserProfile()  
        } catch (err) {
            setError(err)
            throw err
        } finally {
            setLoading(false)
        }
    }

    const logout = () => {
        logoutUser() 
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, error, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}