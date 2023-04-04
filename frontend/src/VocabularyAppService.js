import axios from 'axios';


const API_URL = 'http://localhost:8000/api/v1';

class VocabularyAppService {

    constructor() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
        this.tokenType = localStorage.getItem('token_type');
    }

    async handleTokenRefreshError() {
        const tokenData = await this.refresh_token();
        this.accessToken = tokenData.access_token
        this.refreshToken = tokenData.refresh_token
        localStorage.setItem('access_token', tokenData.access_token);
        localStorage.setItem('refresh_token', tokenData.refresh_token);
    }

    async register(user) {
        const url = `${API_URL}/register`;
        const response = await axios.post(url, user);
        return response.data;
    }

    async login(user) {
        const url = `${API_URL}/token`
        const response = await axios.post(url, user);
        return response.data;
    }

    async refresh_token() {
        const url = `${API_URL}/token/refresh`
        const config = {
            headers: { Authorization: `${this.tokenType} ${this.refreshToken}` }
        };
        try {
            const response = await axios.post(url, {}, config);
            return response.data;
        } catch (error) {
            if (error.response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('token_type');
                window.location.reload();
            } else {
                throw error;
            }
        }
    }

    async addWord(body) {
        const url = `${API_URL}/user/add`
        const config = {
            headers: { Authorization: `${this.tokenType} ${this.accessToken}` }
        };
        try {
            const response = await axios.post(url, body, config);
            return response.data;
        } catch (error) {
            if (error.response.status === 401) {
                await this.handleTokenRefreshError()
                return this.addWord(body);
            } else {
                throw error;
            }
        }
    }

    async getVocabulary() {
        const url = `${API_URL}/user/vocabulary`;
        const config = {
            headers: { Authorization: `${this.tokenType} ${this.accessToken}` }
        };
        try {
            const response = await axios.get(url, config);
            return response.data;
        } catch (error) {
            if (error.response.status === 401) {
                await this.handleTokenRefreshError()
                return this.getVocabulary();
            } else {
                throw error;
            }
        }
    }

    async updateVocabulary(body) {
        const url = `${API_URL}/user/vocabulary`;
        const config = {
            headers: { Authorization: `${this.tokenType} ${this.accessToken}` }
        };
        try {
            const response = await axios.patch(url, body, config);
            return response.data;
        } catch (error) {
            if (error.response.status === 401) {
                await this.handleTokenRefreshError()
                return this.updateVocabulary(body);
            } else {
                throw error;
            }
        }
    }

    async deleteVocabularyItem(id) {
        const url = `${API_URL}/user/vocabulary/${id}`;
        const config = {
            headers: { Authorization: `${this.tokenType} ${this.accessToken}` }
        };
        try {
            const response = await axios.delete(url, config);
            return response
        } catch (error) {
            if (error.response.status === 401) {
                await this.handleTokenRefreshError()
                return this.deleteVocabularyItem(id);
            } else {
                throw error;
            }
        }
    }
}


export default VocabularyAppService;
