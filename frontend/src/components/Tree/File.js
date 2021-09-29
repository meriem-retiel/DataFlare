import { AiOutlineFile } from 'react-icons/ai'
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios'


const StyledFile=styled.div `
    padding-left: 20px;
    padding-top: 0.2em;
    padding-bottom: 0.2em;
    display: flex;
    align-items: center;
    span{
        margin-left: 5px;
    }
    &:hover{
        background-color:${({theme})=>theme.hover} ;
    }
`;

const File =(props)=>(
        <Link to={`/${props.id}`}>
         <StyledFile>
            <AiOutlineFile/>
            <span style={{ textTransform:'lowercase'}}>{props.name}</span>
        </StyledFile>
        </Link>
       
    )

export { File };
