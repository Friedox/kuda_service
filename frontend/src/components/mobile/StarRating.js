import React, { useState } from 'react';
import starEmpty from "../../assets/icon/gray_star.svg"; // Импорт пустой звезды
import starFilled from "../../assets/icon/blue_star.svg"; // Импорт закрашенной звезды

const StarRating = ({ totalStars = 5 }) => {
    const [rating, setRating] = useState(0); // Состояние для хранения текущего рейтинга

    const handleClick = (index) => {
        setRating(index + 1); // Установка рейтинга при клике на звезду
    };

    return (
        <div className="star-rating">
            {Array.from({ length: totalStars }, (_, index) => (
                <img
                    key={index}
                    src={index < rating ? starFilled : starEmpty}
                    alt={`${index + 1} star`}
                    className="star"
                    onClick={() => handleClick(index)}
                />
            ))}
        </div>
    );
};

export default StarRating;
