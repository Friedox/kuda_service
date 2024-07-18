import React, { useEffect, useState } from 'react';
import '../../styles/mobile/style.css';
import '../../styles/mobile/FellowTravelCards.module.css';
import profile_example from '../../assets/profile_example.png'
import star from '../../assets/icon/star.svg'
import ellipse from '../../assets/icon/ellipse.svg'
import arrow_right from '../../assets/icon/arrow_right.svg'

function Profile() {
    return (
        <>
            <section className="mobile_section">
                <div className="profile_big_block">
                    <img className="profile_big_block_avatar" src={profile_example} />
                    <h2>Dmitry Zvidrin</h2>
                    <div className="profile_info_row">
                        <div className="profile_info_review">
                            <img src={star} />
                            <h3>4.9</h3>
                        </div>
                        <img src={ellipse} />
                        <h3>
                            120 tripss
                        </h3>
                    </div>
                </div>

                <a href="#" className="review_btn">
                    <h3>90 reviews</h3>
                    <img src={arrow_right} />
                </a>
            </section>

            <div className="gray_bg" />
        </>
    );
}

export default Profile;
