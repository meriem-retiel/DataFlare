import React from 'react'
import styled from 'styled-components'


export const Button = styled.button`

 background-color: transparent;
 color: ${({theme})=>theme.textColor};
 font-size: 0.8em;
 padding: 0.5em 0.8em;
 border: none;
 margin-left: 8px;
 border-radius: 3px;
 &:hover{
     background-color:${({theme})=>theme.hover};
     color:${({theme})=>theme.header};
 }
`



