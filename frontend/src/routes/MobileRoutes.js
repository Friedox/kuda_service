import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePageMobile from '../pages/mobile/HomePage';
import FellowTravelCards from '../pages/mobile/FellowTravelCards';
import TripFilter from "../pages/mobile/TripFilter";
import MapPointSelect from "../pages/mobile/MapPointSelect";
import { Provider } from 'react-redux';
import store from '../store';
import CreateTripMap from "../pages/mobile/CreateTripMap";
import CreateTripFilter from "../pages/mobile/CreateTripFilter";

function MobileRoutes() {
    return (
        <Provider store={store}>
            <Routes>
                <Route path="/" element={<HomePageMobile />} />
                <Route path="/fellow_travel_cards" element={<FellowTravelCards />} />
                <Route path="/filters" element={<TripFilter />} />
                <Route path="/map" element={<MapPointSelect />} />
                <Route path="/create" element={<CreateTripMap />} />
                <Route path="/create_filter" element={<CreateTripFilter />} />
            </Routes>
        </Provider>
    );
}

export default MobileRoutes;