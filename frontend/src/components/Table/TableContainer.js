import React from 'react'
import Table from './Table'
import Datepicker from './DatePicker'
import axios from 'axios'

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


const dateDiff = ([y,m],delta)=>{
    if (delta>0){
        m=m+delta
        var x=Math.floor(m/12)
        var mod= m%12
        return [y+x,mod]
    
    }else{
        m=m+delta
        if (m<0){
            y=y-1
            var x=Math.floor(-m/12)
            var mod= -m%12
            return [y-x,12-mod]
        }else{
            return[y,m]
        }
    }
   
}

class TableContainer extends React.Component {
    state={
        dateDebut:[2020,9],
        dateFin:[2021,5],
    }
    handledecrementDate=()=>{
        this.setState({
            dateDebut:dateDiff([this.state.dateDebut[0],this.state.dateDebut[1]],-18),
            dateFin:dateDiff([this.state.dateFin[0],this.state.dateFin[1]],-18)
        })
    }
    handleincrementDate=()=>{
        this.setState({
            dateDebut:dateDiff([this.state.dateDebut[0],this.state.dateDebut[1]],18),
            dateFin:dateDiff([this.state.dateFin[0],this.state.dateFin[1]],18)
        })
    }

    render(){
        return(
            <>
            <Datepicker handledecrementDate={this.handledecrementDate} handleincrementDate={this.handleincrementDate} dateDebut={this.state.dateDebut} dateFin={this.state.dateFin}/>
            <Table actualSales={this.props.actualSales} dateDebut={this.state.dateDebut} dateFin={this.state.dateFin}  />
            </>
        )
    }
}

export default TableContainer
