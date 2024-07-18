import location_start_icon from '../../assets/icon/location_start.svg';
import location_end_icon from '../../assets/icon/location_end.svg';
import React from 'react';
import LocationSelectSection from "./LocationSelectSection";

function TripFilter() {
    return (
        <>
            <section className="mobile_section">
                <LocationSelectSection />
            </section>
            <div className='gray_bg'/>
        </>
    );
}

export default TripFilter;
