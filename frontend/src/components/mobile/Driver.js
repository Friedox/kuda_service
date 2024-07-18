import blue_star from "../../assets/icon/blue_star.svg";
import point from "../../assets/icon/point.svg";
function Driver({profile_photo, driver_name, grade, trips}) {
    return (
        <>
            <div className="driver_trip_section">

                <div className="profile_avatar">
                    <img src={profile_photo}/>
                </div>

                <div className="driver_profile_info">
                    <span className="name1">{driver_name}</span>
                    <div className="driver_info">
                        <div className="trip_grade">
                            <img src={blue_star}/>
                            <span className="grade">{grade}</span>
                        </div>

                        <img src={point}/>
                        <div className="trip_counter">
                            <span className="trips">{`${trips} trip${trips > 1 ? 's' : ''}`}</span>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Driver;