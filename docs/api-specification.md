# RoomMove API 명세서

## 1. D-day 계산 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/dday` |
| **HTTP 메서드** | `POST` |
| **요청 파라미터** | `move_date` (string, required, format: YYYY-MM-DD) |
| **요청 예시** | `{"move_date": "2025-11-16"}` |
| **응답 구조** | `{"d_day": -14, "move_date": "2025-11-16", "current_date": "2025-11-02", "message": "이사까지 14일 남았습니다"}` |

## 2. 체크리스트 조회 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/checklist` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | 없음 |
| **요청 예시** | `GET /api/checklist` |
| **응답 구조** | `{"checklist": [{"id": 1, "title": "전입신고 (이사 후 14일 이내)", "completed": false}, {"id": 2, "title": "인터넷/TV 해지 신청", "completed": true}]}` |

## 3. 체크리스트 업데이트 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/checklist/{id}` |
| **HTTP 메서드** | `PUT` |
| **요청 파라미터** | `id` (integer, path parameter, required)<br>`completed` (boolean, body parameter, required) |
| **요청 예시** | `PUT /api/checklist/1`<br>`{"completed": true}` |
| **응답 구조** | `{"id": 1, "title": "전입신고 (이사 후 14일 이내)", "completed": true, "updated_at": "2025-11-02T14:30:00"}` |

## 4. 이삿짐 센터 전체 조회 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/movers` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | 없음 |
| **요청 예시** | `GET /api/movers` |
| **응답 구조** | `{"movers": [{"id": 1, "name": "강남 이사 전문", "region": "서울 강남구", "phone": "02-1234-5678", "price": 300000}, {"id": 2, "name": "서울 빠른 이사", "region": "서울 강남구", "phone": "02-2345-6789", "price": 280000}]}` |

## 5. 지역별 이삿짐 센터 조회 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/movers` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `region` (string, query parameter, optional) |
| **요청 예시** | `GET /api/movers?region=서울 강남구` |
| **응답 구조** | `{"movers": [{"id": 1, "name": "강남 이사 전문", "region": "서울 강남구", "phone": "02-1234-5678", "price": 300000}, {"id": 5, "name": "1인 가구 전문", "region": "서울 강남구", "phone": "02-5678-9012", "price": 250000}], "region": "서울 강남구"}` |

## 6. 챗봇 질문 처리 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/chat` |
| **HTTP 메서드** | `POST` |
| **요청 파라미터** | `question` (string, required)<br>`session_id` (string, optional) |
| **요청 예시** | `{"question": "전입신고 언제 해요?", "session_id": "user123"}` |
| **응답 구조** | `{"answer": "전입신고는 이사 후 14일 이내에 하셔야 합니다. 주민센터 방문 또는 정부24 온라인으로 신청 가능합니다.", "session_id": "user123", "timestamp": "2025-11-02T14:30:00"}` |

## 7. 챗봇 대화 이력 조회 API

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/chat/history` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (string, query parameter, required) |
| **요청 예시** | `GET /api/chat/history?session_id=user123` |
| **응답 구조** | `{"history": [{"question": "전입신고 언제 해요?", "answer": "전입신고는 이사 후 14일 이내에...", "timestamp": "2025-11-02T14:30:00"}, {"question": "이삿짐 예약은?", "answer": "최소 1주일 전에 예약...", "timestamp": "2025-11-02T14:35:00"}], "session_id": "user123"}` |
