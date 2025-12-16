import apiClient from "./apiClient"

// Recupérer tous les restarants \\
export const getRestaurants = async () => {
    try {
        const response = await apiClient.get('/restaurant/api');
        return response.data;
    } catch (error) {
        console.error('Error fetching restaurants:', error);
        throw error;
    }
}