import React from 'react';
import verif from "../../assets/icon/verified.svg";

const ProfileAvatar = ({avatar, verified}) => {
    return (
            <div className="profile_avatar_holder">
            <div className="profile_avatar">
            <img src={avatar}/>
            {verified && <div className="chat_verified"><img src={verif}/></div>}
            </div>
            
      </div>
    )
}

export default ProfileAvatar;