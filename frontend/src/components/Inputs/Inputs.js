import React from 'react'
import styled from 'styled-components'

export const SearchInput = styled.input`
background-color:${({theme})=>theme.line} ;
color:${({theme})=>theme.textColor} ;
font-size: 0.8em;
padding: 0.8em 1.2em;
 border: none;
 display: inline;
 border-radius: 50px;
 &:focus{
     outline: none;
 }

`
const Input = () => {
    return (
            <SearchInput placeholder={'Rechercher'}/>
    )
}

export default Input
