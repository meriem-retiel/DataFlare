import React from 'react'
import styled from 'styled-components'
import Header from './Header'
import Content from './Content'



const Container = styled.div`
background-color: ${({theme})=> theme.secondary} ;
position: fixed;
left:0;
top:0;
bottom:0;
padding:20px;
padding-top:8rem;
width: 16rem;

color: ${({theme})=> theme.textColor };

z-index: 1;
`

const Sidebar = () => {
    return (
        <Container>
            <Header title={'products'}/>
            <Content/>
        </Container>
    )
}

export default Sidebar
