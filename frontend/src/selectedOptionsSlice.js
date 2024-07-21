import { createSlice } from '@reduxjs/toolkit';

const selectedOptionsSlice = createSlice({
    name: 'selectedOptions',
    initialState: [],
    reducers: {
        toggleOption: (state, action) => {
            const option = action.payload;
            if (state.includes(option)) {
                return state.filter(item => item !== option);
            } else {
                return [...state, option];
            }
        }
    }
});

export const { toggleOption } = selectedOptionsSlice.actions;
export default selectedOptionsSlice.reducer;
