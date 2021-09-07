import React from 'react'
import Sidebar from '../components/Sidebar/Sidebar'
import Header from '../components/Header/Header'
import ProductPage from './ProductPage'
import styled from 'styled-components'


const Container= styled.div`

`


const Dashboard = () => {
    return (
        <>
        <Container>
        <Header/>  
        <Sidebar/> 
        <ProductPage/>
        </Container>


          </>
          )
}

export default Dashboard
