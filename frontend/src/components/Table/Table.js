import React from 'react'
import styled from 'styled-components'
import axios from 'axios';
import IconButton from '@material-ui/core/IconButton';
import ArrowBackIosRoundedIcon from '@material-ui/icons/ArrowBackIosRounded';
import ArrowForwardIosRoundedIcon from '@material-ui/icons/ArrowForwardIosRounded';
import ChevronLeftRoundedIcon from '@material-ui/icons/ChevronLeftRounded';
import { dateRange } from '../../helper';

const Container = styled.div`

`;
const TableStyled = styled.table`
border-collapse: collapse;
font-style: normal;
font-size: 12px;
width: 100%;
`;
const Th = styled.th`
    padding: 0px 20px;
    font-weight: inherit;
    
    background-color:${({theme})=> theme.secondary};;
;

  text-align: left;
  padding: 8px;
`;
const Tr = styled.tr`

border: 1px solid #dddddd;
border-color: ${({theme})=> theme.secondary};;
  text-align: left;
  padding: 8px;
`;

const Td = styled.td`
border: 1px solid #dddddd;
color: white;
border-color: ${({theme})=> theme.secondary};;
;
  text-align: left;
  padding: 8px;
`;
const Icon = styled.div`
display: inline;
color:${({theme})=> theme.secondary};

`

const TdActual = styled.td`
color: white;
border: 1px solid #dddddd;
border-color: ${({theme})=> theme.secondary};;
;
background-color:rgba(255, 241, 113, 0.25);
  text-align: left;
  padding: 8px;
`;
const Header = styled.td`
  text-align: left;
  padding: 8px;
  background-color:${({theme})=> theme.secondary};
  color: ${({theme})=> theme.textColor };
  border: 1px solid #dddddd;
  border-color: ${({theme})=> theme.secondary};;

`;
const DateFilter = styled.div`
float: right;
font-style: normal;
font-size: 12px;
`

class Table extends React.Component{
  
    render()
    {  const months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"];
        const dates = dateRange(this.props.dateDebut,this.props.dateFin)
        
        return (

            <Container>

                  <TableStyled>
                 <Th >  </Th>
                {
                    dates.map((item)=>{
                        return(
                            <Th > {item} </Th>
                        )
                    })
                }
                <Tr>
                <Header>Ventes actuels</Header>
                
                    {
                         this.props.actualSales.map((item)=>{
                            return(
                                <TdActual>{item.quantity}</TdActual>
                            );
                        })
                    }
           
                </Tr>
                <Tr>
                <Header>Prévision</Header>
                    {
                         this.props.actualSales.map((item)=>{
                            return(
                                <Td>{item.quantity}</Td>
                            );
                        })
                    }
                           
                </Tr>
                <Tr>
                <Header>Ajustements</Header>
                    {
                         this.props.actualSales.map((item)=>{
                            return(
                                <Td>{item.quantity}</Td>
                            );
                        })
                    }
                           
                </Tr>
    
            </TableStyled>
            
    
            </Container>
          
        )
    }

  
}

export default Table
