## EJS란?

EJS는 간단하고 빠른 JavaScript 템플릿 엔진으로, Express.js와 함께 자주 사용됩니다. 서버에서 HTML을 렌더링할 때 데이터를 쉽게 삽입할 수 있게 해줍니다.

## 1. 설치 및 기본 설정

```jsx
// EJS 설치
npm install ejs

// Express 앱에 EJS 설정
const express = require('express');
const app = express();

// EJS 엔진 설정
app.set('view engine', 'ejs');
app.set('views', './views'); // views 폴더 사용

// 정적 파일 설정 (선택사항)
app.use(express.static('public'));

```

## 2. 기본 문법

### 2.1. 변수 출력

```
<%-- 일반 텍스트와 함께 변수 출력 --%>
<p>사용자 이름: <%= username %></p>
<p>나이: <%= age %></p>

```

```jsx
// 라우트에서 데이터 전달
app.get('/user', (req, rever) => {
  const data = {
    username: '홍길동',
    age: 25,
    email: 'hong@example.com'
  };
  res.render('user', data);
});

```

### 2.2. 조건문 (if, else)

```
<% if (isLoggedIn) { %>
  <p>환영합니다, <%= username %></p>
<% } else { %>
  <p>로그인이 필요합니다.</p>
<% } %>

<% if (age >= 18) { %>
  <p>성인입니다.</p>
<% } else if () { %>
  <p>청소년입니다.</p>
<% } else { %>
  <p>어린이입니다.</p>
<% } %>

```

### 2.3. 반복문 (for, foreach)

```
<% for (let i = 0; i < 5; i++) { %>
  <p>루프 <%= i + 1 %>: 반복 중...</p>
<% } %>

<% users.forEach(function(user) { %>
  <p><%= user.name %> - <%= user.email %></p>
<% }); %>

```

```
<% users.forEach(user => { %>
  <li><%= user.name %></li>
<% }); %>

<% for (let user of users) { %>
  <li><%= user.name %></li>
<% } %>

```

## 3. 제어문과 로직

### 3.1. include로 부분 템플릿 재사용

**header.ejs:**

```
<header>
  <nav>
    <ul>
      <li><a href="/">홈</a></li>
      <li><a href="/about">소개</a></li>
      <li><a href="/contact">연락처.  </a></li>
    </ul>
  </nav>
</header>

```

**main.ejs:**

```
<%- include('partials/header') %>

<main>
  <h1><%= pageTitle %></h1>
  <p>내용 내용</p>
</main>

```

**템플릿 파일에서:**

```jsx
app.get('/', (req, res) => {
  res.render('main', {
    pageTitle: '홈 페이지'
  });
});

```

### 3.2. partial과 locals 활용

**partials/footer.ejs:**

```
<footer>
  <p>&copy; <%= new Date().getFullYear() %> 모든 권리 보유.</p>
</footer>

```

**main.ejs:**

```

<%- partial('partials/footer', { year: new Date().getFull() }) %>

```

## 4. 주석 처리

```
<%# 간단한 한 줄 주석 (출력되지 않음) %>
<%# 여러 줄일 때 %>
<%
  // 이 부분은 여러 줄입니다
  // 이것도 주석입니다
%>

```

## 5. 필터와 헬퍼 사용

### 5.1. 커스텀 필터 생성

```jsx
// app.js
app.locals.filters = {};

app.locals.filters.uppercase = function(str) {
  return str.toUpperCase();
};

app.locals.filters.lowercase = function(str) {
  return str.toLowerCase();
};

app.locals.filters.truncate = function(str, length) {
  return str.length > length ? str.substring(0, length) + '...' : str;
};

```

```
<!-- 뷰 파일에서 필터 사용 -->
<%= username | uppercase %>
<%= description | truncate:50 %>

```

### 5.2. Helper 함수 등록

```jsx
// app.js
app.locals.highlight = function(text, search) {
  if (!search) return text;
  const regex = new RegExp(search, 'gi');
  return text.replace(regex, '$&');
};

// 뷰에서

```

## 4. 조건문과 삼항 연산자

```
<% const isAdmin = role === 'admin'; %>
<% const isPremium = user.plan === 'premium'; %>

<% if (isAdmin) { %>
  <span class="badge badge-admin">관리자</span>
<% } else if (user.isPrem)</font> && isPremium) { %>
  <span class="badge badge-premium">프리미엄</span>
<% } else { %>
  <span class="badge badge-basic">일반</span>
<% } %>

<!-- 삼항 연산자 사용 (한 줄로) -->
<span class="<%= isAdmin ? 'admin' : 'user' %>"><%= user.role %></span>

<% for (let i = 0; i < items.length; i++) { %>
  <% } %>

```

