import React from 'react';
import location_end_icon from "../../assets/icon/location_end.svg";

function AddressCard({ locationTitle, location }) {
    return (
        <>
            <a className="location_select_input">
                {/*<img src={location_end_icon} />*/}
                <div className="location_title_section">
                    <h2>{locationTitle}</h2>
                    <span>{location}</span>
                </div>
            </a>
        </>
    );
}

export default AddressCard;
