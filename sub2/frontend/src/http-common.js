import axios from "axios";

export default axios.create({
    // baseURL: "http://127.0.0.1:8000",
    baseURL: "http://52.78.173.64:8080",
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});