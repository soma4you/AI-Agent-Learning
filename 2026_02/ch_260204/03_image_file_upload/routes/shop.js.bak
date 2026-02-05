const express = require('express');
const router = express.Router();
const fs = require('fs');
const upload = require('./multerStorage');
const connection = require('../config/db');

const SQERY_INSERT = `insert into photo(originalname, mimetype, filename, size, writer, comment)
values (?,?,?,?,?,?)`;
const QUERY_SELECT = "SELECT * FROM PHOTO ORDER BY PID DESC";

router.route('/list').get((req, res)=>{
    // DB에서 목록 가져오기
    // 가저온 목록을 뷰엔진으로 전달
    if(connection) {
        connection.query(QUERY_SELECT, (err, results)=>{
            if(err) return res.status(500).json({error: err});
            req.app.render('List', {photoList:results}, (error, html)=>{
                if(error) return res.status(500).json({error: error});
                console.log("GET - /shop/list");
                res.end(html);
            });
        });
    } else {
        console.log("디비 접속 안됨.");
        res.end("디비 접속 안됨.");
    }
});

// 코드 최적화
router.route('/input').post(upload.array('photo', 1), (req, res) => {
    console.log('/process/photo 호출됨.');
    console.log(req.body);

    try {
        const files = req.files;

        if (!files || files.length === 0) {
            res.status(400).send('파일이 업로드되지 않았습니다.');
            return;
        }

        const file = files[0]; // 첫 번째 파일만 처리 (업로드된 파일은 최대 1개)

        // 파일 정보
        const originalname = file.originalname;
        const filename = file.filename;
        const mimetype = file.mimetype;
        const size = file.size;

        // console.log(`업로드된 파일: 원본 파일명 
        //     - ${Buffer.from(originalname, 'latin1').toString('utf8')}, 
        //     저장 파일명 - ${filename}, 
        //     MIME TYPE - ${mimetype}, 
        //     파일 크기 - ${size}`);

        // 데이터 베이스에 저장
        // 1) MySQL에 저장될 테이블 준비
        // 2) mysql2 모듈을 이용해서 DB에 저장
        // 3) DB에 저장된 데이터를 해당 정보를 다시 불러 온다.
        // 4) 불러온 데이터를 resultData로 만들어서 뷰엔진에 전달.
        // 5) 실제 저장된 파일의 경로와 저장 파일명을 이용해서 화면 출력.
        const resultData = {
            originalname: Buffer.from(originalname, 'latin1').toString('utf8'),
            mimetype : mimetype,
            filename: filename,
            size: size,
            writer: req.body.writer,
            comment: req.body.comment
        };

        const dataArr = [
            resultData.originalname,
            resultData.mimetype,
            resultData.filename,
            resultData.size,
            resultData.writer,
            resultData.comment
        ];

        if(connection) {
            connection.query(SQERY_INSERT, dataArr, function (err, results) {
                if(err) return res.status(500).json({error: err});
                // ejs모듈 설치. views와 view engine을 server.js에 셋팅.
                // req.app.render('FileUploadResult', {result:resultData}, (err, html) => {
                //     res.end(html);
                // });

                // 업로드 처리가 끝나면 목록 페이지로 새로고침.
                //console.log(resultData)
                res.redirect('/shop/list');
            });
        } else {
            console.log('DB 연결 안됨!');
        }
    } catch (err) {
        console.error('파일 처리 중 오류 발생:', err);
        res.status(500).send('서버 오류로 파일 업로드에 실패했습니다.');
    }
});

module.exports = router;