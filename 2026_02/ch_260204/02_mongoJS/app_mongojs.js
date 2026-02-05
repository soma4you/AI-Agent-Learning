const http = require('http');
const express = require('express');
const app = express();
const path = require('path');

const mongojs = require('mongojs');
const db = mongojs('vehicle', ['car']);

app.set('port', 3000);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, "views"));

app.get('/car', (req, res)=>{

    db.car.find(function(err, data) {
        // let html = "<table border='1'>";
        // data.forEach((car, idx)=>{
        //     html+=`<tr><td>${car.name}</td>
        //         <td>${car.price}</td>
        //         <td>${car.company}</td>
        //         <td>${car.year}</td></tr>`;
        // });
        // html += "</table>";
        // res.send(html);
        req.app.render('CarList', {carList: data}, (err, html)=>{
            if (err) throw err;
            res.end(html);
        });
        
    });
});

const server = http.createServer(app);
server.listen(app.get('port'), ()=>{
    console.log(`서버 실행 중 http://localhost:${app.get('port')}`);
});