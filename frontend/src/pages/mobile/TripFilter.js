import divided_line from '../../assets/icon/divided_line.svg';
import bag from '../../assets/icon/bag.svg';
import child from '../../assets/icon/child.svg';
import people2 from '../../assets/icon/2people.svg';
import smoke from '../../assets/icon/smoke.svg';
import pet from '../../assets/icon/pet.svg';
import star from '../../assets/icon/star.svg';
import profile_example from '../../assets/profile_example.png';
import '../../styles/mobile/style.css';
import React, {useEffect, useState} from 'react';
import Cookies from 'js-cookie';
import HeaderInformationBlock from '../../components/mobile/HeaderInformationBlock'
import Button from '../../components/mobile/Button'
import '../../styles/mobile/FellowTravelCards.module.css';
import LocationSelectSection from "../../components/mobile/LocationSelectSection";
import DatePicker from "react-datepicker";

import {format} from "date-fns";


function FellowTravelCards() {
    const [selectedDate, setSelectedDate] = useState(null);
    const [formattedDate, setFormattedDate] = useState('');
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [showFilters, setShowFilters] = useState(false);
    const [trips, setTrips] = useState([]);

    const toggleFilters = () => {
        setShowFilters(!showFilters);
    };

    const handleApply = () => {
        // Здесь можно добавить логику для применения фильтров
        toggleFilters();
    };

    const dataChange = (date) => {
        setSelectedDate(date);
        setFormattedDate(formatDate(date));
    };

    const formatDate = (date) => {
        if (!date) return '';
        const now = new Date();
        if (date.toDateString() === now.toDateString()) {
            return `Today at ${format(date, 'HH:mm')}`;
        }
        return `${format(date, 'dd MMM')} at ${format(date, 'HH:mm')}`;
    };

    const CustomInput = ({ value, onClick }) => {
        value = formatDate(selectedDate);
        return (
            <input
                value={value}
                onClick={onClick}
                readOnly
                className="input"
                placeholder="Select time"
            />)
    };

    const handleOptionClick = (option) => {
        setSelectedOptions(prevState => {
            if (prevState.includes(option)) {
                return prevState.filter(item => item !== option);
            } else {
                return [...prevState, option];
            }
        });
    };

    const isSelected = (option) => selectedOptions.includes(option);

    useEffect(() => {
        const sessionId = Cookies.get('session_id');
        if (!sessionId) {
            // Перенаправляем пользователя на главную страницу или другую страницу
            window.location.href = '/'; // Убедитесь, что этот путь существует в вашем приложении
        } else {
            // Делаем запрос на сервер для получения фильтрованных данных
            fetch('https://kuda-trip.ru/api/trip/get_upcoming', {
                method: 'POST',
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


    const resetFilters = () => {
        setSelectedOptions([]);
    };

    return (
        <>
            <HeaderInformationBlock
                startLocation="Universitetskaya, 1-7"
                endLocation="Pushkin, 3"
                date="Today at 18:00"
                passengers="1 passenger "
            />
            <section className="mobile_section">
                <div className="trip_cards_list">
                    <a href="#" className="trip_card_full">
                        <div className="trip_card_section">
                            <div className="trip_time_section">
                                <span className="trip_time">18:15</span>
                                <div className="trip_time_line">
                                    <img src={divided_line} />
                                    <div className="travel_time">
                                        <span> 1 hour 12 min </span>
                                    </div>
                                </div>
                                <span className="trip_time">19:27</span>
                            </div>
                        </div>
                        <div className="trip_card_section">
                            <div className="trip_location_section">
                                <div className="trip_location">
                                    <span className="city_header gray_color">Innopolis</span>
                                    <span className="address_span gray_color">Universitetskaya, 1-7</span>
                                </div>
                                <div className="trip_location right_align">
                                    <span className="city_header gray_color">Kazan</span>
                                    <span className="address_span gray_color">Pravo-bulachnaya 320</span>
                                </div>
                            </div>
                        </div>
                        <div className="trip_card_section trip_mini_info">
                            <span className="available_seats">3 places</span>
                            <div className="filters">
                                <img src={bag} alt=""/>
                                <img src={child} alt=""/>
                                <img src={people2} alt=""/>
                                <img src={smoke} alt=""/>
                                <img src={pet} alt=""/>
                            </div>
                        </div>
                        <div className="line"></div>
                        <div className="trip_card_section bottom_info_trip">
                            <div href="#" className="mini_profile_view">
                                <div className="profile_avatar">
                                    <img src={profile_example} />
                                </div>
                                <div className="profile_info">
                                    <span className="name">Andrey</span>
                                    <span className="car">Kia Optima</span>
                                </div>
                                <div className="grade_div">
                                    <img src={star} />
                                    <span className="grade">4.9</span>
                                </div>
                            </div>
                            <div className="clearfix"></div>

                            <div className="trip_cost">
                                800₽
                            </div>
                        </div>
                    </a>
                <div className="filter_flex">
                    <div className="filter_block">
                        <LocationSelectSection />
                    </div>

                    <div className="flex_row">
                        <DatePicker
                            selected={selectedDate}
                            onChange={dataChange}
                            showTimeSelect
                            dateFormat="Pp"
                            placeholderText="Select time"
                            customInput={<CustomInput value={formattedDate} />}
                        />
                    </div>

                    <div className="filters_tripcard">
                        <div className="filter_sort">
                            <div className="header_sort">
                                <h2>Sort</h2>
                                <h3 onClick={resetFilters} >Reset everything</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('earliest_trip')}>
                                <img src={earliest_trip} className={isSelected('earliest_trip') ? 'selected' : ''} />
                                <h3 className={isSelected('earliest_trip') ? 'selected' : ''} id="gray_filter">The earliest trips</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('cheapest_trip')}>
                                <img src={cheapest_trip} className={isSelected('cheapest_trip') ? 'selected' : ''} />
                                <h3 className={isSelected('cheapest_trip') ? 'selected' : ''} id="gray_filter">The cheapest trips</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('shortest_trip')}>
                                <img src={shortest_trip} className={isSelected('shortest_trip') ? 'selected' : ''} />
                                <h3 className={isSelected('shortest_trip') ? 'selected' : ''} id="gray_filter">The shortest trips</h3>
                            </div>
                        </div>
                        <div className="Convenience_safety">
                            <h2> Convenience and safety </h2>
                            <div className="filter_card" onClick={() => handleOptionClick('confirmed')}>
                                <img src={confirmed} className={isSelected('confirmed') ? 'selected' : ''} />
                                <h3 className={isSelected('confirmed') ? 'selected' : ''}>The profile is confirmed</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('smoke')}>
                                <img src={smoke} className={isSelected('smoke') ? 'selected' : ''} />
                                <h3 className={isSelected('smoke') ? 'selected' : ''}>You can smoke</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('pet')}>
                                <img src={pet} className={isSelected('pet') ? 'selected' : ''} />
                                <h3 className={isSelected('pet') ? 'selected' : ''}>It is possible with animals</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('bag')}>
                                <img src={bag} className={isSelected('bag') ? 'selected' : ''} />
                                <h3 className={isSelected('bag') ? 'selected' : ''}>I take parcels</h3>
                            </div>
                            <div className="filter_card" onClick={() => handleOptionClick('child')}>
                                <img src={child} className={isSelected('child') ? 'selected' : ''} />
                                <h3 className={isSelected('child') ? 'selected' : ''}>Child safety seat</h3>
                            </div>
                        </div>
                    </div>
                    <button className="find_btn">
                        <h2>Find</h2>
                    </button>
                </div>
            </section>
            <div className="bottom_absolute_block">
                <Button
                    type='blue_button'
                    size='pd10_70'
                    icon=''
                    text='Filters'
                    link_href='fellow_travel_cards'
                />
            </div>
            <div className="gray_bg" />
        </>
    );
}

export default FellowTravelCards;
