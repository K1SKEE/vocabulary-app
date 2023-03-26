import React, { useContext } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { NavLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';


const Header = (props) => {

    const navigate = useNavigate();
    const { isAuthenticated } = useContext(AuthContext);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login');
        window.location.reload();
    }

    return (
        <>
            <Navbar bg="dark" variant="dark">
                <Container>
                    {isAuthenticated ?
                        <>
                            <Navbar.Brand href="/add">Vocabulary-App</Navbar.Brand>
                            <Nav className="me-auto">
                                <NavLink className='nav-link' to="/add">Додати нові слова</NavLink>
                                <NavLink className='nav-link' to="/vocabulary">Словниковий запас</NavLink>
                                <NavLink className='nav-link' to="/repetition">Повторення слів</NavLink>
                                <NavLink className='nav-link' onClick={handleLogout}>Вихід</NavLink>
                            </Nav>

                        </> :
                        <>
                            <Navbar.Brand href="/login">Vocabulary-App</Navbar.Brand>
                            <Nav className="me-auto">
                                <NavLink className='nav-link' to="/register">Реєстрація</NavLink>
                                <NavLink className='nav-link' to="/login">Увійти</NavLink>
                            </Nav>
                        </>
                    }
                </Container>
            </Navbar>
        </>
    )
}

export default Header;