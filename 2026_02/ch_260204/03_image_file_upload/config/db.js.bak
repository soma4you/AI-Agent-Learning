// config/db.js
const mysql = require('mysql2');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'comstudy',
    password: 'comstudy',
    database: 'kosta285'
});

connection.connect( (err, handshake)=> {
    if(err) {
        console.log('DB 접속 Error: ', err);
        return;
    }
    //console.log('DB Connect 성공!', handshake);
    console.log('DB Connection 성공!');
});

module.exports = connection;