import logo from '../../assets/logo.svg';
import profile_example from '../../assets/profile_example.png';
import fellow_travel from '../../assets/illustration/fellow_travel.svg';
import group_plus from '../../assets/icon/group_plus.svg';
import plus from '../../assets/icon/plus.svg';
import taxi from '../../assets/illustration/taxi.svg';

import TripCardMedium from '../../components/mobile/TripCardMedium';
import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import '../../styles/mobile/style.css';

function HomePage() {
    const [trips, setTrips] = useState([]);

    useEffect(() => {
        const sessionId = Cookies.get('session_id');
        if (!sessionId) {
            // Перенаправляем пользователя на главную страницу или другую страницу
            window.location.href = '/'; // Убедитесь, что этот путь существует в вашем приложении
        } else {
            // Делаем запрос на сервер для получения фильтрованных данных
            fetch('https://kuda-trip.ru/api/v1/trip/get_upcoming', {
                method: 'GET',
                credentials: 'include', // Включение cookies в запрос
                headers: {
                    'Content-Type': 'application/json'
                }
                // body: JSON.stringify({ tags: [] })
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            let errorMessage;
                            try {
                                errorMessage = JSON.parse(text);
                            } catch (e) {
                                errorMessage = text;
                            }
                            throw new Error(`Network response was not ok: ${response.statusText}. Response body: ${JSON.stringify(errorMessage)}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    setTrips(data); // Предполагается, что trips - это массив поездок
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }
    }, []);

    const formatDate = (timestamp) => {
        const date = new Date(timestamp * 1000); // Convert seconds to milliseconds
        return date.toLocaleString();
    };

    return (
        <>
            <section className="mobile_section">
                <div className="mobile_header">
                    <img className="logo" src={logo} alt='logo' />
                    <a href="" className="profile_btn">
                        <img src={profile_example} alt="profile_example" />
                    </a>
                </div>
                <div className="mobile_btn_section">
                    <div className="left_btns">
                        <a href="fellow_travel_cards" className="mobile_btn light_blue_bg">
                            <h2>
                                Fellow travelers
                            </h2>
                            <img className="" src={fellow_travel} alt="fellow_travel" />
                        </a>
                        <a href="" className="mobile_btn icon_btn light_aqua_bg h140px">
                            <img className="" src={group_plus} alt="group_plus" />
                            <h2>
                                Create a group <br /> of fellow travelers
                            </h2>
                        </a>
                    </div>

                    <div className="right_btns">
                        <a href="create" className="mobile_btn icon_btn light_green_bg">
                            <img className="" src={plus} alt="plus" />
                            <h2>
                                Create a trip
                            </h2>
                        </a>
                        <a href="taxi_create" className="mobile_btn light_orange_bg h205px">
                            <h2>
                                Taxi
                            </h2>
                            <img className="" src={taxi} alt="taxi" />
                        </a>
                    </div>
                </div>
                <div className="trip_cards_section">
                    <h2>
                        Upcoming trips
                    </h2>
                    {trips.map((trip) => (
                        <TripCardMedium
                            key={trip.trip_id}
                            startLocation={`Point ID: ${trip.pickup.point_id}`}
                            endLocation={`Point ID: ${trip.dropoff.point_id}`}
                            date={formatDate(trip.start_timestamp)}
                            passengers={`${trip.available_sits} passengers`}
                        />
                    ))}
                </div>
            </section>
        </>
    );
}

export default HomePage;
