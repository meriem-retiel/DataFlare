import React from 'react'
import styled from 'styled-components'

const Container = styled.div`
background-color:red;
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

const Table = ({data}) => {
    return (
        <TableStyled>
             <Th >  </Th>
            {
                data.map((item)=>{
                    return(
                        <>
                        <Th >
                            {item.date}

                        </Th>
                       
                       </>
                    );

                })
            }
            <Tr>
            <Header>Ventes actuels</Header>
            
                {
                    data.map((item)=>{
                        return(
                            <TdActual>{item.ActualSale}</TdActual>
                        );
                    })
                }
       
            </Tr>
            <Tr>
            <Header>Prévision</Header>
                {
                    data.map((item)=>{
                        return(
                            <Td>{item.ForcastedSale}</Td>
                        );
                    })
                }
                       
            </Tr>
            <Tr>
            <Header>Ajustements</Header>
                {
                    data.map((item)=>{
                        return(
                            <Td>{item.AjustementSale}</Td>
                        );
                    })
                }
                       
            </Tr>

        </TableStyled>
        
    )
}

export default Table
