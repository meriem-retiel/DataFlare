import React, { useState } from 'react';
import { Modal, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import axios from "axios";

const Container = styled.div`
background-color: red;
color: ${({theme})=> theme.textColor };
`
const ButtonUplaod = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };


  const submitForm = (event) => {
    event.preventDefault();

    const data = new FormData();
    console.log(uploadFile)
    data.append("uploadFile", uploadFile);
    console.log(data.get('uploadFile'))
    axios
      .post("http://127.0.0.1:8000/api/upload/", data, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .then((response) => {
        console.log('success')
      })
      .catch((error) => {
        // error response
      });
  };

  const [uploadFile, setUploadFile] = React.useState();

  return (
    <>
      <Button style={{float:'right'}} type="primary" shape="circle" onClick={showModal}icon={ <PlusOutlined />} />

<Modal style={{color:"#242526"}} title="Ajouter un fichier" visible={isModalVisible} onOk={submitForm} onCancel={handleCancel}>
<div>
      <form onSubmit={submitForm}>
s
        <br />
        <input type="file" name='uploadFile' onChange={(e) => setUploadFile(e.target.files)} />
        <br />
        <input type="submit" />
      </form>
    </div>
  
      </Modal>
     
    </>
  );
}
 
export default ButtonUplaod