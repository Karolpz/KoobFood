import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home/Home'
import Reservation from './pages/Reservation/Reservation'
import Restaurant from './pages/Restaurant/Restaurant'
import Login from './pages/Login/Login'
import Signup from './pages/Signup/Signup'

const Router = () => {
    return (
        <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/reservation' element={<Reservation />} />
            <Route path='/restaurants' element={<Restaurant />} />
            <Route path='/login' element={<Login />} />
            <Route path='/signup' element={<Signup />} />
        </Routes>
    )
}

export default Router