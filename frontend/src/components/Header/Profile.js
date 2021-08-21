import React from 'react'
import styled from 'styled-components'
import Image from '../../assets/images/my-profile-image.png'


const Container = styled.div`
position:absolute;
top:18px;
right:20px;


`
const ProfileImg = styled.img`
height: 2rem;
border-radius:50%;
`



const Profile = () => {
    return (
        <Container>
            <ProfileImg src={Image}/>
        </Container>
    )
}

export default Profile
