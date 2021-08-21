import React from 'react'
import styled from 'styled-components'
import Table from '../components/Table/Table'


const Container = styled.div`
position: absolute;
left:16rem;
right: 0;
top:7.7rem;
bottom:0;
`

const ProductPage = () => {
    return (
        <Container>
           <Table/>
        </Container>
    )
}

export default ProductPage
