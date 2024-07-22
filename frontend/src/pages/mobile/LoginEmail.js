import React, {useEffect, useState} from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../../actions/authActions';
import logo_full from '../../assets/illustration/logo_full.svg';
import '../../styles/mobile/style.css';
import Cookies from 'js-cookie';
import {useNavigate} from "react-router-dom";
import axios from "axios"; // Импорт библиотеки для работы с куками


function LoginEmail() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const dispatch = useDispatch();

    const navigate = useNavigate();

    useEffect(() => {
        const checkSession = async () => {
            try {
                const response = await axios.get('https://kuda-trip.ru/api/v1/auth/getusers/me/', {
                    withCredentials: true, // Включение cookies в запрос
                });

                if (response.data.status === 'ok') {
                    // Сессия действительна, перенаправляем пользователя
                    navigate('/homes'); // Замените на нужный маршрут
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

    const handleLogin = async () => {
        try {
            // Дождитесь завершения входа
            await dispatch(login(email, password));

            // Проверьте авторизацию после завершения входа
            const sessionId = Cookies.get('session_id');
            if (sessionId) {
                // Перенаправьте на страницу Home, если пользователь авторизован
                window.location.href = '/home';
            } else {
                // Если session_id не установлен, что-то пошло не так
                setError('Login failed. Please check your credentials and try again.');
            }
        } catch (error) {
            console.error('Login error', error);
            setError('Login failed. Please check your credentials and try again.');
        }
    };


    return (
        <>
            <section className="mobile_section">
                <img src={logo_full} id="logo_login" alt="Logo"/>
                <div className="login_main">
                    <h1>Let's get started</h1>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="email@mail.ru"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button className="login_btn" onClick={handleLogin}>Log in</button>
                    {error && <p className="error_message">{error}</p>}
                    <div className="or_section">
                        <div/>
                        <h5>or</h5>
                        <div/>
                    </div>
                    <a href="signup" className="login_email">
                        <h2>Sign Up</h2>
                    </a>
                </div>
            </section>
        </>
    );
}

export default LoginEmail;
