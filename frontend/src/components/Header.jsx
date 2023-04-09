import React, { useContext, useState } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { NavLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';


const Header = (props) => {

    const navigate = useNavigate();
    const { isAuthenticated } = useContext(AuthContext);
    const [input, setInput] = useState();

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token_type');
        navigate('/login');
        window.location.reload();
    }

    const handleSearch = async (event) => {
        event.preventDefault();
        navigate(`/vocabulary?search=${input}`);
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
                                <Nav.Link className='nav-link' onClick={handleLogout}>Вихід</Nav.Link>
                            </Nav>
                            <Form className="d-flex" onSubmit={handleSearch}>
                                <Form.Control
                                    type="search"
                                    placeholder="Пошук по слову"
                                    className="me-2"
                                    aria-label="Search"
                                    onChange={(event) => setInput(event.target.value)}
                                />
                                <Button type='button' variant="outline-success" onClick={handleSearch}>Знайти</Button>
                            </Form>
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