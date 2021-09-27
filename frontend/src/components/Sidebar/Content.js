import React from 'react'
import styled from 'styled-components'
import Tree from '../Tree/Tree'
import axios from 'axios'

const structure= [
    {
      type:"folder",
      name:"Antinflammatoires et antagiques",
      childrens:[
        {
          type:"file",
          name:"A1241",
        },
        {
            type:"file",
            name:"A1255",
          },
        {
            type:"file",
            name:"A1234",
        },
        {
          type:"folder",
          name:"Anti-infectieux",
          childrens:[
            {
              type:"file",
              name:"A1234",
            },
            {
              type:"file",
              name:"A3249",
            },
          ]
        },
      ],
    },
    {
      type:"folder",
      name:"Cardiologie",
      childrens:[
        {
          type:"file",
          name:"B1234",
        },
        {
          type:"file",
          name:"B5463",
        },
      ],
    },
    {
        type:"folder",
        name:"Dermatologie",
        childrens:[
          {
            type:"file",
            name:"C1324",
          },
          {
            type:"file",
            name:"C6574",
          },
        ],
      },
      {
        type:"folder",
        name:"Diabetologie",
        childrens:[
          {
            type:"file",
            name:"E4253",
          },
          {
            type:"file",
            name:"E4352",
          },
        ],
      },
      {
        type:"folder",
        name:"Gastro-enterologie",
        childrens:[
          {
            type:"file",
            name:"F32435",
          },
          {
            type:"file",
            name:"F3564",
          },
        ],
      },
      {
        type:"folder",
        name:"Gynecologie",
        childrens:[
          {
            type:"file",
            name:"G32435",
          },
          {
            type:"file",
            name:"G3764",
          },
          {
            type:"file",
            name:"G564",
          },
        ],
      }
  ]

const Container= styled.div`
font-size: 0.8rem;
white-space: nowrap; 
overflow: hidden;
text-overflow: ellipsis;
`


class Content extends React.Component {
  state = {
    products:[]
  }

  componentDidMount() {
    axios.get('http://127.0.0.1:8000/api/')
    .then(res=>{
      this.setState({
        products:res.data
      });
      console.log(res.data)
    })
  }
  render(){
    return (
      <Container>
          <Tree data={this.props.data}/>
      </Container>
  )

  }
   
}

export default Content
