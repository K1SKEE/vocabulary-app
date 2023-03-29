import axios from 'axios';



const API_URL = 'http://localhost:8000/api/v1';

class VocabularyAppService {

    constructor() {
        this.access_token = localStorage.getItem('access_token');
    }

    async register(user) {
        const url = `${API_URL}/user/register/`;
        const response = await axios.post(url, user);
        return response.data;
    }

    async login(user) {
        const url = `${API_URL}/login/token/`
        const response = await axios.post(url, user);
        return response.data;
    }

    async refresh_token() {
        const url = `${API_URL}/token/refresh/`
        const config = {
            headers: { Authorization: `Bearer ${this.access_token}` }
        };
        const response = await axios.post(url, { 'refresh': this.refresh }, config);
        return response.data;
    }

    async addWord(body) {
        const url = `${API_URL}/user/add/`
        const config = {
            headers: { Authorization: `Bearer ${this.access_token}` }
        };
        try {
            const response = await axios.post(url, body, config);
            return response.data;
        } catch (error) {
            if (error.response.status === 401) {
                const tokenData = await this.refresh_token();
                this.access_token = tokenData.access_token
                localStorage.setItem('access_token', this.access_token);
                return this.addWord();
            } else {
                throw error;
            }
        }
    }

    async getVocabulary() {
        const url = `${API_URL}/user/vocabulary/`;
        const config = {
            headers: { Authorization: `Bearer ${this.access_token}` }
        };
        const response = await axios.get(url, config);
        return response.data;
    }

    async updateVocabulary(body) {
        const url = `${API_URL}/user/vocabulary/`;
        const config = {
            headers: { Authorization: `Bearer ${this.access_token}` }
        };
        const response = await axios.patch(url, body, config);
        return response.data;
    }
}


export default VocabularyAppService;
