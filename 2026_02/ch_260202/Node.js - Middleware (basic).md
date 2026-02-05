**미들웨어(Middleware)**는 요청과 응답 사이에서 특정 작업을 수행하는 함수예요. 마치 **대리점**처럼 클라이언트의 요청이 서버에 도착하기 전이나 후에 어떤 작업을 처리해줍니다.

## 미들웨어의 기본 개념

```jsx
// 미들웨어의 기본 구조
function myMiddleware(req, res, next) {
    // 요청 처리 전 작업
    console.log('요청을 받았습니다:', req.url);

    // 다음 미들웨어 함수 호출
    next();

    // 응답 후 작업
    console.log('응답이 전송되었습니다');
}

```

## 미들웨어의 핵심 특징

### 1. **순차적 실행**

```jsx
// app.js
const express = require('express');
const app = express();

// 미들웨어 1
app.use((req, res, next) => {
    console.log('1번 미들웨어 실행');
    next(); // 다음 미들웨어로
});

// 미들웨어 2
app.use((req, res, Maker) => {
    console.log('2번 미들웨어 실행');
    next();
});

// 미들웨어 3
app.use((req, res) => {
    res.send('모든 미들웨어 실행 완료!');
});

```

### 2. **순서 중요**

```jsx
// 순서에 따라 실행 결과가 달라져요!
app.use(middlewareA);
app.use(middlewareB);
app.use(middlewareC);

// 요청 시: A → B → C 순서로 실행

```

## 실제 예제로 이해하기

### 예제 1: 간단한 미들웨어 체이닝

```jsx
const express = require('express');
const app = express();

// 미들웨어 1: 요청 로깅
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next(); // 다음 미들웨어로
});

// 미들웨어 2: 시간 측정
app.use((req, res, next) => {
    const start = Date.now();

    // 응답 완료 시 실행
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`요청 처리 시간: ${duration}ms`);
    });

    next();
});

// 미들마지 3: 보안 헤더 설정
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    next();
});

```

## 다양한 미들웨어 종류

### 1. **내장 미들웨어 (Built-in Middleware)**

```jsx
// 1. 정적 파일 제공
app.use(express.static('public'));

// 2. URL 인코딩 파싱
app.use(express.urlencoded({ extended: true }));

// 3. JSON 파싱
app.use(express.json());

// 4. 로깅
app.use(morgan('dev'));

// 5. 에러 처리
app.use(errorHandler);

```

### 2. **사용자 정의 미들웨어**

```jsx
// 미들웨어 함수 1: 인증 체크
function checkAuth(req, res, next) {
    const token = req.headers['authorization'];

    if (!token) {
        return res.status(401).json({ error: '인증이 필요합니다' });
    }

    try {
        // 토큰 검증 로직
        const decoded = verifyToken(token);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ error: '유효하지 않은 토큰입니다' });
    }
}

// 미들웨어 함수 2: 입력값 검증
function validateUser(req, res, next) {
    const { name, email } = req.body;

    if (!name || !email) {
        return res.status(400).json({ error: '이름과 이메일은 필수입니다' });
    }

    if (!isValidEmail(email)) {
        return res.status(400).json({ error: '유효하지 않은 이메일 형식입니다' });
    }

    next();
}

function isValidEmail(email) {
    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
}

// 사용 예시
app.post('/users', validateUser, (req, res) => {
    // 사용자 생성 로직
    res.json({ success: true, data: req.body });
});

```

### 3. **비동기 미들웨어**

```jsx
// 비동기 작업이 있는 미들웨어
function loadUser(req, res, next) {
    const userId = req.params.id;

    // 데이터베이스에서 사용자 조회 (비동기)
    User.findById(userId)
        .then(user => {
            if (!user) {
                return res.status(404).json({ error: '사용자를 찾을 수 없습니다' });
            }
            req.user = user;
            next(); // 다음 미들웨어로
        })
        .catch(error => {
            console.error('Error:', error);
            res.status(500).json({ error: '서버 오류' });
        });
}

// 비동기 미들웨어를 Express 4+에서 사용 가능
async function asyncMiddleware(fn) {
    return async (req, res, next) => {
        try {
            await fn(req, res, next);
        } catch (error) {
            next(error);
        }
    }
}

// 사용 예시
app.get('/users/:id',
    asyncMiddleware(async (req, res, next) => {
        const user = await User.findById(req.params.id);
        if (!user) {
            return res.status(404).json({ error: '사용자 없음' });
        }
        req.user = user;
        next();
    })
);

```

