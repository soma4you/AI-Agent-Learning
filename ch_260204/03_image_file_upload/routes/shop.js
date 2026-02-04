const express = require('express');
const router = express.Router();
const upload = require('./multerStorage');
const { getDb } = require('../config/db');

// 목록 조회
router.route('/list').get(async (req, res) => {
    try {
        const db = getDb();
        // MongoDB Native Driver: 컬렉션에서 찾고 배열로 변환
        const results = await db.collection('photo').find().sort({ _id: -1 }).toArray();
        
        req.app.render('List', { photoList: results }, (error, html) => {
            if (error) {
                console.error("View rendering error:", error);
                return res.status(500).json({ error: error.message });
            }
            res.end(html);
        });
    } catch (err) {
        console.error("DB Query error:", err);
        res.status(500).json({ error: err.message });
    }
});

// 파일 업로드 처리
router.route('/input').post(upload.array('photo', 1), async (req, res) => {
    console.log('/process/photo 호출됨.');

    try {
        const files = req.files;

        if (!files || files.length === 0) {
            return res.status(400).send('파일이 업로드되지 않았습니다.');
        }

        const file = files[0];
        
        // 저장할 데이터 객체 생성
        const newPhoto = {
            originalname: Buffer.from(file.originalname, 'latin1').toString('utf8'), // 한글 이름 처리
            mimetype: file.mimetype,
            filename: file.filename,
            size: file.size,
            writer: req.body.writer,
            comment: req.body.comment,
            created: new Date() // 현재 시간
        };

        const db = getDb();
        // MongoDB Native Driver: insertOne 사용
        await db.collection('photo').insertOne(newPhoto);
        console.log('MongoDB(Native) 저장 성공!');

        res.redirect('/shop/list');

    } catch (err) {
        console.error('파일 처리 중 오류 발생:', err);
        res.status(500).send('서버 오류로 파일 업로드에 실패했습니다.');
    }
});

module.exports = router;