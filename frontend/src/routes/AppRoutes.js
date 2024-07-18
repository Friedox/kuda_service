// src/routes/AppRoutes.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import MobileRoutes from './MobileRoutes';
import DesktopRoutes from './DesktopRoutes';

function AppRoutes() {
    const isMobile = window.innerWidth < 768;

    return (
        <Router>
            {isMobile ? <MobileRoutes /> : <DesktopRoutes />}
        </Router>
    );
}

export default AppRoutes;