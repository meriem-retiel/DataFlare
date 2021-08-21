import React from 'react'
import { Folder } from './Folder';
import { File } from './File';

const TreeRecursive = ({ data }) => {
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
            {/* Call the <TreeRecursive /> component with the current item.childrens */}
            <TreeRecursive data={item.childrens} />
          </Folder>
        );
      }
    });
  };

  export {TreeRecursive};