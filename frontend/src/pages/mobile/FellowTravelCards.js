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

function FellowTravelCards() {
    const [selectedDate, setSelectedDate] = useState(null);
    const [formattedDate, setFormattedDate] = useState('');
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [showFilters, setShowFilters] = useState(false);
    const [trips, setTrips] = useState([]);
    const [filterData, setFilterData] = useState({
        pickup: { latitude: 0, longitude: 0 },
        pickup_range: 0,
        dropoff: { latitude: 0, longitude: 0 },
        dropoff_range: 0,
        start_timestamp: 0,
        end_timestamp: 0,
        tags: []
    });

    useEffect(() => {
        // Функция для получения данных с сервера
        const fetchTrips = async () => {
            try {
                const response = await axios.post('https://kuda-trip.ru/api/trip/get_filtered', filterData);
                if (response.data.status === 'ok') {
                    const tripsWithAddresses = await Promise.all(response.data.detail.map(async (trip) => {
                        const startAddress = await getAddressFromCoordinates(0, 0);
                        const endAddress = await getAddressFromCoordinates(0, 0);
                        return { ...trip, startAddress, endAddress };
                    }));
                    setTrips(tripsWithAddresses);
                }
            } catch (error) {
                console.error('Error fetching trips:', error);
            }
        };

        // Вызов функции при загрузке компонента и изменении фильтров
        fetchTrips();
    }, [filterData]);

    const toggleFilters = () => {
        setShowFilters(!showFilters);
    };

    const handleApply = () => {
        // Обновляем данные фильтра
        const updatedFilterData = {
            ...filterData,
            start_timestamp: selectedDate ? Math.floor(new Date(selectedDate).getTime() / 1000) : 0,
            tags: selectedOptions
        };
        setFilterData(updatedFilterData);
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
            />
        );
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

    const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp * 1000); // преобразование timestamp в миллисекунды
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); // возвращаем строку локального времени без секунд
    };

    const getAddressFromCoordinates = async (latitude, longitude) => {
        const apiUrl = `https://kuda-trip.ru/api/trip/convert_coords?latitude=${latitude}&longitude=${longitude}`; // Замените на ваш URL сервера
        console.log(apiUrl)

        try {
            const response = await axios.get(apiUrl);
            console.log(response.data.detail)
            const address = response.data.detail; // Предполагаем, что сервер возвращает строку с адресом
            return address;
        } catch (error) {
            console.error('Error fetching address:', error);
            return '';
        }
    };

    // const getAddressFromCoordinates = async (latitude, longitude) => {
    //     const apiKey = '2d7d974c-4c95-4115-a3e5-8a33651cb060';
    //     try {
    //         const response = await axios.get(`https://geocode-maps.yandex.ru/1.0/?format=json&apikey=${apiKey}&geocode=${longitude},${latitude}`);
    //         const address = response.data.response.GeoObjectCollection.featureMember[0].GeoObject.metaDataProperty.GeocoderMetaData.text;
    //         return address;
    //     } catch (error) {
    //         console.error('Error fetching address:', error);
    //         return '';
    //     }
    // };

    const isSelected = (option) => selectedOptions.includes(option);

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
                    {trips.map((trip, index) => (
                        <a href="#" className="trip_card_full" key={index}>
                            <div className="trip_card_section">
                                <div className="trip_time_section">
                                    <span className="trip_time">{formatTimestamp(trip.start_timestamp)}</span>
                                    <div className="trip_time_line">
                                        <img src={divided_line} />
                                        <div className="travel_time">
                                            <span>{trip.fare}</span>
                                        </div>
                                    </div>
                                    <span className="trip_time">{formatTimestamp(trip.end_timestamp)}</span>
                                </div>
                            </div>
                            <div className="trip_card_section">
                                <div className="trip_location_section">
                                    <div className="trip_location">
                                        <span className="city_header gray_color">{trip.start_city}</span>
                                        <span className="address_span gray_color">{trip.startAddress}</span>
                                    </div>
                                    <div className="trip_location right_align">
                                        <span className="city_header gray_color">{trip.end_city}</span>
                                        <span className="address_span gray_color">{trip.endAddress}</span>
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
                                        <span className="name">Alex</span>
                                        <span className="car">Haval</span>
                                    </div>
                                    <div className="grade_div">
                                        <img src={star} />
                                        <span className="grade">4.8</span>
                                    </div>
                                </div>
                                <div className="clearfix"></div>

                                <div className="trip_cost">
                                    FREE
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

                        <div className={`filter_block_f ${showFilters ? 'show' : ''}`}>
                            <div
                                className={`filter_btn ${isSelected("only_verified") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("only_verified")}
                            >
                                Only verified users
                            </div>
                            <div
                                className={`filter_btn ${isSelected("smoke") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("smoke")}
                            >
                                You can smoke
                            </div>
                            <div
                                className={`filter_btn ${isSelected("parcels") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("parcels")}
                            >
                                I take parcels
                            </div>
                            <div
                                className={`filter_btn ${isSelected("child") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("child")}
                            >
                                Child safety seat
                            </div>
                            <div
                                className={`filter_btn ${isSelected("with_animals") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("with_animals")}
                            >
                                With animals
                            </div>
                            <div
                                className={`filter_btn ${isSelected("max_two") ? 'checkbox_blue' : ''}`}
                                onClick={() => handleOptionClick("max_two")}
                            >
                                Maximum two in the back
                            </div>
                        </div>
                        <a href="filters" className="button blue_button w100" onClick={handleApply}>
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
