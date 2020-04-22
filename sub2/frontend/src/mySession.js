import axios from 'axios';


const session = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Origin': '*',
    },

});



export default session;