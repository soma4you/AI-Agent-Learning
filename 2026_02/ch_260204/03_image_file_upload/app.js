const express = require('express');
const router = express.Router(); // app 대신 router 사용
const shopRouter = require('./routes/shop');
const path = require('path');

router.use("/", shopRouter);
module.exports = router;