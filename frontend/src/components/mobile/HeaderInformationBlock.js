import React from 'react';

function HeaderInformationBlock({ startLocation, endLocation, date }) {
    return (
        <>
            <div className="header_information_block">
                <h3>{`${startLocation} — ${endLocation}`}</h3>
                <h5 className="gray_color">{`${date}`}</h5>
                {/*${passengers} passenger${passengers > 1 ? 's' : ''}`*/}
            </div>
        </>
    );
}

export default HeaderInformationBlock;
