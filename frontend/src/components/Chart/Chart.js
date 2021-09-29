import {Line} from "react-chartjs-2";
import styled from "styled-components";


const ydata= {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
    label: "Ventes actuels",
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 100, 500, 250, 210, 300, 450],
    },
    {
      label: "Previsions",
      backgroundColor: '#0A84FF',
      borderColor: '#0A84FF',
      data: [0,200 , 234, 200, 300, 450, 350],
      }
      

  
  ]
}
const Container = styled.div`

`


export const BarChart = ({data}) => {
  return (
    <Container>
      <Line
        data={data}
        height={300}
        width={600}
        options={{
          maintainAspectRatio : false, 
          scales: {
            y: {
                beginAtZero: true
            }
        }
         
        }}
      />
    </Container>
  );
};