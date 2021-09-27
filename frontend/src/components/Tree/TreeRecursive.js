import React from 'react'
import { Folder } from './Folder';
import { File } from './File';

/*const TreeRecursive = ({ data }) => {
    // loop through the data
    return data.map(item => {
      // if its a file render <File />
      if (item.type === 'file') {
        return <File name={item.name} />;
      }
      // if its a folder render <Folder />
      if (item.type === 'folder') {
        return (
          <Folder name={item.name}>
            
            <TreeRecursive data={item.childrens} />
          </Folder>
        );
      }
    });
  };
*/
const TreeRecursive = (props) => {
    // loop through the data
    return(
    <Folder name ='Biopharm'>
      {
          props.data.map(item => {
          // if its a file render <File />
          if (1 === 1) {
            return <File id={item.id} name={item.designation} />;
             }
  // if its a folder render <Folder />
      })
      }
    </Folder>
    )
   
  };

 

  export {TreeRecursive};