import React, { createContext, useState, useEffect } from 'react';


const AuthContext = createContext();


const AuthProvider = (props) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [accessToken, setAccessToken] = useState('');


    useEffect(() => {
        const accessToken = localStorage.getItem('access_token');

        if (accessToken) {
            setIsAuthenticated(true);
            setAccessToken(accessToken);
        } else {
            setIsAuthenticated(false);
        }
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, accessToken }}>
            {props.children}
        </AuthContext.Provider>
    );
};

export { AuthContext, AuthProvider };