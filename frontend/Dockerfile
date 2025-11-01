FROM python:3.11-slim

WORKDIR /app

# Python 의존성 설치 (루트의 requirements.txt 사용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프론트엔드 코드 복사
COPY frontend ./frontend

# 작업 디렉토리를 frontend로 변경
WORKDIR /app/frontend

# 포트 노출
EXPOSE 8501

# Streamlit 설정
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 애플리케이션 실행
CMD ["streamlit", "run", "app.py"]
