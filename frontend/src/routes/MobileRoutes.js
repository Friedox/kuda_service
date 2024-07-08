import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePageMobile from '../pages/mobile/HomePage';
import FellowTravelCards from '../pages/mobile/FellowTravelCards';
import Login from '../pages/mobile/login';
import Login_email from '../pages/mobile/login_email';
import Trip_card from '../pages/mobile/trip_card';

function MobileRoutes() {
    return (
        <Routes>
            <Route path="/" element={<HomePageMobile />} />
            <Route path="/fellow_travel_cards" element={<FellowTravelCards />} />
            <Route path="/login" element={<Login />} />
            <Route path="/login_email" element={<Login_email />} />
            <Route path="/Trip_card" element={<Trip_card />} />
        </Routes>
    );
}

export default MobileRoutes;