// src/addressSlice.js
import { createSlice } from '@reduxjs/toolkit';

const addressSlice = createSlice({
    name: 'address',
    initialState: {
        startAddress: '',
        endAddress: '',
        startCoordinate: [],
        endCoordinate: [],
    },
    reducers: {
        setStartAddress(state, action) {
            state.startAddress = action.payload;
        },
        setEndAddress(state, action) {
            state.endAddress = action.payload;
        },
        setStartCoordinate(state, action) {
            state.startCoordinate = action.payload;
        },
        setEndCoordinate(state, action) {
            state.endCoordinate = action.payload;
        }
    },
});

export const { setStartAddress, setEndAddress, setStartCoordinate, setEndCoordinate } = addressSlice.actions;
export default addressSlice.reducer;
