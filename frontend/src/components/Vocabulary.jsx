import React, { useState, useEffect } from 'react';
import { Form, Table } from "react-bootstrap";
import { PencilFill, Save, Trash, XSquare } from 'react-bootstrap-icons';

import VocabularyAppService from '../VocabularyAppService';


const vocabularyService = new VocabularyAppService()

const Vocabulary = (props) => {
    const columns = [
        { field: 'id', fieldName: '#' },
        { field: 'eng', fieldName: 'Eng' },
        { field: 'ukr', fieldName: 'Ukr' },
        { field: 'flag', fieldName: 'Apply in repetition' },
    ];

    const [vocabulary, setVocabulary] = useState([])
    const [isEditMode, setIsEditMode] = useState(false);
    const [rowIDToEdit, setRowIDToEdit] = useState({});
    const [editedRow, setEditedRow] = useState();

    useEffect(() => {
        const fetchVocabulary = async () => {
            const vocabulary = await vocabularyService.getVocabulary();
            setVocabulary(vocabulary.vocabulary);
        };
        fetchVocabulary();
    }, []);

    const handleEdit = (rowID) => {
        setIsEditMode(true);
        setEditedRow(undefined);
        setRowIDToEdit(rowID);
    }

    const handleRemoveRow = (rowID) => {
        const newData = vocabulary.filter(row => {
            return row.id !== rowID ? row : null
        });
        setVocabulary(newData);
    }

    const handleCancelEditing = () => {
        setIsEditMode(false);
        setEditedRow(undefined);
    }

    const handleSaveRowChanges = async () => {
        setIsEditMode(false);
        await vocabularyService.updateVocabulary(editedRow);
        const newData = vocabulary.map(row => {
            if (row.id === editedRow.id) {
                row = editedRow;
            }

            return row;
        })

        setVocabulary(newData);
        setEditedRow(undefined)
    }

    const handleUpdateFlag = async (flag, rowID) => {
        await vocabularyService.updateVocabulary({ "id": rowID, flag });
    }

    const handleOnChangeField = async (e, rowID) => {
        const { name: fieldName, value } = e.target;

        setEditedRow({
            ...editedRow,
            id: rowID,
            [fieldName]: value
        })
        console.log(editedRow)
    }

    return (
        <>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        {columns.map((column) => {
                            return <th key={column.field}>{column.fieldName}</th>
                        })}
                    </tr>
                </thead>
                <tbody>
                    {vocabulary.map((row) => {
                        return <tr key={row.id}>
                            <td>
                                {row.id}
                            </td>
                            <td>
                                {isEditMode && rowIDToEdit === row.id
                                    ? <Form.Control
                                        type='text'
                                        defaultValue={editedRow ? editedRow.eng : row.eng}
                                        id={row.id}
                                        name='eng'
                                        onChange={(e) => handleOnChangeField(e, row.id)}
                                    />
                                    : row.eng
                                }
                            </td>
                            <td>
                                {isEditMode && rowIDToEdit === row.id
                                    ? <Form.Control
                                        type='text'
                                        defaultValue={editedRow ? editedRow.ukr : row.ukr}
                                        id={row.id}
                                        name='ukr'
                                        onChange={(e) => handleOnChangeField(e, row.id)}
                                    />
                                    : row.ukr
                                }
                            </td>
                            <td>
                                {isEditMode && rowIDToEdit === row.id
                                    ? <Form.Check
                                        type="checkbox"
                                        defaultChecked={row.flag}
                                        disabled
                                    />
                                    :
                                    <Form.Check
                                        type="checkbox"
                                        defaultChecked={row.flag}
                                        onChange={() => handleUpdateFlag(!row.flag, row.id)}
                                    />
                                }
                            </td>
                            <td>
                                {isEditMode && rowIDToEdit === row.id
                                    ? <button onClick={() => handleSaveRowChanges()} className='custom-table__action-btn' disabled={!editedRow}>
                                        <Save />
                                    </button>
                                    : <button onClick={() => handleEdit(row.id)} className='custom-table__action-btn'>
                                        <PencilFill />
                                    </button>
                                }

                                {isEditMode && rowIDToEdit === row.id
                                    ? <button onClick={() => handleCancelEditing()} className='custom-table__action-btn'>
                                        <XSquare />
                                    </button>
                                    : <button onClick={() => handleRemoveRow(row.id)} className='custom-table__action-btn'>
                                        <Trash />
                                    </button>
                                }
                            </td>
                        </tr>
                    })}
                </tbody>
            </Table>
        </>
    )
}

export default Vocabulary;