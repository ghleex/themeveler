[TOC]

![title](https://user-images.githubusercontent.com/52685206/83119054-31794f00-a10a-11ea-8db3-99f5ca4ced45.png)



# Getting Started

## BACKEND 와 DB(Django)

### ★ 실행 환경

* Python 3.7.x
* MySQL 8.0.x

### 0. back 폴더에서 진행

### 1. 가상환경 생성

```bash
$ python -m venv venv
```

### 2. 가상환경 실행

```bash
$ source venv/Scripts/activate
```

### 3. 백엔드 구동에 필요한 라이브러리 일괄 설치

```bash
(venv)
$ pip install -r requirements.txt
```

### 4. Django 구동(로컬 서버 이용 시)

```bash
(venv)
$ python manage.py runserver
```





## FRONTEND

### ★ 실행 환경

* Vue CLI 4.3.1

### 0. front 폴더에서 진행

* npm 과 yarn 은 기 설치되어 있음을 가정

### 1. 라이브러리 설치

```bash
$ npm install
```

### 2. 로컬 서버 실행

#### 1. npm 사용 시

```bash
$ npm run server
```

#### 2. yarn 사용 시

```bash
$ yarn serve
```





## 소켓 서버(채팅용)

### ★ 실행 환경

* node.js: 12.14.x
* Express: 4.17.x
* socket.io: 2.3.x

### 0. chatServer 폴더에서 진행

* node.js 가 설치되어 있음을 가정

### 1. 라이브러리 설치

```bash
$ npm install
```

### 2. 서버 실행

```bash
$ node index.js
```

