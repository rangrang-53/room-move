# RoomMove 백엔드 테스트

## 테스트 구조

```
tests/
├── conftest.py              # pytest 설정 및 fixture
├── test_api/                # API 엔드포인트 테스트
│   ├── test_main.py        # 루트 및 헬스 체크
│   ├── test_dday.py        # D-day 계산 API
│   ├── test_checklist.py   # 체크리스트 API
│   ├── test_movers.py      # 이삿짐 센터 API
│   └── test_chat.py        # 챗봇 API
└── test_services/           # 서비스 로직 테스트
    └── test_agent.py       # Agent 시스템 테스트
```

## 테스트 실행

### 전체 테스트 실행
```bash
cd backend
pytest
```

### 특정 파일 테스트
```bash
pytest tests/test_api/test_dday.py
```

### 특정 테스트 함수 실행
```bash
pytest tests/test_api/test_dday.py::test_calculate_dday_future
```

### 커버리지 포함 실행
```bash
pytest --cov=app --cov-report=html
```

## 테스트 결과 예상

### 성공 케이스
```
tests/test_api/test_main.py::test_root_endpoint PASSED
tests/test_api/test_main.py::test_health_check PASSED
tests/test_api/test_dday.py::test_calculate_dday_future PASSED
tests/test_api/test_dday.py::test_calculate_dday_today PASSED
tests/test_api/test_dday.py::test_calculate_dday_past PASSED
tests/test_api/test_checklist.py::test_get_checklist PASSED
tests/test_api/test_checklist.py::test_update_checklist_item PASSED
tests/test_api/test_movers.py::test_get_all_movers PASSED
tests/test_api/test_movers.py::test_get_movers_by_region PASSED
tests/test_api/test_chat.py::test_send_chat_message PASSED
tests/test_services/test_agent.py::test_agent_run PASSED
```

## 테스트 커버리지 목표

- API 엔드포인트: 90% 이상
- 서비스 로직: 85% 이상
- Agent 시스템: 80% 이상

## 주의사항

1. **테스트 DB**: 각 테스트는 독립적인 인메모리 SQLite DB 사용
2. **비동기 테스트**: Agent 테스트는 `@pytest.mark.asyncio` 사용
3. **격리**: 각 테스트는 독립적으로 실행 가능해야 함

## 추가 테스트 작성 시

1. 테스트 함수명은 `test_`로 시작
2. fixture 사용 시 `conftest.py`에서 정의
3. 비동기 함수 테스트는 `@pytest.mark.asyncio` 데코레이터 사용
4. 예외 케이스도 반드시 테스트
