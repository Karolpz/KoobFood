import React from 'react'
import Logo from '../../../public/images/logo-koobfood.png'
import Navbar from '../../components/Navbar/Navbar'

const Header = () => {
    
    const item = [
        { name: 'Accueil', link: '/' }, 
        { name: 'Restaurants', link: '/restaurants' }, 
        { name: 'Se connecter', link: '/login' },
        { name: 'S\'inscrire', link: '/signup' }
    ]

  return (
    <header className="header">
        <div className="header__logo">
        <img src={Logo} alt="KoobFood Logo" />
          </div>
        <div className="header__navbar">
            <Navbar 
            items={item}/>
        </div>
    </header>
  )
}

export default Header