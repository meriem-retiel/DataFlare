import { AiOutlineFile } from 'react-icons/ai'
import styled from 'styled-components'

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

const File =({name})=>(
        <StyledFile>
            <AiOutlineFile/>
            <span style={{ textTransform:'lowercase'}}>{name}</span>
        </StyledFile>
    )

export { File };
