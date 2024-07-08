import divided_line from '../../assets/icon/divided_line.svg';
import bag from '../../assets/icon/bag.svg';
import child from '../../assets/icon/child.svg';
import people2 from '../../assets/icon/2people.svg';
import smoke from '../../assets/icon/smoke.svg';
import pet from '../../assets/icon/pet.svg';
import star from '../../assets/icon/star.svg';
import profile_example from '../../assets/profile_example.png';
import '../../styles/mobile/style.css';
import '../../styles/mobile/FellowTravelCards.module.css';



function FellowTravelCards() {
    return (
        <>
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
                                <span className="trip_time">18:15</span>
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
                </div>
            </section>
        </>
    );
}

export default FellowTravelCards;
