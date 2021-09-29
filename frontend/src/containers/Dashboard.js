import {React,useState,useEffect} from 'react'
import Sidebar from '../components/Sidebar/Sidebar'
import Header from '../components/Header/Header'
import ProductPage from './ProductPage'
import styled from 'styled-components'
import axios from 'axios'
import {
  BrowserRouter as Router,
  Link,
  Route,
  Switch
}from 'react-router-dom'
import BaseRouter from '../routes'


const Container= styled.div`

`
const data =[
  {
    id:1,
    designation:'products1',
  },
  {
    id:2,
    designation:'products2',
  }
]


const Dashboard = () => {
  const [productsList, setProdcutsList] = useState([])
  useEffect(()=>{getProducts()
},'')
const getProducts=()=>{
  axios.get('http://127.0.0.1:8000/api/')
  .then(res=>{setProdcutsList(res.data)

  })
}


    return (
        <>
        <Container>
        <Router> 
        <Header/> 
 
        <Sidebar data={productsList} /> 
        <BaseRouter/>
        </Router> 
        </Container>
          </>
          )
}

export default Dashboard
