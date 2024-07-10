import React, { useEffect, useState, useRef } from 'react';
import map_point from "../../assets/icon/map_point.svg";
import local_icon from "../../assets/icon/LocateIcon.svg";
import user_location from "../../assets/icon/user_locatin.svg";
import Button from "../../components/mobile/Button";
import { useDispatch } from 'react-redux';
import { setStartAddress, setEndAddress } from '../../addressSlice';
import { useNavigate, useLocation } from 'react-router-dom';
import loadYandexMapScript from '../../utils/loadYandexMapScript';
import location_start_icon from "../../assets/icon/location_start.svg";
import location_end_icon from "../../assets/icon/location_end.svg";

function MapPointSelect() {
    const [mapInitialized, setMapInitialized] = useState(false);
    const [lastGeocodeTime, setLastGeocodeTime] = useState(0);
    const [pointType, setPointType] = useState(false);
    const [startTripAddress, setStartTripAddressState] = useState('');
    const [endTripAddress, setEndTripAddressState] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();
    const target = new URLSearchParams(location.search).get('target');
    const pointTypeRef = useRef(pointType);

    useEffect(() => {
        pointTypeRef.current = pointType;
    }, [pointType]);

    useEffect(() => {
        let ymapsInstance;
        const initializeMap = (ymaps) => {
            ymapsInstance = ymaps;
            if (!mapInitialized && ymaps.ready) {
                ymaps.ready(() => {
                    if (!mapInitialized) {
                        const map = new ymaps.Map("map", {
                            center: [55.76, 37.64],
                            zoom: 10,
                            controls: []
                        });

                        const location = ymaps.geolocation;
                        location.get({ mapStateAutoApply: true }).then(
                            function (result) {
                                const userCoordinates = result.geoObjects.get(0).geometry.getCoordinates();
                                map.setCenter(userCoordinates);

                                const userAddress = result.geoObjects.get(0).properties.get('text');
                                setStartTripAddressState(userAddress);

                                const marker = new ymaps.Placemark(userCoordinates, {}, {
                                    iconLayout: 'default#image',
                                    iconImageHref: user_location,
                                    iconImageSize: [40, 40],
                                    iconImageOffset: [-15, -42]
                                });
                                map.geoObjects.add(marker);
                            },
                            function (err) {
                                console.log('Ошибка: ' + err);
                            }
                        );

                        map.behaviors.enable('drag');
                        adjustMarkerSize();

                        window.addEventListener('resize', adjustMarkerSize);
                        map.events.add('boundschange', handleBoundsChange);

                        setMapInitialized(true);
                    }
                });
            }
        };

        const adjustMarkerSize = () => {
            const iconSizePercentage = 0.75;
            const iconWidth = window.innerWidth * iconSizePercentage;
            const iconHeight = window.innerHeight * iconSizePercentage;
            const marker = document.querySelector('.cursor-point');
            marker.style.width = `100%`;
            marker.style.height = `100vh`;
        };

        const handleBoundsChange = (event) => {
            const now = Date.now();
            if (now - lastGeocodeTime > 5000) {
                const center = event.get('newCenter');
                ymapsInstance.geocode(center).then(function (res) {
                    const firstGeoObject = res.geoObjects.get(0);
                    const address = firstGeoObject.getAddressLine();
                    if (!pointTypeRef.current) {
                        setStartTripAddressState(address);
                    } else {
                        setEndTripAddressState(address);
                    }
                    setLastGeocodeTime(now);
                });
            }
        };

        loadYandexMapScript()
            .then((ymaps) => {
                initializeMap(ymaps);
            })
            .catch((err) => {
                console.log(err);
            });


    }, [mapInitialized, lastGeocodeTime]);

    const handleClick = (newPointType) => {
        setPointType(newPointType);
    };

    useEffect(() => {
        console.log(`pointType изменился: ${pointType}`);
    }, [pointType]);

    return (
        <>
            <div id="map" className="yandex_map"></div>
            <div className="cursor-point" style={{
                background: `url(${map_point}) no-repeat center center`,
                width: '100px',
                height: '100px',
            }} />
            <div className="bottom_block h_none">
                <h2>Where are we going today</h2>
                <div className="location_select_section">
                    <a className="location_select_input" onClick={() => handleClick(false)}>
                        <img src={location_start_icon} />
                        <div className="location_title_section">
                            <h2>My location</h2>
                            <span>{startTripAddress || 'Loading current location...'}</span>
                        </div>
                    </a>

                    <div className="line_section">
                        <div className='line bg_e' />
                    </div>

                    <a className="location_select_input" onClick={() => handleClick(true)}>
                        <img src={location_end_icon} />
                        <div className="location_title_section">
                            <h2>SC “Koltso”</h2>
                            <span>{endTripAddress || 'Kazan, Pushkin, 3'}</span>
                        </div>
                    </a>
                </div>
                <a className="button blue_button w100 mt20px" href="/create_filter" >
                    <h3>Next</h3>
                </a>
            </div>
        </>
    );
}

export default MapPointSelect;
