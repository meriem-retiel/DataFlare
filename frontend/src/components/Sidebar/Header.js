import React from 'react'
import styled from 'styled-components'
import ButtonUplaod from './Upload2'

const HeaderText = styled.h3`
color:${({theme})=>theme.header};
font-style: normal;
font-weight: 500;
font-size: 1.3rem;
background:${({theme})=>theme.secondary} ;
`

const Header = ({title}) => {
    return (
        <>
        <HeaderText style={{display:'inline', marginLeft:'4px'}}>
            {title}
        </HeaderText>
        <ButtonUplaod/>
        </>

    )
}

export default Header
