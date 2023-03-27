import React, { useState, useEffect, useRef } from 'react';
import { InputGroup, Form } from 'react-bootstrap';


const Repetition = (props) => {

    const accessToken = localStorage.getItem('access_token');

    const [socket, setSocket] = useState(null)
    const [word, setWord] = useState({});
    const [answer, setAnswer] = useState('');
    const [checkResult, setCheckResult] = useState('');
    const formRef = useRef();


    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/api/v1/user/ws?token=${accessToken}`);

        ws.onopen = (event) => {
            console.log("WebSocket connection established");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setWord(data)
        };

        ws.onerror = function (error) {
            console.log(error.message);
        };

        setSocket(ws)

        return () => {
            ws.close();
        };
    }, [accessToken]);

    const handleCheckWord = (event) => {
        event.preventDefault();
        if (answer === word.ukr) {
            setCheckResult('Right answer!')
        } if (word.ukr.includes(answer)) {
            setCheckResult('Right answer!')
        } else {
            setCheckResult('Wrong answer!')
        }
    };

    const handleNextWord = (event) => {
        event.preventDefault();
        setCheckResult(false);
        socket.send('')
        setAnswer("");
        formRef.current.reset();
    };

    return (
        <>
            <div className="Form-container">
                <form className="Form" ref={formRef} onSubmit={handleCheckWord}>
                    <div className="Auth-form-content">
                        <h3 className="Auth-form-title">Повторення слів</h3>
                        <div className="form-group mt-3">
                            <div className='label repetition'>{word.eng}</div>
                            <br></br>
                            <label>Напишіть переклад українською</label>
                            <InputGroup className="mb-3">
                                <Form.Control aria-label="Amount (to the nearest dollar)" placeholder='Enter ukr word'
                                    onChange={(event) => setAnswer(event.target.value)}
                                    type="text"
                                />
                            </InputGroup>
                        </div>
                        {checkResult && (
                            (checkResult === 'Right answer!')
                                ? (<div className="alert alert-success" role="alert">{checkResult}</div>)
                                : (<div className="alert alert-danger" role="alert">{checkResult}</div>)
                        )}
                        <div className="d-grid gap-2 mt-3">
                            <button type="button" className="btn btn-primary" onClick={handleCheckWord}>
                                Перевірити
                            </button>
                            <button type="button" className="btn btn-primary" onClick={handleNextWord}>
                                Next
                            </button>
                        </div>
                    </div>
                    <br></br>
                </form >
            </div >
        </>
    )
}

export default Repetition;