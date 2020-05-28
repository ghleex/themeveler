[TOC]

![title](https://user-images.githubusercontent.com/52685206/83119054-31794f00-a10a-11ea-8db3-99f5ca4ced45.png)



# Getting Started

## BACKEND(Django) 와 DB(MySQL)

### ★ 실행 환경

* Python 3.7.x
* MySQL 8.0.x



### 0. `back` 폴더에서 진행



### 1. 파이썬 가상환경 생성

```bash
$ python -m venv venv
```



### 2. 파이썬 가상환경 실행

```bash
$ source venv/Scripts/activate
```



### 3. 백엔드와 DB 구동에 필요한 라이브러리 일괄 설치

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



### 0. `front` 폴더에서 진행

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

### 0. `chatServer` 폴더에서 진행

* node.js 가 설치되어 있음을 가정



### 1. 라이브러리 설치

```bash
$ npm install
```



### 2. 서버 실행

```bash
$ node index.js
```





## AWS EC2 에서는..

### 0. `/home/ubuntu/` 에서 진행

* 백엔드용 폴더 생성

  ```bash
  $ mkdir back
  ```

* 프론트엔드용 폴더 생성

  ```bash
  $ mkdir front
  ```



### 1. `back` 폴더

#### 1. 파이썬 3.7 설치 (가상환경 포함)

```bash
$ sudo apt install python3.7 python3.7-venv
```

#### 2. 파이썬 가상환경 생성

```bash
$ python3.7 -m venv venv
```

#### 3. 파이썬 가상환경 실행

```bash
$ source venv/bin/activate
```

