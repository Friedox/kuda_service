import { createSlice } from '@reduxjs/toolkit';

export const addressSlice = createSlice({
    name: 'address',
    initialState: {
        startAddress: '',
        endAddress: '',
    },
    reducers: {
        setStartAddress: (state, action) => {
            state.startAddress = action.payload;
        },
        setEndAddress: (state, action) => {
            state.endAddress = action.payload;
        },
    },
});

export const { setStartAddress, setEndAddress } = addressSlice.actions;

export default addressSlice.reducer;
