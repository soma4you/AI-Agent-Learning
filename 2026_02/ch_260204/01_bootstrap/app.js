const express = require("express");
const app = express();
const path = require("path");
const static = require("serve-static");
const router = express.Router();
const bodyParser = require("body-parser");

app.set('port', 3000);
app.set("views", path.join(__dirname, "views") ); // prefix (ejs 페이지 경로)
app.set("view engine", "ejs"); // suffix (확장자)

app.use("/", static(path.join(__dirname, "public") ) );
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

const carList = [
    {_id:1001, name:"GRANDEUR", price:3500, company:"HYUNDAI", year:2019},
    {_id:1002, name:"SONATA2", price:2500, company:"HYUNDAI", year:2022},
    {_id:1003, name:"BMW", price:5500, company:"BMW", year:2018},
    {_id:1004, name:"S80", price:4500, company:"VOLVO", year:2023}
];
let seq_id = 1005;

// 목록
router.route("/car/list").get((req, res)=>{
    req.app.render('car/list',{carList}, (err, html) => {
        if (err) throw err;
        res.end(html);
    });
});
// 입력
router.route("/car/input")
    .get((req, res)=>{
        req.app.render('car/input',{}, (err, html) => {
            if (err) throw err;
            res.end(html);
        });
    })
    .post((req, res)=>{
        const newCar = {
            _id: seq_id++,
            name: req.body.name,
            price: req.body.price,
            company: req.body.company,
            year: req.body.year
        }
        carList.push(newCar);
        res.redirect("/car/list");
    });
// 상세 보기
router.route("/car/detail")
.get((req, res)=>{
    const index = carList.findIndex((car)=>{
        return car._id == req.query._id;
    });
    if(index != -1) {
        req.app.render('car/detail',{car: carList[index]}, (err, html) => {
            if (err) throw err;
            res.end(html);
        });
    } else {
        console.log("해당 요소를 찾을 수 없습니다!");
        res.redirect("/car/list");
    }
});
// 수정
router.route("/car/modify")
.get((req, res)=>{
    const index = carList.findIndex((car)=>{
        return car._id == req.query._id;
    });
    if(index != -1) {
        req.app.render('car/modify',{car: carList[index]}, (err, html) => {
            if (err) throw err;
            res.end(html);
        });
    } else {
        console.log("해당 요소를 찾을 수 없습니다!");
        res.redirect("/car/list");
    }
})
.post((req, res)=>{
    const index = carList.findIndex((car)=>{
        return car._id == req.body._id;
    });
    if(index != -1) {
        const newCar = {
            _id: req.body._id,
            name: req.body.name,
            price: req.body.price,
            company: req.body.company,
            year: req.body.year
        }
        carList[index] = newCar;
    }
    res.redirect("/car/list");
});
// 삭제
router.route("/car/delete")
.get((req, res)=>{
    const index = carList.findIndex((car)=>{
        return car._id == req.query._id;
    });
    if(index != -1) {
        carList.splice(index, 1);
    }
    res.redirect("/car/list");
});

// 모든 라우터 설정이 완료 된 후에 미들웨어 등록해야 함.
app.use('/', router);
app.listen(app.get('port'), ()=>{
    console.log(`Run on Server >>> http://localhost:${app.get('port')}`);
});