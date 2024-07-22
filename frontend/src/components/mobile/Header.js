import React from 'react';
import back from '../../assets/icon/back.svg';
import forward from '../../assets/icon/forward.svg';
function Header({header_text, href}) {

    const handleShare = () => {
        if (navigator.share) {
            navigator.share({
                title: 'Check out this trip!',
                text: 'Here are the details for the trip.',
                url: href,
            }).then(() => {
                console.log('Successfully shared');
            }).catch((error) => {
                console.error('Error sharing', error);
            });
        } else {
            console.log('Web Share API is not supported in your browser.');
        }
    }

    return (
        <>
            <div className="header_panel">
                <button className="back_btn">
                    <img src={back}/>
                </button>
                <h1>{header_text}</h1>
                <a href={href} className="forward_btn">
                    <img src={forward}/>
                </a>
            </div>
        </>
    );
}

export default Header;
