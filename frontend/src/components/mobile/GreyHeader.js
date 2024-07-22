import React from 'react';
import back_grey from '../../assets/icon/back_grey.svg';
function GreyHeader({header_text}) {
    return (
        <>
            <div className="header_panel">
                <button className="back_btn">
                    <img src={back_grey}/>
                </button>
                <h1>{header_text}</h1>
                <button className="back_btn">
                </button>
            </div>
        </>
    );
}

export default GreyHeader;
