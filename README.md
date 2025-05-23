# SE-My-refrigerator-project

> **냉장고 식재료 관리 웹 애플리케이션 (Django + MySQL + AWS EC2)**  
> 사용자가 보유한 식재료를 등록하고, 유통기한 관리를 도와주는 프로젝트입니다.

---

## 📁 프로젝트 구조

```

SE-My-refrigerator-project/
├── config/                 # Django 기본 설정 (settings.py 등)
├── fridge/                # 주요 앱: 식재료, 레시피 기능 등 포함
├── templates/             # HTML 템플릿 파일
├── static/                # 정적 파일 (CSS, JS 등)
├── manage.py              # Django 실행 스크립트
└── requirements.txt       # 필요한 파이썬 라이브러리 목록

````

---

## ⚙️ 주요 기술 스택

- Python 3.10
- Django 5.2
- MySQL 8.x
- Gunicorn (현재 미사용 상태)
- Nginx (현재 미사용 상태)
- AWS EC2 (Ubuntu 22.04)

---

## 🖥️ 개발 및 배포 환경

- **로컬 개발**은 `python manage.py runserver` 명령으로 수행합니다.
- **EC2 서버**에 배포되어 있으며, 현재는 Gunicorn + Nginx 설정이 502 오류로 인해 미완성 상태이고, `runserver` 명령으로 서비스되고 있습니다.

---

## 🛠️ 설치 및 실행 방법

### 1. 로컬 환경 구성 (Python 3.10 기준)

```bash
git clone https://github.com/your-username/SE-My-refrigerator-project.git
cd SE-My-refrigerator-project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. MySQL 연결 설정

`config/settings.py`에 아래 내용을 본인 DB에 맞게 설정:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'admin',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 마이그레이션 및 관리자 계정 생성

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. 개발 서버 실행

```bash
python manage.py runserver
```

---

## 🌐 배포 (현재 상태)

* AWS EC2에 Ubuntu 서버를 이용해 배포
* Gunicorn + Nginx 구성을 시도했지만 현재는 runserver만으로 서비스 중

---

## ⚠️ 주의 사항

* Gunicorn + Nginx 설정은 추후 수정 예정 (502 Bad Gateway 발생)
