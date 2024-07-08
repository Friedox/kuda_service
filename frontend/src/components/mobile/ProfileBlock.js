import React from 'react';
import location_end_icon from "../../assets/icon/location_end.svg";
import profile_example from "../../assets/profile_example.png";
import star from "../../assets/icon/star.svg";

function AddressCard({name, grade, profile_img, profile_id}) {
    return (
        <>
            <div href="/profile" className="mini_profile_view">
                <div className="profile_avatar">
                    <img src={profile_img} />
                </div>
                <div className="profile_info">
                    <span className="name">{name}</span>
                    <div className="grade_div">
                        <img src={star} />
                        <span className="grade">{grade}</span>
                    </div>
                </div>
            </div>
        </>
    );
}

export default AddressCard;
