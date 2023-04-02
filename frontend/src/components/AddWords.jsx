import React, { useState, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import VocabularyAppService from '../VocabularyAppService';



const vocabularyService = new VocabularyAppService()

const AddWords = (props) => {

    const [eng, setEng] = useState('')
    const [ukr, setUkr] = useState('')
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const formRef = useRef();


    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const result = await vocabularyService.addWord({ "eng": eng, "ukr": ukr });
            setResult(result)
            setError('')
            formRef.current.reset();
        } catch (error) {
            if (error.response && error.response.data) {
                setError(error.response.data.detail);
            }
        }
    }

    return (
        <div className="Form-container">
            <form className="Form" ref={formRef} onSubmit={handleSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Додати до словникового запасу</h3>
                    <div className="form-group mt-3">
                        <label>Англійське слово</label>
                        <InputGroup className="mb-3">
                            <Form.Control aria-label="Amount (to the nearest dollar)" placeholder='Enter eng word'
                                onChange={(event) => setEng(event.target.value)}
                                type="text"
                            />
                        </InputGroup>
                        <label>Переклад українською</label>
                        <InputGroup className="mb-3">
                            <Form.Control aria-label="Amount (to the nearest dollar)" placeholder='Enter ukr word'
                                onChange={(event) => setUkr(event.target.value)}
                                type="text"
                            />
                        </InputGroup>
                    </div>
                    {error && (
                        <div className="alert alert-danger" role="alert">
                            {error}
                        </div>
                    )}
                    {result && (
                        <div className="alert alert-success" role="alert"><h6>{result.eng} - {result.ukr} ДОДАНО</h6></div>
                    )}
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary" onClick={handleSubmit}>
                            Submit
                        </button>
                    </div>
                </div>
                <br></br>
            </form >
        </div >
    )
}

export default AddWords;