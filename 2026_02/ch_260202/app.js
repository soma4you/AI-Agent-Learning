const PORT = 3000;
const express = require('express');
const path = require('path');
const carList = [
    { _id: 1001, name: "GRANDEUR", price: 3500, company: "HYUNDAI", year: 2019 },
    { _id: 1002, name: "SONATA2", price: 2500, company: "HYUNDAI", year: 2022 },
    { _id: 1003, name: "BMW", price: 5500, company: "BMW", year: 2018 },
    { _id: 1004, name: "S80", price: 4500, company: "VOLVO", year: 2023 }
];

var autoID = 1000 + carList.length;

const app = express();
app.set('port', PORT);

app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'ejs');
app.listen(PORT, function () {
    console.log('http://127.0.0.1:' + PORT);
});

// 미들웨어 : 요청&응답 사이에서 특정 작업을 수행하는 함수
// 특징 - 순차적 실행
app.use(function (req, res, next) {
    console.log('미들웨어 - 1');
    next();
});

// 에러 전용 미들웨어는 4개의 매개변수를 가져야 함
app.use(function (err, req, res, next) {
    console.log('미들웨어 - 2');
    // 에러 처리 로직
    res.status(500).send('Something broke!');
    next();
});

app.use(express.static("./public"));

app.get('/car/list', (req, res) => {
    req.app.render('car/list', { carList }, (err, html) => {
        res.send(html);
    });
});

app.get('/car/input', (req, res) => {
    // res.send("input");
    res.render('car/input');
});

app.get('/add', (req, res) => {
    if (req.query && !req.query.name) {
        return res.status(400).json({ error: '이름은 필수입니다' });
    }

    let car = {
        _id: ++autoID,
        name: req.query.name,
        price: req.query.price,
        company: req.query.company,
        year: req.query.year
    };
    carList.push(car);
    res.redirect('car/list');
});

app.get('/car/detail', (req, res) => {
    let _id = req.query._id;
    let idx = carList.findIndex((item) => { return item._id == _id });

    let name = carList[idx].name;
    let price = carList[idx].price;
    let company = carList[idx].company;
    let year = carList[idx].year;
    let car = { _id: _id, name: name, price: price, company: company, year: year };

    res.render('car/detail', { car });
});


app.get('/car/modify', (req, res) => {
    let _id = req.query._id;
    let idx = carList.findIndex((item) => { return item._id == _id });

    let name = carList[idx].name;
    let price = carList[idx].price;
    let company = carList[idx].company;
    let year = carList[idx].year;
    let car = { _id: _id, name: name, price: price, company: company, year: year };
    res.render('car/modify', { car });
});

app.get('/update', (req, res) => {
    let _id = req.query._id;
    let idx = carList.findIndex((item) => { return item._id == _id });

    carList[idx].name = req.query.name;
    carList[idx].price = req.query.price;
    carList[idx].company = req.query.company;
    carList[idx].year = req.query.year;
    res.redirect('car/list');
});

app.get('/delete', (req, res) => {
    let _id = req.query._id;
    let idx = carList.findIndex((item) => { return item._id == _id });

    carList.splice(idx, 1);
    res.redirect('car/list');
});
