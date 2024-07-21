import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../store';
import HomePageMobile from '../pages/mobile/HomePage';
import FellowTravelCards from '../pages/mobile/FellowTravelCards';
import TripFilter from "../pages/mobile/TripFilter";
import MapPointSelect from "../pages/mobile/MapPointSelect";
import CreateTripMap from "../pages/mobile/CreateTripMap";
import CreateTripFilter from "../pages/mobile/CreateTripFilter";
import Login from '../pages/mobile/Login';
import LoginEmail from '../pages/mobile/LoginEmail';
import TripCard from '../pages/mobile/TripCard';
import Register from "../pages/mobile/Register";
import SignUpEmail from "../pages/mobile/Register";
import PrivateRoute from "./PrivateRoute";
import Profile from "../pages/mobile/Profile";
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
                <Route path="/login_email" element={<LoginEmail />} />
                <Route path="/home" element={<HomePageMobile />} />
                <Route path="/fellow_travel_cards" element={<FellowTravelCards />} />
                {/*<Route path="/filters" element={<FellowTravelCards />} />*/}
                <Route path="/map" element={<MapPointSelect />} />
                <Route path="/create" element={<CreateTripMap />} />
                <Route path="/create_filter" element={<CreateTripFilter />} />
                <Route path="/trip_card" element={<TripCard />} />
                <Route path="/" element={<Login />} />
                <Route path="/signup" element={<SignUpEmail />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/trip_card/:tripId" element={<TripCard />} />
                <Route path="/home" element={<HomePageMobile/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/taxi_create" element={<TaxiCreate/>}/>
                <Route path="/car_searching" element={<CarSearching/>}/>
                <Route path="/driver_wait" element={<DriverWait/>}/>
                <Route path="/start_trip" element={<StartTrip/>}/>
                <Route path="/driver_not_found" element={<DriverNotFound/>}/>
                <Route path="/rating" element={<Rating/>}/>
            </Routes>
        </Provider>
    );
}

export default MobileRoutes;
