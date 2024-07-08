import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePageMobile from '../pages/desktop/HomePage';
import FellowTravelCards from '../pages/desktop/FellowTravelCards';

function MobileRoutes() {
    return (
        <Routes>
            <Route path="/" element={<HomePageMobile />} />
            <Route path="/fellow_travel_cards" element={<FellowTravelCards />} />
        </Routes>
    );
}

export default MobileRoutes;