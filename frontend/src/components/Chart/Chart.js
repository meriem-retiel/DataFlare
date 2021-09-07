import {Line} from "react-chartjs-2";
import styled from "styled-components";


const ydata= {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
    label: "My First dataset",
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 30, 45],
    }]
}
const Container = styled.div`

`


export const BarChart = ({data}) => {
  return (
    <Container>
      <Line
        data={data}
        height={400}
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