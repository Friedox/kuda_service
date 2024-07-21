import axios from 'axios';
import Cookies from 'js-cookie';

export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGOUT_SUCCESS = 'LOGOUT_SUCCESS';

export const login = (email, password) => async dispatch => {
    try {
        const response = await axios.post('https://kuda-trip.ru/api/v1/auth/login', {
            login: email,
            password: password
        });

        const { status, detail } = response.data;
        if (status === 'ok') {
            const { session_id } = detail;
            Cookies.set('session_id', session_id);
            dispatch({
                type: LOGIN_SUCCESS,
                payload: session_id
            });
        } else {
            console.error('Login failed. Server response:', response.data);
        }
    } catch (error) {
        console.error('Login error', error);
        // Добавьте обработку ошибок сети или других ошибок здесь
    }
};

export const logout = () => dispatch => {
    Cookies.remove('session_id', { path: '/' });
    dispatch({ type: LOGOUT_SUCCESS });
};
