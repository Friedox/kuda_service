import React, {useEffect, useState} from 'react';
import axios from 'axios';
import Cookies from 'js-cookie'; // Импорт библиотеки для работы с куками
import logo_full from '../../assets/illustration/logo_full.svg';
import '../../styles/mobile/style.css';

function LoginEmail() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    // Cookies.set('session_id')
    //
    // useEffect(() => {
    //     const sessionId = Cookies.get('session_id');
    //     if (sessionId) {
    //         // Перенаправляем пользователя на главную страницу или другую страницу
    //         window.location.href = '/home'; // Убедитесь, что этот путь существует в вашем приложении
    //     }
    // }, []);

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:8000/auth/login', {
                login: email,
                password: password
            });

            const { session_id } = response.data;

            // Сохраняем session_id в куках
            Cookies.set('session_id', session_id, { expires: 7, path: '/' });

            // Перенаправляем пользователя на главную страницу или другую страницу
            window.location.href = '/home'; // Убедитесь, что этот путь существует в вашем приложении
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
                </div>
            </section>
        </>
    );
}

export default LoginEmail;
