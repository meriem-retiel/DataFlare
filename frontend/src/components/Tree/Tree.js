
import React from "react";
import styled from "styled-components"
import { TreeRecursive } from "./TreeRecursive";


const StyledTree = styled.div`
  line-height: 1.4;
`;

const Tree = ({ data,children }) => {
    const isImperative = data && !children;
    return <StyledTree>{isImperative ? <TreeRecursive data={data} /> : children}</StyledTree>;
  
};
export default Tree;