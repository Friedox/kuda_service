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
import Login from '../pages/mobile/Login';
import Login_email from '../pages/mobile/LoginEmail';
import TripCard from '../pages/mobile/TripCard';
import TaxiCreate from "../pages/mobile/TaxiCreate";
import CarSearching from "../pages/mobile/CarSearching";
import DriverWait from "../pages/mobile/DriverWait";
import StartTrip from "../pages/mobile/StartTrip";
import DriverNotFound from "../pages/mobile/DriverNotFound";
import Rating from "../pages/mobile/Raiting";

function MobileRoutes() {
    return (
        <Provider store={store}>
            <Routes>
                <Route path="/" element={<Login_email/>}/>
                <Route path="/fellow_travel_cards" element={<FellowTravelCards/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/login_email" element={<Login_email/>}/>
                <Route path="/TripCard" element={<TripCard/>}/>
                <Route path="/home" element={<HomePageMobile/>}/>
                <Route path="/fellow_travel_cards" element={<FellowTravelCards/>}/>
                <Route path="/filters" element={<TripFilter/>}/>
                <Route path="/map" element={<MapPointSelect/>}/>
                <Route path="/create" element={<CreateTripMap/>}/>
                <Route path="/create_filter" element={<CreateTripFilter/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/login_email" element={<Login_email/>}/>
                <Route path="/TripCard" element={<TripCard/>}/>
                <Route path="/TaxiCreate" element={<TaxiCreate/>}/>
                <Route path="/CarSearching" element={<CarSearching/>}/>
                <Route path="/DriverWait" element={<DriverWait/>}/>
                <Route path="/StartTrip" element={<StartTrip/>}/>
                <Route path="/DriverNotFound" element={<DriverNotFound/>}/>
                <Route path="/Rating" element={<Rating/>}/>
            </Routes>
        </Provider>
    )
};


export default MobileRoutes;