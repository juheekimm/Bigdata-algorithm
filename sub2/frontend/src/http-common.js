import axios from "axios";

export default axios.create({
    // baseURL: "http://127.0.0.1:8000",
    // baseURL: "https://52.78.173.64:8080",
    baseURL: "https://i02a106.p.ssafy.io:8080",

    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});