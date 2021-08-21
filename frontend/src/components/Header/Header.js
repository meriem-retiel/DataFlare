import React from 'react'
import styled from 'styled-components'
import Logo from './Logo'
import Menu from './Menu'
import Profile from './Profile'


const GlobalContainer = styled.div`
position: absolute;
width: 100%;
z-index: 3;
`

const Container = styled.div`

background-color: ${({theme})=> theme.secondary} ;
border-bottom: 0.5px solid;
border-color:${({theme})=> theme.line} ; 
padding: 8px 20px;

`

const Header = () => {
    return (
        <>
        <GlobalContainer>
        <Container>
            <Logo/>
            <Profile/>
        </Container>
        <Menu/>
        </GlobalContainer>
        
        </>
    )
}

export default Header
