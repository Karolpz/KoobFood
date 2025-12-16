import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import Router from './Router.jsx'
import Header from './layout/Header/Header.jsx'
import Footer from './layout/Footer/Footer.jsx'

const App = () => {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Router />
      </main>
      <Footer />
    </BrowserRouter>
  )
}

export default App