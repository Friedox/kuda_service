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

const store = configureStore({
    reducer: {
        address: addressReducer,
    },
});

export default store;
