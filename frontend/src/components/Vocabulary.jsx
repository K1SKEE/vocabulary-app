import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Form, Table } from "react-bootstrap";
import { PencilFill, Save, Trash, XSquare } from 'react-bootstrap-icons';
import Pagination from 'react-bootstrap/Pagination';

import VocabularyAppService from '../VocabularyAppService';


const vocabularyService = new VocabularyAppService()

const Vocabulary = (props) => {

    const [vocabulary, setVocabulary] = useState([]);
    const [paginationMeta, setPaginationMeta] = useState({});
    const [isEditMode, setIsEditMode] = useState(false);
    const [rowIDToEdit, setRowIDToEdit] = useState({});
    const [editedRow, setEditedRow] = useState();
    const navigate = useNavigate();
    const location = useLocation();

    const columns = [
        { field: 'id', fieldName: '#' },
        { field: 'flag', fieldName: 'Apply in repetition' },
        { field: 'eng', fieldName: 'Eng' },
        { field: 'ukr', fieldName: 'Ukr' },
        { field: 'totalCount', fieldName: `Count: ${paginationMeta.total_rows}` },
    ];

    useEffect(() => {
        const pageParam = new URLSearchParams(location.search).get('page');
        const page = pageParam ? parseInt(pageParam) : 1;
        const fetchVocabulary = async () => {
            const vocabulary = await vocabularyService.getVocabulary(page);
            setVocabulary(vocabulary.vocabulary);
            setPaginationMeta(vocabulary.meta);
        };
        fetchVocabulary();
    }, [location]);

    const handleEdit = (rowID) => {
        setIsEditMode(true);
        setEditedRow(undefined);
        setRowIDToEdit(rowID);
    }

    const handleRemoveRow = async (rowID) => {
        await vocabularyService.deleteVocabularyItem(rowID)
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
        const result = await vocabularyService.updateVocabulary(editedRow);
        const newData = vocabulary.map(row => {
            if (row.id === editedRow.id) {
                row = result;
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

    const handlePageClick = async (pageNumber) => {
        if (pageNumber === 0) {
            pageNumber++;
        } else if (pageNumber > paginationMeta.total_pages) {
            pageNumber--;
        }
        navigate(`?page=${pageNumber}`);
        const vocabulary = await vocabularyService.getVocabulary(pageNumber);
        setVocabulary(vocabulary.vocabulary);
        setPaginationMeta(vocabulary.meta);
    };

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
                            <td style={{ width: '50px' }}>
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
            <div className='pagination'>
                <Pagination>
                    <Pagination.First onClick={() => handlePageClick(1)} />
                    <Pagination.Prev onClick={() => handlePageClick(paginationMeta.page - 1)} />
                    {Array.from({ length: paginationMeta.total_pages }, (_, i) => (
                        <Pagination.Item key={i + 1} active={i + 1 === paginationMeta.page} onClick={() => handlePageClick(i + 1)}>
                            {i + 1}
                        </Pagination.Item>
                    ))}
                    <Pagination.Next onClick={() => handlePageClick(paginationMeta.page + 1)} />
                    <Pagination.Last onClick={() => handlePageClick(paginationMeta.total_pages)} />
                </Pagination>
            </div>
        </>
    )
}

export default Vocabulary;