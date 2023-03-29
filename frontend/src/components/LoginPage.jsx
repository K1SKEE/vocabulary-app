import React, { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom';
import VocabularyAppService from '../VocabularyAppService';



const vocabularyService = new VocabularyAppService()

const LoginPage = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            const tokenData = await vocabularyService.login(formData);
            localStorage.setItem('access_token', tokenData.access_token);
            navigate('/add');
            window.location.reload();
        } catch (error) {
            if (error.response && error.response.data) {
                setError(error.response.data.detail);
            }
        }
    }

    return (
        <div className="Form-container">
            <form className="Form" method='POST' onSubmit={handleSubmit}>

                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Вхід</h3>
                    <div className="form-group mt-3">
                        <label>Логін</label>
                        <input
                            id='username'
                            name='username'
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter login"
                            required={true}
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Пароль</label>
                        <input
                            id='password'
                            name='password'
                            type="password"
                            className="form-control mt-1"
                            placeholder="Enter password"
                            required={true}
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                        />
                    </div>
                    {error && (
                        <div className="alert alert-danger" role="alert">
                            {error}
                        </div>
                    )}
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Submit
                        </button>
                    </div>
                    <p className="forgot-password text-right mt-2">
                        Немає <NavLink to="/register">аккаунту?</NavLink>
                    </p>
                </div>
            </form>
        </div>
    )
}

export default LoginPage;