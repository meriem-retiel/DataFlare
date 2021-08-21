import React from 'react'
import styled from 'styled-components'
import logo from '../../statics/logo.svg'
import { css } from 'styled-components'

const Container= styled.div`

`
const TextContainer = styled.div`

display:inline;
position: absolute;
top: 25px;
left: 68px;
`

const LogoStyled = styled.img`

position: relative;
display: inline;
height: 45px;
padding-bottom:0;
padding-top: 0;
margin:0;


`
const TextLogo= styled.h3`
display: inline;

color:${({theme})=>theme.header};
font-style: normal;
font-weight: 600;
font-size: 1.3rem;
${props => props.light && css`
    color:${({theme})=>theme.textColor};
  `}

`

const Logo = () => {
    return (
        <Container>
            <LogoStyled src={logo} />
            <TextContainer>
            <TextLogo >Data</TextLogo>
            <TextLogo light>Flare</TextLogo>
            </TextContainer>
        </Container>
        
    )
}

export default Logo
