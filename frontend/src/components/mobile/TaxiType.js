import React from 'react';

function TaxiType({image, type, price, selected, onClick}) {
    return (

        <div
            className={`taxi_type_card ${selected ? 'selected_taxi' : ''}`}
            onClick={() => onClick(type)} // Передаем тип такси как аргумент
        >
            <div className="car_image">
                <img src={image} alt="Icon"/>
            </div>
            <div className="type_taxi_info">
                <h4>{type}</h4>
                <h2>{`${price}₽`}</h2>
            </div>
        </div>
    );
}

export default TaxiType;