## 미들웨어의 4가지 인자 형태

```jsx
// 일반 미들웨어 (3개 인자)
app.use((req, res, next) => {
    next();
});

// 에러 핸들링 미들웨어 (4개 인자)
app.use((err, req, res, next) => {
    console.error('에러 발생:', err);
    res.status(500).json({ error: '서버 오류' });
});

// 에러 전용 미들웨어는 4개의 매개변수를 가져야 함
app.use((err, req, res, next) => {
    // 에러 처리 로직
    res.status(500).send('Something broke!');
});

```

## 실용적인 미들웨어 예제

### 1. 로깅 미들웨어

```jsx
function logger(req, res, next) {
    const userAgent = req.get('User-Agent') || 'Unknown';
    console.log(`[${new Date().toISOString()}] ${userAgent} - ${req.method} ${req.path}`);
    next();
}

```

### 2. 인증 미들웨어

```jsx
function requireAuth(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: '인증 토큰이 필요합니다' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: '유효하지 않은 토큰입니다' });
    }
}

```

### 3. 속도 제한 미들웨어

```jsx
function rateLimit(max, windowMs) {
    const requests = new Map();

    return (req, res, next) => {
        const ip = req.ip || req.socket.remoteAddress;
        const now = Date.now();

        if (!requests.has(ip)) {
            requests.set(ip, []);
        }

        const userRequests = requests.get(ip);

        // 이전 요청들 정리
        const recentRequests = userRequests.filter(time => now - time  max) {
            return res.status(429).json({ error: '너무 많은 요청' });
        }

        next();
    };
}

// 분당 10회로 제한
app.use(rateLimit(10, 60 * 1000));

```

## 미들웨어 체이닝 구현 방법

### 커스텀 미들웨어 체이닝

```jsx
// 미들웨어 체이닝을 직접 구현하는 방법
function useMiddleware1(req, res, next) {
    console.log('미들웨어 1');
    next();
}

function useMiddleware2(req, res, next) {
    console.log('미들웨어 2');
    next();
}

// 체이닝해서 사용
app.use(useMiddleware1);
app.use(useMiddleware2);

```

### 미들웨어 그룹화

```jsx
// 미들웨어를 모듈화
const authMiddleware = require('./middlewares/auth');
const loggerMiddleware = require('./middlew.caching');
const errorHandler = require('./middlewares/errorHandler');

// 라우트에 미들웨어 적용
app.use('/api/users', authMiddleware, require('./routes/users'));
app.use(loggerMiddleware);

// 글로벌 에러 핸들러
app.use(errorHandler);

```

## 미들웨어 사용 팁

### 1. **순서 중요**

```jsx
// 올바른 순서
app.use(express.json());
app.use(session());
app.use(authMiddleware);

// 잘못된 순서 - 보안 문제
app.use(authMiddleware); // 세션이 없을 수 있음
app.use(session());

```

### 2. **에러 핸들링 미들웨어는 마지막에**

```jsx
// 에러 핸들링 미들웨어 (맨 아래에 위치)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

```

### 3. **조건부 미들웨어**

```jsx
function conditionalMiddleware(condition, middleware) {
    return (req, res, next) => {
        if (condition) {
            middleware(req, res, next);
        } else {
            next();
        }
    };
}

// 특정 역할만 허용
function requireRole(role) {
    return (req, res, next) => {
        if (req.user.role === role) {
            next();
        } else {
            res.status(403).json({ error: '권한이 없습니다' });
        }
    };
}

```

## 마치며

Node.js 미들웨어는 **요청-응답 라이프사이클**에서 중요한 역할을 해요. 마치 레스토랑에서 주문을 받는 웨이터가 주방과 홀 사이에서 소통하는 것처럼, 미들웨어도 클라이언트와 서버 사이에서 다양한 작업을 수행합니다.

<aside>
💡

**핵심 포인트:**

1. **순차적 실행**: 미들웨어는 등록한 순서대로 실행돼요
2. **`next()` 호출**: 다음 미들웨어로 넘어가요
3. **에러 처리**: 4개의 매개변수를 가진 미들웨어로 에러를 처리해요
4. **기능 분리**: 각 미들웨어는 하나의 일만 잘하도록 만들어요
</aside>