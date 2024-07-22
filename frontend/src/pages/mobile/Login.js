import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import logo_full from '../../assets/illustration/logo_full.svg';
import google_logo from '../../assets/icon/google_logo.svg';
import '../../styles/mobile/style.css';

function Login() {

    const navigate = useNavigate();

    useEffect(() => {
        const checkSession = async () => {
            try {
                const response = await axios.get('https://kuda-trip.ru/api/v1/auth/getusers/me/', {
                    withCredentials: true, // Включение cookies в запрос
                });

                if (response.data.status === 'ok') {
                    // Сессия действительна, перенаправляем пользователя
                    navigate('/home'); // Замените на нужный маршрут
                }
            } catch (error) {
                if (error.response && error.response.data.detail.message === 'Invalid session ID') {
                    // Остаемся на текущей странице
                    console.log('Invalid session, staying on login page');
                } else {
                    console.error('Error checking session:', error);
                    // Возможно, стоит добавить обработку других ошибок
                }
            }
        };

        checkSession();
    }, [navigate]);

    return (
        <>
            <section className="mobile_section">
                <img src={logo_full} id="logo_login"/>
                <div className="login_main">
                    <h1> Let's get started </h1>
                    <a href="#" className="google_btn">
                        <img src={google_logo}/>
                        <h2>Continue with Google</h2>
                    </a>
                    <div className="or_section">
                        <div/>
                        <h5>or</h5>
                        <div/>
                    </div>
                    <a href="login_email" className="login_email">
                        <h2>Log in using email</h2>
                    </a>
                </div>
            </section>
        </>
    );
}

export default Login;
