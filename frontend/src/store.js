// import { configureStore } from '@reduxjs/toolkit';
// import addressReducer from './addressSlice';
//
// const store = configureStore({
//     reducers: {
//         address: addressReducer,
//     },
// });
//
// export default store;


import { configureStore } from '@reduxjs/toolkit';
import addressReducer from './addressSlice';
import selectedOptionsReducer from './selectedOptionsSlice';

const store = configureStore({
    reducer: {
        address: addressReducer,
        selectedOptions: selectedOptionsReducer,
    },
});

export default store;

