import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../../actions/authActions';
import logo_full from '../../assets/illustration/logo_full.svg';
import '../../styles/mobile/style.css';
import Cookies from 'js-cookie'; // Импорт библиотеки для работы с куками


function LoginEmail() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const dispatch = useDispatch();

    const handleLogin = async () => {
        try {
            // Дождитесь завершения входа
            await dispatch(login(email, password));

            // Проверьте авторизацию после завершения входа
            const sessionId = Cookies.get('session_id');
            if (sessionId) {
                console.log(sessionId)
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
