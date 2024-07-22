import React, { useEffect, useState } from 'react';
import axios from 'axios';
import divided_line from '../../assets/icon/divided_line.svg';
import bag from '../../assets/icon/bag.svg';
import child from '../../assets/icon/child.svg';
import people2 from '../../assets/icon/2people.svg';
import smoke from '../../assets/icon/smoke.svg';
import pet from '../../assets/icon/pet.svg';
import star from '../../assets/icon/star.svg';
import profile_example from '../../assets/profile_example.png';
import '../../styles/mobile/style.css';
import Cookies from 'js-cookie';
import HeaderInformationBlock from '../../components/mobile/HeaderInformationBlock';
import Button from '../../components/mobile/Button';
import '../../styles/mobile/FellowTravelCards.module.css';
import LocationSelectSection from '../../components/mobile/LocationSelectSection';
import DatePicker from 'react-datepicker';
import { format } from 'date-fns';
import earliest_trip from "../../assets/icon/earliest_trip.svg";
import cheapest_trip from "../../assets/icon/cheapest_trip.svg";
import shortest_trip from "../../assets/icon/shortest_trip.svg";
import confirmed from "../../assets/icon/confirmed.svg";
import location_start_icon from "../../assets/icon/location_start.svg";
import location_end_icon from "../../assets/icon/location_end.svg";
import {useNavigate} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import loadYandexMapScript from "../../utils/loadYandexMapScript";
import {setStartAddress, setStartCoordinate} from "../../addressSlice";
import { toggleOption } from '../../selectedOptionsSlice';


