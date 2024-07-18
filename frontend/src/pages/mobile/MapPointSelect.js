import React, { useEffect, useState } from 'react';
import map_point from "../../assets/icon/map_point.svg";
import local_icon from "../../assets/icon/LocateIcon.svg";
import user_location from "../../assets/icon/user_locatin.svg";
import Button from "../../components/mobile/Button";
import { useDispatch } from 'react-redux';
import { setStartAddress, setEndAddress } from '../../addressSlice';
import { useNavigate, useLocation } from 'react-router-dom';
import loadYandexMapScript from '../../utils/loadYandexMapScript';
import Cookies from 'js-cookie';

function MapPointSelect() {

    const [mapInitialized, setMapInitialized] = useState(false);
    const [lastGeocodeTime, setLastGeocodeTime] = useState(0);
    const [address, setAddressState] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();
    const target = new URLSearchParams(location.search).get('target');

    useEffect(() => {
        const initializeMap = (ymaps) => {
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
                                setAddressState(userAddress);

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
                        map.events.add('boundschange', function(event) {
                            const now = Date.now();
                            if (now - lastGeocodeTime > 5000) {
                                const center = map.getCenter();
                                ymaps.geocode(center).then(function (res) {
                                    const firstGeoObject = res.geoObjects.get(0);
                                    const address = firstGeoObject.getAddressLine();
                                    setAddressState(address);
                                    setLastGeocodeTime(now);
                                });
                                setLastGeocodeTime(now);
                            }
                        });

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

        loadYandexMapScript()
            .then((ymaps) => {
                initializeMap(ymaps);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [mapInitialized, lastGeocodeTime]);

    const handleApply = () => {
        if (target === 'start') {
            dispatch(setStartAddress(address));
        } else if (target === 'end') {
            dispatch(setEndAddress(address));
        }
        navigate('/filters');
    };

    return (
        <>
            <div id="map" className="yandex_map"></div>
            <div className="cursor-point" style={{
                background: `url(${map_point}) no-repeat center center`,
                width: '100px',
                height: '100px',
            }} />
            {/*<button id="geocodeButton">Get Address</button>*/}
            <div className="bottom_block">
                <h2>Where are we going today</h2>
                <div className="input_text">
                    <img src={local_icon} alt="Icon" />
                    <input type="text" placeholder="Address" value={address} readOnly />
                </div>
                <div className='scroll_div'></div>
                <a onClick={handleApply} className="button blue_button w100">
                    <h2>Apply</h2>
                </a>
            </div>
        </>
    );
}

export default MapPointSelect;
