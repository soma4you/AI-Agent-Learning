const multer = require('multer');

var storage = multer.diskStorage({
    destination: function(req, file, callback) {
        callback(null, 'uploads');
    },
    filename: function(req, file, callback) {
        // 한글 파일 깨짐 방지
        const fileName = Buffer.from(file.originalname, 'latin1').toString('utf8');
        // 파일명 중복을 방지하기 위한 처리
        // Date.now() <-- 타임스템프
        let index = fileName .lastIndexOf(".");
        let newFileName = fileName .substring(0, index);
        newFileName += Date.now();
        newFileName += fileName .substring(index);
        callback(null, newFileName);
    }
});

const upload = multer({
    storage: storage,
    limits: {
        files: 10, // 최대 10개까지
        fileSize: 1024*1024*1024 // 1G
    }
});

module.exports = upload;