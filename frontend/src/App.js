import React from "react";
import Dashboard from "./containers/Dashboard";
import { ThemeProvider } from "styled-components";
import { GlobalStyles } from "./styles/global";
import { lightTheme, darkTheme } from "./styles/theme";


const structure= [
  {
    type:"folder",
    name:"Catégorie 1",
    childrens:[
      {
        type:"file",
        name:"Medoc1",
      },
      {
        type:"folder",
        name:"Subcatégorie",
        childrens:[
          {
            type:"file",
            name:"Medoc2",
          },
          {
            type:"file",
            name:"Medoc3",
          },
        ]
      },
    ],
  },
  {
    type:"folder",
    name:"Catégorie 2",
    childrens:[
      {
        type:"file",
        name:"medoc4",
      },
      {
        type:"file",
        name:"medoc5",
      },
    ],
  }
]
export default function App() {
  return(
    <ThemeProvider theme={darkTheme}>
      <GlobalStyles/>
      <Dashboard/>
    </ThemeProvider>

  );
}
