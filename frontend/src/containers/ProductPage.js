import { RecentActors } from '@material-ui/icons'
import axios from 'axios'
import {React,  useState,useEffect } from 'react'
import styled from 'styled-components'
import { BarChart } from '../components/Chart/Chart'
import TableConrainer from '../components/Table/TableContainer'



const structure= [
    {
        date:"Janvier 2020",
        ActualSale:200,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"février 2020",
        ActualSale:200,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Mars 2020",
        ActualSale:100,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Avril 2020",
        ActualSale:200,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Mai 2020",
        ActualSale:200,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"Juin 2020",
        ActualSale:200,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Juillet 2020",
        ActualSale:100,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Aout 2020",
        ActualSale:124,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Septembre 2020",
        ActualSale:245,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Octobre 2020",
        ActualSale:200,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"Novembre 2020",
        ActualSale:200,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Decembre 2020",
        ActualSale:100,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Janvier 2021",
        ActualSale:200,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"février 2021",
        ActualSale:200,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Mars 2021",
        ActualSale:100,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Avril 2021",
        ActualSale:111,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Mai 2021",
        ActualSale:210,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"Juin 2021",
        ActualSale:200,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Juillet 2021",
        ActualSale:100,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Aout 2021",
        ActualSale:200,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Septembre 2021",
        ActualSale:356,
        ForcastedSale:310,
        AjustementSale:null,
    },
    {
        date:"Octobre 2021",
        ActualSale:null,
        ForcastedSale:300,
        AjustementSale:null,
    },
    {
        date:"Novembre 2021",
        ActualSale:null,
        ForcastedSale:350,
        AjustementSale:null,
    },
    {
        date:"Decembre 2021",
        ActualSale:null,
        ForcastedSale:310,
        AjustementSale:null,
    },


]




const chartData = {
    labels: structure.map((item) => item.date),
    datasets: [{
    label: "Ventes actuels",
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: structure.map((item) => item.ActualSale),
    fill: false, 
    },
    {
        label: "Prévision",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 30, 132)',
        data: structure.map((item) => item.ForcastedSale),
        fill: false,}

        

  
],
}

const Container = styled.div`
position: fixed;
top:0;
bottom:0;
left: 0;
overflow: hide;
right: 0;
padding-top:8rem;
padding-left: 16rem;

color: ${({theme})=> theme.textColor };

`

function ProductPage(props){
const  [actualSales,setActualSales]=useState([])
const  [forecastedSales,setForecastedSales]=useState([])
const  [adjustedSales,setAdjustedSales]=useState([])

const getActualSales=()=>{
    axios.get(`http://127.0.0.1:8000/api/salesActual/${props.match.params.productID}/`)
        .then(res=>{
          setActualSales(res.data);
          console.log(res.data)
        })


}


useEffect(() => {
    getActualSales()

},props.match.params.productID)

const chartData = {
    labels: actualSales.map((item) => item.date),
    datasets: [{
    label: "Ventes actuels",
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: actualSales.map((item) => item.quantity),
    fill: false, 
    },


        

  
],
}

    
        return (
            <Container>
               <TableConrainer actualSales={actualSales}/>
               <BarChart data ={chartData}/>
            </Container>
        )

    }


export default ProductPage
