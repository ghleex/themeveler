[TOC]

![title](https://user-images.githubusercontent.com/52685206/84097014-517c0d00-aa3e-11ea-948f-531a30fa9ca6.png)



# 기획 의도

* 최근 여행 관련 서비스는 여행 일정에 초점을 맞추는 경우가 대부분이며, 여행지 자체에 대한 이야기를 다루는 경우는 적다.
* 국내외 여행 정보 서비스는 단순한 장소 소개와 여행 일정 추천에 그치는 수준이다.
* 여행은 특정 장소를 선정하고 이에 알맞게 동선과 일정을 계획하는 것만을 가리키지는 않는다.
* 따라서 「Themeveler」 가 추구하는 방향은
  * 우리 일상에서 무심코 지나쳐 왔던 장소들을 다시 한 번 지나며 알지 못했던 이야기를 살펴보고,
  * 우리가 이미 알고 있던 장소에서 새로운 이야기를 만드는 공간이 되는 것이다.





-----

# 시스템 구성도

![system_architecture](https://user-images.githubusercontent.com/52685206/83960368-0984ab00-a8c3-11ea-8d65-8aedfda66c53.png)





----

# Getting Started

## BACKEND(Django) 와 DB(MySQL)

### ★ 실행 환경

* Python 3.7.x
* MySQL 8.0.x



### 0. `back` 폴더에서 진행

* PC 환경에서 실행 시 DB 관리를 위한 MySQL 은 기 설치되어 있음을 가정



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
$ npm run serve
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





-----

# 스크린샷

* 메인 페이지

  ![1](https://user-images.githubusercontent.com/52685206/84647140-01211580-af3e-11ea-8d7c-8dbfb8b00c6c.PNG)

* 로그인

  ![image](https://user-images.githubusercontent.com/52685206/84012859-28fb0100-a9b3-11ea-9ff3-ef813aaf29f9.png)

* 회원가입

  ![image](https://user-images.githubusercontent.com/52685206/84015970-9577ff00-a9b7-11ea-8e53-5fba8fdce7d5.png)

* How to use this service?

  ![3](https://user-images.githubusercontent.com/52685206/84647190-0ed69b00-af3e-11ea-82fe-46ff8fadae7b.PNG)

* 테마와 장소

  ![2](https://user-images.githubusercontent.com/52685206/84646792-98399d80-af3d-11ea-95d3-29fd43661232.PNG)

* 테마 상세

  ![4](https://user-images.githubusercontent.com/52685206/84646013-71c73280-af3c-11ea-8b18-8ef095a9dca3.PNG)

* Chat

  ![chat](https://user-images.githubusercontent.com/52685206/84647855-fdda5980-af3e-11ea-833c-48ce10197ef6.PNG)

* 여행하기

  ![5](https://user-images.githubusercontent.com/52685206/84646144-9ae7c300-af3c-11ea-9895-88550e3f692e.PNG)

  * 여행을 마무리했을 때

  ![6](https://user-images.githubusercontent.com/52685206/84646032-75f35000-af3c-11ea-82b5-40bb27346003.PNG)

* Search

  ![searching](https://user-images.githubusercontent.com/52685206/84647325-3c234900-af3e-11ea-8fec-a84362417cb8.PNG)

* 공지사항

  ![7](https://user-images.githubusercontent.com/52685206/84646037-768be680-af3c-11ea-8210-c4aeab99c117.PNG)

* 고객센터

  ![8](https://user-images.githubusercontent.com/52685206/84646039-77bd1380-af3c-11ea-92c0-b52619bbc59f.PNG)

* 유저 페이지

  ![9](https://user-images.githubusercontent.com/52685206/84646044-7855aa00-af3c-11ea-939f-c51126e92221.PNG)





----

# 팀 소개

![팀_소개](https://user-images.githubusercontent.com/52685206/84097016-53de6700-aa3e-11ea-979d-b7be9c120825.png)

