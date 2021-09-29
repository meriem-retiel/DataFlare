import React from 'react'
import styled from 'styled-components'
import { Button } from 'antd'
import { CaretLeftOutlined,CaretRightOutlined } from '@ant-design/icons';


const Container = styled.div`
font-size: 12px;
`

class DatePicker extends React.Component{

    
    render()
    {
        return(
            <Container>
                <Button onClick={this.props.handledecrementDate}   color="inherit" type="link" shape="circle" icon={<CaretLeftOutlined />} />
                <span>{this.props.dateDebut[0]}/{this.props.dateDebut[1]}/01</span>- <span>{this.props.dateFin[0]}/{this.props.dateFin[1]}/01</span>
                <Button onClick={this.props.handleincrementDate} color="inherit" type="link" shape="circle" icon={<CaretRightOutlined />} />
            </Container>
        )
    }
}

export default DatePicker