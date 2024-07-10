import React from 'react';
import back from '../../assets/icon/back.svg';
import forward from '../../assets/icon/forward.svg';
function Header({header_text}) {
    return (
        <>
            <div className="header_panel">
                <button className="back_btn">
                    <img src={back}/>
                </button>
                <h1>{header_text}</h1>
                <button className="forward_btn">
                    <img src={forward}/>
                </button>
            </div>
        </>
    );
}

export default Header;
