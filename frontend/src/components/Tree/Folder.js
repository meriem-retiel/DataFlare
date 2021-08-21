import { React, useState } from 'react';
import {AiOutlineFolder,AiOutlineFolderOpen} from 'react-icons/ai'
import styled from 'styled-components'
import {CaretUpOutlined} from '@ant-design/icons'
import {CaretDownOutlined} from '@ant-design/icons'
import { MinusSquareOutlined } from '@ant-design/icons';
import { PlusSquareOutlined } from '@ant-design/icons';
const StyledFolder= styled.div`
    padding-top:4px ;
    padding-bottom:4px ; 
    .folder--label{
        display:flex;
        align-items:center;
        span {
            margin-right:5px;
        }
    }
`;

const Collapsible = styled.div`
  /* set the height depending on isOpen prop */
  height: ${p => (p.isOpen ? 'auto' : '0')};
  /* hide the excess content */
  overflow: hidden;
`;

const Folder =({name,children})=>{
    const [isOpen, setIsOpen] = useState(false);
    const handleToggle = e => {
        e.preventDefault();
        setIsOpen(!isOpen);
      };
    return(
        <StyledFolder>
            <div className="folder--label" onClick={handleToggle}>
            {isOpen ? <MinusSquareOutlined /> : <PlusSquareOutlined />}
                <span>{name}</span>
            </div>
            <Collapsible isOpen={isOpen}>{children}</Collapsible>
        </StyledFolder>
    )
};

export { Folder };