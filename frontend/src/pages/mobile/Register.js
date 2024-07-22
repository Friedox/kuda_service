import React, {useState} from 'react';
import axios from 'axios';
import Cookies from 'js-cookie'; // Импорт библиотеки для работы с куками
import logo_full from '../../assets/illustration/vertical_login.svg';
import '../../styles/mobile/style.css';

function SignUpEmail() {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [criteria, setCriteria] = useState({
        length: false,
        uppercase: false,
        number: false,
    });

    const handlePasswordChange = (e) => {
        const value = e.target.value;
        setPassword(value);
        setCriteria({
            length: value.length >= 8,
            uppercase: /[A-Z]/.test(value),
            number: /\d/.test(value),
        });
    };

    const getCriterionClass = (criterionMet) => {
        if (password.length === 0) {
            return 'criterion';
        }
        return criterionMet ? 'criterion valid' : 'criterion invalid';
    };

    const handleSignUp = async () => {
        try {
            const response = await axios.post('https://kuda-trip.ru/api/v1/auth/signup', {
                email: email,
                username: username,
                password: password,
                is_google_account: false
            });

            // Если регистрация успешна, перенаправляем пользователя на страницу логина
            window.location.href = '/login_email'; // Убедитесь, что этот путь существует в вашем приложении
        } catch (error) {
            console.error('Sign Up error', error);
            setError('Sign Up failed. Please check your details and try again.');
        }
    };

    return (
        <>
            <section className="mobile_section">
                <img src={logo_full} id="logo_login" className="" alt="Logo"/>
                <div className="login_main">
                    <h1>Let's get acquainted</h1>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="email@mail.ru"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="text"
                        id="username"
                        name="username"
                        placeholder="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                    <div className="criteria">
                        <div className={`${getCriterionClass(criteria.length)} validation`}>
                            <span>8 characters</span>
                        </div>
                        <div className={`${getCriterionClass(criteria.number)} validation`}>
                            <span>numbers</span>
                        </div>
                        <div className={`${getCriterionClass(criteria.uppercase)} validation`}>
                            <span>сapital letter</span>
                        </div>
                    </div>
                    <button className="login_btn" onClick={handleSignUp}>Sign Up</button>
                    {error && <p className="error_message">{error}</p>}
                    <div className="or_section">
                        <div/>
                        <h5>or</h5>
                        <div/>
                    </div>
                    <a href="login_email" className="login_email">
                        <h2>Log In</h2>
                    </a>

                </div>
            </section>
        </>
    );
}

export default SignUpEmail;
