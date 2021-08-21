import React from 'react'
import styled from 'styled-components'
import { css } from 'styled-components'
import { Button } from '../Buttons/Buttons'
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import Icon from '../../assets/icons/maps_ugc_black.svg'
import { AiOutlineComment } from 'react-icons/ai';
import { BsFillChatFill } from "react-icons/bs";
import SearchInput from '../Inputs/Inputs';

const Container = styled.div`
background-color: ${({theme})=> theme.secondary} ;
border-bottom: 0.5px solid;
border-color:${({theme})=> theme.line} ; 
padding: 8px 20px;

`




const Menu = () => {
    return (
        <Container>
            <SearchInput/>
            <Button>
            <CheckCircleIcon style={{height:'18px', position:'relative',top:'4px'}}/>
                <p style={{paddingLeft:'6px', display:'inline'}}>Approuver / Désapprouver</p>
            </Button>
            <Button>
            <BsFillChatFill style={{height:'20px', position:'relative',top:'4px'}}/>
            <p style={{paddingLeft:'6px', display:'inline'}}> Commenter</p>
            </Button>
        </Container>
    )
}

export default Menu
