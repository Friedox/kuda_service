import React from 'react';

//type:
//blue_button - blue button
//white_button - white button
//border_button - black border 1px

//size:
//w100 - width: 100% + padding: 10px 0;
//pd10_70 - padding: 10px 70px

function Button({ type, size, icon, text, link_href}) {
    const buttonClasses = `button ${type} ${size}`;

    return (
        <a href={link_href} className={buttonClasses}>
            {icon && <img src={icon} alt="icon" />}
            <h2>{text}</h2>
        </a>
    );
}

export default Button;
