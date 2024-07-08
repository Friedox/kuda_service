import logo_full from '../../assets/illustration/logo_full.svg';
import google_logo from '../../assets/icon/google_logo.svg';
import '../../styles/mobile/style.css';

function login_email() {
    return (
        <>
            <section className="mobile_section">
                <img src={logo_full} id="logo_login"/>
                <div className="login_main">
                    <h1> Let's get started </h1>
                    <input type="email" id="name" name="name" placeholder="email@mail.ru"/>
                    <input type="password" id="password" name="password" placeholder="password"/>
                    <button className="login_btn">Log in</button>
                </div>
            </section>
        </>
    );
}

export default login_email;
