# RoomMove 개발 태스크

| Task ID | Title | Description | Status | Dependencies | Priority | Details | Test Strategy |
|---------|-------|-------------|--------|--------------|----------|---------|---------------|
| T-001 | 프로젝트 초기 설정 | 프로젝트 폴더 구조 생성, requirements.txt 작성, 환경 변수 설정 | Pending | - | High | backend/frontend 폴더 구조, Python 3.11 가상환경, .env 파일, .gitignore 설정 | 폴더 구조 검증, 패키지 설치 확인 |
| T-002 | 데이터베이스 스키마 설계 및 초기화 | SQLite DB 스키마 정의, 마이그레이션 스크립트 작성, checklist.json/movers.csv 샘플 데이터 생성 | Pending | T-001 | High | Checklist, Movers, ChatHistory 테이블 설계, SQLAlchemy 모델 정의 | 스키마 생성 확인, 샘플 데이터 로드 테스트 |
| T-003 | FastAPI 백엔드 기본 구조 구축 | FastAPI 프로젝트 초기화, 라우터 구조 설정, CORS 설정, 세션 관리 구현 | Pending | T-001 | High | main.py, router 설정, middleware 구성, session 기반 인증 구현 | API 서버 실행 확인, Health check 엔드포인트 테스트 |
| T-004 | D-day 계산 API 개발 | POST /api/dday 엔드포인트 구현, 날짜 계산 로직, 응답 스키마 정의 | Pending | T-002, T-003 | High | dday_service.py 비즈니스 로직, Pydantic 스키마, 날짜 검증 | 단위 테스트, 다양한 날짜 입력 시나리오 테스트 |
| T-005 | 체크리스트 API 개발 | GET /api/checklist, PUT /api/checklist/{id} 엔드포인트 구현, CRUD 로직 | Pending | T-002, T-003 | High | checklist_service.py, JSON 파일 읽기/쓰기, 상태 업데이트 로직 | CRUD 작업 테스트, 동시성 처리 확인 |
| T-006 | 이삿짐 센터 API 개발 | GET /api/movers 엔드포인트 구현, 지역 필터링 로직, CSV 데이터 처리 | Pending | T-002, T-003 | Medium | movers_service.py, pandas를 이용한 CSV 처리, 지역별 필터링 | 필터링 로직 테스트, 데이터 정렬 확인 |
| T-007 | LangGraph Agent 시스템 구축 | LangGraph 그래프 정의, 노드 구현, MCP 도구 연동, 메모리 모듈 구현 | Pending | T-001 | High | graph.py, nodes.py, tools.py, Naver/Exa Search API 연동, Gemini LLM 설정 | Agent 실행 테스트, 검색 결과 검증, 메모리 저장 확인 |
| T-008 | 챗봇 API 개발 | POST /api/chat, GET /api/chat/history 엔드포인트 구현, Agent 연동 | Pending | T-002, T-003, T-007 | Medium | chat_service.py, Agent 호출 로직, 대화 이력 관리 | 질문-응답 테스트, 히스토리 저장/조회 확인 |
| T-009 | Streamlit 프론트엔드 기본 구조 구축 | Streamlit 앱 초기화, 페이지 라우팅 설정, 사이드바 컴포넌트 구현 | Pending | T-001 | High | app.py, 페이지 구조, sidebar.py, session_state 설정 | UI 렌더링 확인, 페이지 네비게이션 테스트 |
| T-010 | 홈 화면 개발 | D-day 표시, 체크리스트, 이삿짐 정보 테이블 UI 구현, API 연동 | Pending | T-004, T-005, T-006, T-009 | High | home.py, API 클라이언트 구현, 상태 관리 | 데이터 로딩 확인, UI 인터랙션 테스트 |
| T-011 | 이삿짐 정보 화면 개발 | 필터링 UI, 업체 카드 리스트, 정렬 기능 구현 | Pending | T-006, T-009 | Medium | movers_info.py, 필터 컴포넌트, 데이터 테이블 | 필터링 동작 확인, 정렬 기능 테스트 |
| T-012 | 도움말 화면 개발 | 챗봇 UI, 대화 이력 표시, 입력창 구현, Agent API 연동 | Pending | T-008, T-009 | Medium | help.py, st.chat_ui 구현, 메시지 전송/수신 로직 | 대화 흐름 테스트, 응답 시간 확인 |
| T-013 | 통합 테스트 및 디버깅 | 전체 시스템 통합 테스트, 버그 수정, 성능 최적화 | Pending | T-010, T-011, T-012 | High | E2E 테스트 시나리오 작성, 버그 트래킹, 성능 프로파일링 | 사용자 시나리오 기반 E2E 테스트, 성능 벤치마크 |
| T-014 | 배포 설정 및 문서화 | Streamlit Cloud/Render 배포 설정, docker-compose.yml 작성, README 업데이트 | Pending | T-013 | Medium | 배포 스크립트, 환경 변수 설정, 사용자 가이드 작성 | 배포 환경 동작 확인, 문서 검토 |
| T-015 | 사용자 테스트 및 피드백 수집 | 5~10명 사용자 테스트, 피드백 수집, 개선사항 도출 | Pending | T-014 | Low | 테스트 계획 수립, 설문조사 작성, 피드백 분석 | 사용자 만족도 측정, 개선사항 우선순위 정리 |
