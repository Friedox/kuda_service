
import logo_full from '../../assets/illustration/logo_full.svg';
import google_logo from '../../assets/icon/google_logo.svg';
import '../../styles/mobile/style.css';

function login() {
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

export default login;
