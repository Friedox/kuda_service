import React from 'react';

function TripCardMedium({ startLocation, endLocation, date, passengers }) {
    return (
        <>
            <a href="src/components/mobile/TripCardMedium#" className="trip_card_medium">
                <h3>{`${startLocation} — ${endLocation}`}</h3>
                <h5>{`${date}, ${passengers} passenger${passengers > 1 ? 's' : ''}`}</h5>
            </a>
        </>
    );
}

export default TripCardMedium;
