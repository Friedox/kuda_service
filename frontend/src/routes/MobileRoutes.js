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
import Login from '../pages/mobile/login';
import Login_email from '../pages/mobile/login_email';
import Trip_card from '../pages/mobile/trip_card';
import DirectMessages from '../pages/mobile/DirectMessage';
import Conversation from '../pages/mobile/Conversation';

function MobileRoutes() {
    return (
        <Provider store={store}>
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/fellow_travel_cards" element={<FellowTravelCards/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/login_email" element={<Login_email/>}/>
                <Route path="/Trip_card" element={<Trip_card/>}/>
                <Route path="/home" element={<HomePageMobile/>}/>
                <Route path="/fellow_travel_cards" element={<FellowTravelCards/>}/>
                <Route path="/filters" element={<TripFilter/>}/>
                <Route path="/map" element={<MapPointSelect/>}/>
                <Route path="/create" element={<CreateTripMap/>}/>
                <Route path="/create_filter" element={<CreateTripFilter/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/chats" element={<DirectMessages/>}/>
                <Route path="/convTest" element={<Conversation/>}/>
            </Routes>
        </Provider>
    )
};


export default MobileRoutes;