import '../../styles/mobile/style.css';
import LocationSelectSection from "../../components/mobile/LocationSelectSection";
import DatePicker from "react-datepicker";
import React, { useState } from "react";
import { format } from "date-fns";
import cheapest_trip from "../../assets/icon/cheapest_trip.svg";
import earliest_trip from "../../assets/icon/earliest_trip.svg";
import shortest_trip from "../../assets/icon/shortest_trip.svg";
import smoke from "../../assets/icon/smoke.svg";
import pet from "../../assets/icon/pet.svg";
import bag from "../../assets/icon/bag.svg";
import child from "../../assets/icon/child.svg";
import confirmed from "../../assets/icon/confirmed.svg";
function TripFilter() {
    const [selectedDate, setSelectedDate] = useState(null);
    const [formattedDate, setFormattedDate] = useState('');
    const [selectedOptions, setSelectedOptions] = useState([]);

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
    const resetFilters = () => {
        setSelectedOptions([]);
    };
    return (
        <>
            <section className="mobile_section">
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

            <div className='gray_bg' />
        </>
    );
}

export default TripFilter;
