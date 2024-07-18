import logo from '../../assets/logo.svg';
import profile_example from '../../assets/profile_example.png';
import fellow_travel from '../../assets/illustration/fellow_travel.svg';
import group_plus from '../../assets/icon/group_plus.svg';
import plus from '../../assets/icon/plus.svg';
import taxi from '../../assets/illustration/taxi.svg';

import TripCardMedium from '../../components/mobile/TripCardMedium';
import React, {useEffect, useState} from 'react';
import Cookies from 'js-cookie';
import '../../styles/mobile/style.css';

function HomePage() {

    return (
        <>
            <section className="mobile_section">
                <div className="mobile_header">
                    <img className="logo" src={logo} alt='logo'/>
                    <a href="" className="profile_btn">
                        <img src={profile_example}  alt="profile_example"/>
                    </a>
                </div>
                <div className="mobile_btn_section">
                    <div className="left_btns">
                        <a href="filters" className="mobile_btn light_blue_bg">
                            <h2>
                                Fellow travelers
                            </h2>
                            <img className="" src={fellow_travel} alt="fellow_travel"/>
                        </a>
                        <a href="" className="mobile_btn icon_btn light_aqua_bg h140px">
                            <img className="" src={group_plus}  alt="group_plus"/>
                            <h2>
                                Create a group <br /> of fellow travelers
                            </h2>
                        </a>
                    </div>

                    <div className="right_btns">
                        <a href="create" className="mobile_btn icon_btn light_green_bg">
                            <img className="" src={plus} alt="plus"/>
                            <h2>
                                Create a trip
                            </h2>
                        </a>
                        <a href="" className="mobile_btn light_orange_bg h205px">
                            <h2>
                                Taxi
                            </h2>
                            <img className="" src={taxi} alt="taxi"/>
                        </a>
                    </div>
                </div>
                {/*<div className="trip_cards_section">*/}
                {/*    <h2>*/}
                {/*        Upcoming trips*/}
                {/*    </h2>*/}
                {/*    <TripCardMedium*/}
                {/*        startLocation="Universitetskaya, 1-7"*/}
                {/*        endLocation="Pushkin, 3"*/}
                {/*        date="Today at 18:00"*/}
                {/*        passengers="1 passenger "*/}
                {/*    />*/}
                {/*    <TripCardMedium*/}
                {/*        startLocation="Universitetskaya, 1-7"*/}
                {/*        endLocation="Pushkin, 3"*/}
                {/*        date="Today at 18:00"*/}
                {/*        passengers="1 passenger "*/}
                {/*    />*/}
                {/*</div>*/}
            </section>
        </>
    );
}

export default HomePage;