function FellowTravelCards() {
    const [selectedDate, setSelectedDate] = useState(null);
    const [formattedDate, setFormattedDate] = useState('');
    // const [selectedOptions, setSelectedOptions] = useState([]);
    const [showFilters, setShowFilters] = useState(true);
    const [trips, setTrips] = useState([
        {
            pickup: {
                latitude: 55.75190325,
                longitude: 48.75292795468886,
                address: {
                    city: "Innopolis",
                    name: "Building named after A. S. Popov",
                    road: "Universitetskaya street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420500",
                    country_code: "ru",
                    house_number: "7"
                },
                point_id: 1
            },
            dropoff: {
                latitude: 55.7455385,
                longitude: 48.7394729136916,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420500",
                    country_code: "ru",
                    house_number: "98"
                },
                point_id: 2
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 0,
            trip_id: 1,
            available_sits: 2,
            driver_phone: "string",
            driver_tg: "string",
            car_number: "string",
            car_type: "string",
            tags: ["smoke"]
        },
        {
            pickup: {
                latitude: 55.752,
                longitude: 48.753,
                address: {
                    city: "Innopolis",
                    name: "Library",
                    road: "Universitetskaya street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420500",
                    country_code: "ru",
                    house_number: "8"
                },
                point_id: 3
            },
            dropoff: {
                latitude: 55.746,
                longitude: 48.74,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420500",
                    country_code: "ru",
                    house_number: "99"
                },
                point_id: 4
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 100,
            trip_id: 2,
            available_sits: 3,
            driver_phone: "string2",
            driver_tg: "string2",
            car_number: "string2",
            car_type: "string2",
            tags: ["smoke", "pet"]
        },
        {
            pickup: {
                latitude: 55.753,
                longitude: 48.754,
                address: {
                    city: "Innopolis",
                    name: "Cafeteria",
                    road: "Student street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420501",
                    country_code: "ru",
                    house_number: "9"
                },
                point_id: 5
            },
            dropoff: {
                latitude: 55.747,
                longitude: 48.741,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420501",
                    country_code: "ru",
                    house_number: "100"
                },
                point_id: 6
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 150,
            trip_id: 3,
            available_sits: 4,
            driver_phone: "string3",
            driver_tg: "string3",
            car_number: "string3",
            car_type: "string3",
            tags: ["bag"]
        },
        {
            pickup: {
                latitude: 55.754,
                longitude: 48.755,
                address: {
                    city: "Innopolis",
                    name: "Dormitory",
                    road: "Student street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420502",
                    country_code: "ru",
                    house_number: "10"
                },
                point_id: 7
            },
            dropoff: {
                latitude: 55.748,
                longitude: 48.742,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420502",
                    country_code: "ru",
                    house_number: "101"
                },
                point_id: 8
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 200,
            trip_id: 4,
            available_sits: 2,
            driver_phone: "string4",
            driver_tg: "string4",
            car_number: "string4",
            car_type: "string4",
            tags: ["pet"]
        },
        {
            pickup: {
                latitude: 55.755,
                longitude: 48.756,
                address: {
                    city: "Innopolis",
                    name: "Tech Park",
                    road: "Technopark street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420503",
                    country_code: "ru",
                    house_number: "11"
                },
                point_id: 9
            },
            dropoff: {
                latitude: 55.749,
                longitude: 48.743,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420503",
                    country_code: "ru",
                    house_number: "102"
                },
                point_id: 10
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 250,
            trip_id: 5,
            available_sits: 5,
            driver_phone: "string5",
            driver_tg: "string5",
            car_number: "string5",
            car_type: "string5",
            tags: ["smoke", "pet"]
        },
        {
            pickup: {
                latitude: 55.756,
                longitude: 48.757,
                address: {
                    city: "Innopolis",
                    name: "Shopping Mall",
                    road: "Mall street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420504",
                    country_code: "ru",
                    house_number: "12"
                },
                point_id: 11
            },
            dropoff: {
                latitude: 55.75,
                longitude: 48.744,
                address: {
                    city: "Innopolis",
                    road: "Sportivnaya Street",
                    state: "Tatarstan",
                    county: "Verkhneuslonsky District",
                    country: "Russia",
                    postcode: "420504",
                    country_code: "ru",
                    house_number: "103"
                },
                point_id: 12
            },
            start_timestamp: 0,
            end_timestamp: 0,
            fare: 300,
            trip_id: 6,
            available_sits: 1,
            driver_phone: "string6",
            driver_tg: "string6",
            car_number: "string6",
            car_type: "string6",
            tags: ["smoke", "pets", "bag"]
        }
    ]);



    const toggleFilters = () => {
        setShowFilters(!showFilters);
    };

    const resetFilters = () => {
        // setSelectedOptions([]);
    };

    const handleApply = async () => {
        // Пример тела запроса, замените его реальными данными
        const requestBody = {
            pickup: {
                latitude: startCoordinate[0], // замените на реальные данные
                longitude: startCoordinate[1]
            },
            pickup_range: 100000,
            dropoff: {
                latitude: endCoordinate[0], // замените на реальные данные
                longitude: endCoordinate[1]
            },
            dropoff_range: 100000,
            start_timestamp: selectedDate ? Math.floor(selectedDate.getTime() / 1000) : 0,
            tags: selectedOptions
        };

        console.log(requestBody)
        console.log(startCoordinate)
        console.log(endCoordinate)

        try {
            const response = await axios.post('https://kuda-trip.ru/api/v1/trips/get_filtered/', requestBody);
            console.log(response)
            setTrips(response.data.detail);
            setShowFilters(false);
        } catch (error) {
            console.error('Error fetching trips:', error);
        }
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
            />
        );
    };

    // const handleOptionClick = (option) => {
    //     setSelectedOptions(prevState => {
    //         if (prevState.includes(option)) {
    //             return prevState.filter(item => item !== option);
    //         } else {
    //             return [...prevState, option];
    //         }
    //     });
    // };

    const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp * 1000); // преобразование timestamp в миллисекунды
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); // возвращаем строку локального времени без секунд
    };

    // const isSelected = (option) => selectedOptions.includes(option);

    const selectedOptions = useSelector(state => state.selectedOptions);
    const dispatch = useDispatch();

    const handleOptionClick = (option) => {
        dispatch(toggleOption(option));
    };

    const isSelected = (option) => selectedOptions.includes(option);

    const navigate = useNavigate();
    // const dispatch = useDispatch();
    const startAddress = useSelector((state) => state.address.startAddress);
    const endAddress = useSelector((state) => state.address.endAddress);
    const startCoordinate = useSelector((state) => state.address.startCoordinate);
    const endCoordinate = useSelector((state) => state.address.endCoordinate);

    useEffect(() => {
        if (!startAddress) {
            // Загрузка скрипта Yandex Maps API
            loadYandexMapScript()
                .then((ymaps) => {
                    ymaps.ready(() => {
                        const location = ymaps.geolocation;
                        location.get({ mapStateAutoApply: true }).then(
                            function (result) {
                                const userAddress = result.geoObjects.get(0).properties.get('text');
                                dispatch(setStartAddress(userAddress));
                                dispatch(setStartCoordinate(result.geoObjects.get(0).geometry.getCoordinates()));
                            },
                            function (err) {
                                console.log('Ошибка: ' + err);
                            }
                        );
                    });
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    }, [dispatch, startAddress]);

    return (
        <>
            <HeaderInformationBlock
                startLocation={startAddress}
                endLocation={endAddress}
                date={selectedDate}
                // passengers={}
            />

            <section className="mobile_section">
                <div className="trip_cards_list">

                    {trips.length > 0 && trips.map((trip, index) => (
                        <a href={"trip_card/" + trip.trip_id} className="trip_card_full" key={index}>
                            <div className="trip_card_section">
                                <div className="trip_time_section">
                                    <span className="trip_time">{formatTimestamp(trip.start_timestamp)}</span>
                                    <div className="trip_time_line">
                                        <img src={divided_line} />
                                        <div className="travel_time">
                                            <span>1 h</span>
                                        </div>
                                    </div>
                                    <span className="trip_time">{formatTimestamp(trip.end_timestamp)}</span>
                                </div>
                            </div>
                            <div className="trip_card_section">
                                <div className="trip_location_section">
                                    <div className="trip_location">
                                        <span className="city_header gray_color">{trip.pickup.address.city}</span>
                                        <span className="address_span gray_color">{trip.pickup.address.road} {trip.pickup.address.house_number}</span>
                                    </div>
                                    <div className="trip_location right_align">
                                        <span className="city_header gray_color">{trip.dropoff.address.city}</span>
                                        <span className="address_span gray_color text_right">{trip.dropoff.address.road} {trip.dropoff.address.house_number}</span>
                                    </div>
                                </div>
                            </div>
                            <div className="trip_card_section trip_mini_info">
                                <span className="available_seats">{trip.available_sits} places</span>
                                <div className="filters">
                                    {trip.tags.includes('bag') && <img src={bag} alt="Bag" />}
                                    {trip.tags.includes('child') && <img src={child} alt="Child" />}
                                    {trip.tags.includes('people2') && <img src={people2} alt="People2" />}
                                    {trip.tags.includes('smoke') && <img src={smoke} alt="Smoke" />}
                                    {trip.tags.includes('pet') && <img src={pet} alt="Pet" />}
                                </div>
                            </div>
                            <div className="line"></div>
                            <div className="trip_card_section bottom_info_trip">
                                <div href="#" className="mini_profile_view">
                                    <div className="profile_avatar">
                                        <img src={profile_example} />
                                    </div>
                                    <div className="profile_info">
                                        <span className="name">Имя пользователя</span>
                                        <span className="car">{trip.car_type}</span>
                                    </div>
                                    <div className="grade_div">
                                        <img src={star} />
                                        <span className="grade">{trip.driver_phone}</span>
                                    </div>
                                </div>
                                <div className="clearfix"></div>

                                <div className="trip_cost">
                                    {trip.fare ? trip.fare : "FREE"}
                                </div>
                            </div>
                        </a>
                    ))}
                </div>
            </section>
            <div className="bottom_absolute_block">
                <Button
                    type='blue_button'
                    size='pd10_70'
                    icon=''
                    text='Filters'
                    onClick={toggleFilters}
                />
            </div>

            {showFilters && (
                <section className="mobile_section trip_filter_section">
                    <div className="filter_flex">
                        <div className="filter_block">
                            <div className="location_select_section">
                                <a className="location_select_input" onClick={() => navigate('/map?target=start')}>
                                    <img src={location_start_icon} />
                                    <div className="location_title_section">
                                        <h2>My location</h2>
                                        <span>{startAddress || 'Loading current location...'}</span>
                                    </div>
                                </a>

                                <div className="line_section">
                                    <div className='line bg_e' />
                                </div>

                                <a className="location_select_input" onClick={() => navigate('/map?target=end')}>
                                    <img src={location_end_icon} />
                                    <div className="location_title_section">
                                        <h2>Куда</h2>
                                        <span>{endAddress || 'The end point'}</span>
                                    </div>
                                </a>
                            </div>
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
                                <div className="filter_card" onClick={() => handleOptionClick('smoke')}>
                                    <img src={smoke} className={isSelected('smoke') ? 'selected' : ''} />
                                    <h3 className={isSelected('smoke') ? 'selected' : ''}>You can smoke</h3>
                                </div>
                                <div className="filter_card" onClick={() => handleOptionClick('confirmed')}>
                                    <img src={confirmed} className={isSelected('confirmed') ? 'selected' : ''} />
                                    <h3 className={isSelected('confirmed') ? 'selected' : ''}>The profile is confirmed</h3>
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
                                {/*<div className="filter_card" onClick={() => handleOptionClick('earliest_trip')}>*/}
                                {/*    <img src={earliest_trip} className={isSelected('earliest_trip') ? 'selected' : ''} />*/}
                                {/*    <h3 className={isSelected('earliest_trip') ? 'selected' : ''} id="gray_filter">The earliest trips</h3>*/}
                                {/*</div>*/}
                                {/*<div className="filter_card" onClick={() => handleOptionClick('cheapest_trip')}>*/}
                                {/*    <img src={cheapest_trip} className={isSelected('cheapest_trip') ? 'selected' : ''} />*/}
                                {/*    <h3 className={isSelected('cheapest_trip') ? 'selected' : ''} id="gray_filter">The cheapest trips</h3>*/}
                                {/*</div>*/}
                                {/*<div className="filter_card" onClick={() => handleOptionClick('shortest_trip')}>*/}
                                {/*    <img src={shortest_trip} className={isSelected('shortest_trip') ? 'selected' : ''} />*/}
                                {/*    <h3 className={isSelected('shortest_trip') ? 'selected' : ''} id="gray_filter">The shortest trips</h3>*/}
                                {/*</div>*/}
                            </div>
                            {/*<div className="Convenience_safety">*/}
                            {/*    <h2> Convenience and safety </h2>*/}
                            {/*    <div className="filter_card" onClick={() => handleOptionClick('confirmed')}>*/}
                            {/*        <img src={confirmed} className={isSelected('confirmed') ? 'selected' : ''} />*/}
                            {/*        <h3 className={isSelected('confirmed') ? 'selected' : ''}>The profile is confirmed</h3>*/}
                            {/*    </div>*/}
                            {/*    <div className="filter_card" onClick={() => handleOptionClick('smoke')}>*/}
                            {/*        <img src={smoke} className={isSelected('smoke') ? 'selected' : ''} />*/}
                            {/*        <h3 className={isSelected('smoke') ? 'selected' : ''}>You can smoke</h3>*/}
                            {/*    </div>*/}
                            {/*    <div className="filter_card" onClick={() => handleOptionClick('pet')}>*/}
                            {/*        <img src={pet} className={isSelected('pet') ? 'selected' : ''} />*/}
                            {/*        <h3 className={isSelected('pet') ? 'selected' : ''}>It is possible with animals</h3>*/}
                            {/*    </div>*/}
                            {/*    <div className="filter_card" onClick={() => handleOptionClick('bag')}>*/}
                            {/*        <img src={bag} className={isSelected('bag') ? 'selected' : ''} />*/}
                            {/*        <h3 className={isSelected('bag') ? 'selected' : ''}>I take parcels</h3>*/}
                            {/*    </div>*/}
                            {/*    <div className="filter_card" onClick={() => handleOptionClick('child')}>*/}
                            {/*        <img src={child} className={isSelected('child') ? 'selected' : ''} />*/}
                            {/*        <h3 className={isSelected('child') ? 'selected' : ''}>Child safety seat</h3>*/}
                            {/*    </div>*/}
                            {/*</div>*/}
                        </div>
                        <a className="button blue_button w100" onClick={handleApply}>
                            <h2>Apply</h2>
                        </a>
                    </div>
                </section>
            )}
            <div className="gray_bg" />
        </>
    );
}

export default FellowTravelCards;
