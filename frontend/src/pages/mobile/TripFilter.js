import '../../styles/mobile/style.css';
import LocationSelectSection from "../../components/mobile/LocationSelectSection";
import DatePicker from "react-datepicker";
import React, { useState } from "react";
import { format } from "date-fns";

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

                    <div className="filter_block_f">
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
                </div>
            </section>

            <div className='gray_bg' />
        </>
    );
}

export default TripFilter;
