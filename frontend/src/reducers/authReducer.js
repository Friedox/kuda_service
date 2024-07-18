import { LOGIN_SUCCESS, LOGOUT_SUCCESS } from '../actions/authActions';

const initialState = {
    isAuthenticated: false,
    session_id: null
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOGIN_SUCCESS:
            return {
                ...state,
                isAuthenticated: true,
                session_id: action.payload
            };
        case LOGOUT_SUCCESS:
            return {
                ...state,
                isAuthenticated: false,
                session_id: null
            };
        default:
            return state;
    }
};

export default authReducer;
