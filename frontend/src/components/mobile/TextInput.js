import React from 'react';

function InputText({icon}) {
    return (
        <>
            <div className="input_text">
                <img src={icon} alt="Icon" />
                <input type="text" placeholder="Address"/>
            </div>
        </>
    );
}

export default InputText;