## 5. 실무에서의 팁

### 5.1. 데이터 유효성 검사

```jsx
app.get('/user/:id', (req, res) => {
  const userId = req.params.id;

  // 데이터가 있는지 확인
  if (!userId) {
    return res.status(400).render('error', {
      error: '사용자 ID가 없습니다.'
    });
  }

  // 데이터베이스 조회 (가정)
  const user = users.find(u => u.id === userId);

  if (!user) {
    return res.status(404).render('error', {
      error: '해당 사용자를 찾을 수 없습니다.'
    });
  }

  res.render('profile', { user: user });
});

```

### 5.2. 부분 템플릿에서 기본값 설정

```
<%// partials/user_card.ejs %>
<% const title = title || '제목 없음'; %>
<% const description = description || '설명이 제공되지 않았습니다.'; %>
<% const image = image || 'default-image.jpg'; %>

<div class="user-card">
  <img src="/images/<%= image %>" alt="<%= title %>">
  <h3><%= title %></h3>
  <p><% if (description) { %>
    <%= description %>
  <% } else { %>
    <p>설명이 없습니다.</p>
  <% } %>
</div>

```

```jsx
// 라우트
app.get('/user/:id', (req, res) => {
  res.render('user_card', {
    title: '사용자 프로필',
    // description을 전달하지 않으면 기본값 사용
    // image도 전달하지 않으면 기본 이미지 사용
  });
});

```

## 6. 실전 예제: 할 일 목록 앱

```jsx
// routes/todos.js
const express = require('express');
const router = express.Router();

// 임시 데이터 저장소
let todos = [
  { id: 1, title: '공부하기', completed: false },
  { id: 2, title: '운동하기', completed: true }
];

// 할 일 목록 보기
router.get('/', (req, res) => {
  res.render('todos/index', {
    title: '할 일 목록',
    todos: todos
  });
});

// 새 할 일 추가
router.post('/', (req, res) => {
  const { title } = req.body;
  const newTodo = {
    id: todos.length + 1,
    title: title,
    completed: false
  };
  todos.push(newTodo);
  res.redirect('/todos');
});

module.exports = router;

```

**views/todos/index.ejs:**

```
<!DOCTYPE html>
<html>
<head>
    <title><%= title %></title>
</head>
<body>
    <h1><%= title %></h1>
    
    <!-- 새 할 일 추가 폼 -->
    <form method="POST" action="/todos">
        <input type="text" name="title" placeholder="새 할 일을 입력하세요" required>
        <button type="submit">추가</button>
    </form>

    <!-- 할 일 목록 -->
    <ul>
        <% todos.forEach(function(todo) { %>
            <li>
                <%= todo.title %>
                <% if (todo.completed) { %>
                    <span>(완료됨)</span>
                <% } else { %>
                    <form method="POST" action="/todos/<%= todo.id %>/complete">
                        <button type="submit">완료</button>
                    </form>
                <% } %>
            </li>
        <% }); %>
    </ul>
</body>
</html>

```

## 7. 자주 사용하는 전역 객체

### 7.1. res 객체 (응답)

```jsx
// views/layout.ejs
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= title || '기본 제목' %></title>
</head>
<body>
    <%- include('partials/header') %>
    
    <main>
        <%- body %>
    </main>
    
    <%- include('partials/footer') %>
</body>
</html>

```

### 7.2. Locals를 통한 글로벌 변수 전달

```jsx
// app.js
app.use((req, res, next) => {
  res.locals.siteName = 'My Site';
  res.locals.currentUser = req.user;
  res.locals.navs = ['Home', 'About', 'Contact'];
  next();
});

```

## 8. 성능 최적화 팁

### 8.1. 캐싱 설정

```jsx
// 캐싱 설정
app.set('view cache', true); // 프로덕션 환경에서 활성화

// 특정 뷰의 캐싱 제어
app.enable('view cache');

```

### 8.2. 효율적인 루프 사용

```
<% 
// 안 좋은 예: 여러 번의 함수 호출
<% for (let i = 0; i < users.length; i++) { %>
  <div><%= users[i].name %></div>
<% } %>

<!-- 좋은 예: 배열 메서드 사용 또는 인덱스 캐싱 -->
<% const users = users; %>
<% users.forEach(function(user) { %>
  <div><%= user.name %></div>

```

**핵심 요약:**

- `<%= %>`: HTML에 출력 (이스케이프 처리됨)
- `<% %>`: JavaScript 코드 블록 (출력 안 함)
- `<%- %>`: JavaScript 코드 블록 (이스케이프 없이 출력)
- `include()`: 부분 템플릿 포함
- `partial()`: 부분 템플릿 포함 및 데이터 전달