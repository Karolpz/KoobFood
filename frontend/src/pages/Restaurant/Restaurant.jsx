import React from 'react'
import { getRestaurants } from '../../api/apiRestaurant'
import { useEffect, useState } from 'react'
import { data } from 'react-router-dom'

const Restaurant = () => {

  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const restaurants = await getRestaurants()
        setRestaurants(restaurants)
      } catch (error) {
        setError(error)
      } finally {
        setLoading(false)
      }

    }
    fetchRestaurants();
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>{error.message}</p>

  return (
    <section className="restaurant-list">
      <h2>Liste des Restaurants</h2>
      {restaurants.map((restaurant) => (
        <div key={restaurant.id} className="restaurant-card">
          <ul>
            <li><h3>{restaurant.name}</h3></li>
            <p>{restaurant.description}</p>
            <p>Localisation: {restaurant.location}</p>
            <p>Téléphone: {restaurant.phone_number}</p>
          </ul>
        </div>
      ))}
    </section>
  )
}

export default Restaurant