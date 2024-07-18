import React from 'react';

function HeaderInformationBlock({ startLocation, endLocation, date, passengers }) {
    return (
        <>
            <div className="header_information_block">
                <h3>{`${startLocation} — ${endLocation}`}</h3>
                <h5 className="gray_color">{`${date}, ${passengers} passenger${passengers > 1 ? 's' : ''}`}</h5>
            </div>
        </>
    );
}

export default HeaderInformationBlock;
