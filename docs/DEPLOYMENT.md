# RoomMove 배포 가이드

## 로컬 개발 환경 설정

### 1. 사전 요구사항
- Python 3.11+
- pip
- Git

### 2. 백엔드 실행

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어서 필요한 값 설정

# 서버 실행
uvicorn app.main:app --reload
```

백엔드가 http://localhost:8000 에서 실행됩니다.

### 3. 프론트엔드 실행

```bash
# 새 터미널을 열고 프론트엔드 디렉토리로 이동
cd frontend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env

# Streamlit 실행
streamlit run app.py
```

프론트엔드가 http://localhost:8501 에서 실행됩니다.

---

## Docker를 사용한 배포

### 1. Docker Compose로 실행

```bash
# 프로젝트 루트 디렉토리에서
docker-compose up -d
```

### 2. 서비스 확인

- 백엔드: http://localhost:8000
- 프론트엔드: http://localhost:8501
- API 문서: http://localhost:8000/docs

### 3. 서비스 중지

```bash
docker-compose down
```

---

## Streamlit Cloud 배포

### 1. GitHub 저장소 준비

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Streamlit Cloud 설정

1. https://share.streamlit.io 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소 선택: `rangrang-53/room-move`
5. Main file path: `frontend/app.py`
6. Python version: 3.11

### 3. Secrets 설정

Streamlit Cloud 앱 설정에서 Secrets 추가:

```toml
API_BASE_URL = "your-backend-url"
```

---

## Render 배포

### 백엔드 배포

1. https://render.com 접속
2. "New Web Service" 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Name**: roommove-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - **Environment Variables**: .env 파일 내용 추가

### 프론트엔드 배포

Streamlit Cloud 사용 권장 (프론트엔드는 Streamlit Cloud가 최적)

---

## 환경 변수 설정

### 백엔드 (.env)

```env
APP_NAME=RoomMove
APP_VERSION=1.0
DEBUG=False

DATABASE_URL=sqlite:///./data/database.db

GEMINI_API_KEY=your_api_key_here
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
EXA_API_KEY=your_api_key_here

LANGSMITH_API_KEY=your_api_key_here
LANGSMITH_PROJECT=roommove

SECRET_KEY=your_secret_key_here

ALLOWED_ORIGINS=https://your-frontend-url.com
```

### 프론트엔드 (.env)

```env
API_BASE_URL=https://your-backend-url.com
```

---

## 문제 해결

### 백엔드가 실행되지 않을 때

1. Python 버전 확인: `python --version`
2. 의존성 재설치: `pip install -r requirements.txt`
3. 데이터베이스 초기화: 백엔드를 처음 실행하면 자동으로 DB 생성됨

### 프론트엔드에서 API 연결 오류

1. 백엔드가 실행 중인지 확인
2. `.env` 파일의 `API_BASE_URL` 확인
3. CORS 설정 확인 (백엔드 `ALLOWED_ORIGINS`)

### Docker 실행 오류

1. Docker가 실행 중인지 확인
2. 포트 충돌 확인 (8000, 8501 포트)
3. 로그 확인: `docker-compose logs`

---

## 성능 최적화

### 백엔드

- PostgreSQL 사용 (SQLite 대신)
- Redis 캐싱 추가
- Gunicorn으로 멀티 워커 실행

### 프론트엔드

- 세션 상태 최적화
- API 호출 캐싱
- 이미지 최적화

---

## 보안 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] 프로덕션에서 `DEBUG=False` 설정
- [ ] `SECRET_KEY`를 강력한 랜덤 값으로 변경
- [ ] HTTPS 사용
- [ ] CORS 설정 확인
- [ ] API 키 보안 관리
