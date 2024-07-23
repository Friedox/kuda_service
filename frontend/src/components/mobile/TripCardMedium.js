import React from 'react';

function TripCardMedium({ startLocation, endLocation, date, passengers, tripId}) {
    return (
        <>
            <a href={"trip_card/" + {tripId}} className="trip_card_medium">
                <h3>{`${startLocation} — ${endLocation}`}</h3>
                <h5>{`${date}, ${passengers} passenger${passengers > 1 ? 's' : ''}`}</h5>
            </a>
        </>
    );
}

export default TripCardMedium;
