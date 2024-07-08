import location_start_icon from '../../assets/icon/location_start.svg';
import location_end_icon from '../../assets/icon/location_end.svg';
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { setStartAddress } from '../../addressSlice';
import loadYandexMapScript from '../../utils/loadYandexMapScript';

function LocationSelectSection() {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const startAddress = useSelector((state) => state.address.startAddress);
    const endAddress = useSelector((state) => state.address.endAddress);

    useEffect(() => {
        if (!startAddress) {
            // Загрузка скрипта Yandex Maps API
            loadYandexMapScript()
                .then((ymaps) => {
                    ymaps.ready(() => {
                        const location = ymaps.geolocation;
                        location.get({ mapStateAutoApply: true }).then(
                            function (result) {
                                const userAddress = result.geoObjects.get(0).properties.get('text');
                                dispatch(setStartAddress(userAddress));
                            },
                            function (err) {
                                console.log('Ошибка: ' + err);
                            }
                        );
                    });
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    }, [dispatch, startAddress]);

    return (
        <>
                <div className="location_select_section">
                    <a className="location_select_input" onClick={() => navigate('/map?target=start')}>
                        <img src={location_start_icon} />
                        <div className="location_title_section">
                            <h2>My location</h2>
                            <span>{startAddress || 'Loading current location...'}</span>
                        </div>
                    </a>

                    <div className="line_section">
                        <div className='line bg_e' />
                    </div>

                    <a className="location_select_input" onClick={() => navigate('/map?target=end')}>
                        <img src={location_end_icon} />
                        <div className="location_title_section">
                            <h2>SC “Koltso”</h2>
                            <span>{endAddress || 'Kazan, Pushkin, 3'}</span>
                        </div>
                    </a>
                </div>
        </>
    );
}

export default LocationSelectSection;
