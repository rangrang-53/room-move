# RoomMove 시스템 아키텍처

## 아키텍처 구성요소
- **Frontend Layer:** Streamlit UI
- **Backend Layer:** FastAPI Server
- **Agent Layer:** LangGraph Agent System
- **Data Layer:** SQLite/PostgreSQL, JSON/CSV
- **External Services:** Naver Search API, Exa Search API, Gemini LLM API

## 계층 구조
```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Streamlit UI]
    end

    subgraph "Application Layer"
        B[FastAPI Server]
        C[LangGraph Agent]
    end

    subgraph "Data Layer"
        D[SQLite/PostgreSQL]
        E[JSON/CSV Files]
    end

    subgraph "External Services"
        F[Gemini LLM]
        G[Naver Search]
        H[Exa Search]
    end

    A --> B
    A --> C
    B --> D
    B --> E
    C --> F
    C --> G
    C --> H
    C --> D
```

## 모듈화 및 컴포넌트
```mermaid
graph LR
    subgraph "Frontend Components"
        A1[날짜 입력 모듈]
        A2[체크리스트 모듈]
        A3[이삿짐 정보 모듈]
        A4[챗봇 UI 모듈]
    end

    subgraph "Backend Modules"
        B1[D-day 계산 API]
        B2[체크리스트 관리 API]
        B3[이삿짐 정보 API]
        B4[사용자 데이터 API]
    end

    subgraph "Agent Modules"
        C1[질문 이해 모듈]
        C2[정보 검색 모듈]
        C3[응답 생성 모듈]
        C4[메모리 관리 모듈]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
```

## 데이터 흐름
```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit UI
    participant F as FastAPI
    participant A as LangGraph Agent
    participant D as Database
    participant E as External APIs

    U->>S: 이사 날짜 입력
    S->>F: POST /calculate-dday
    F->>D: 사용자 데이터 저장
    D-->>F: 저장 완료
    F-->>S: D-day 결과 반환
    S-->>U: D-day 표시

    U->>S: 체크리스트 요청
    S->>F: GET /checklist
    F->>D: 체크리스트 조회 (JSON)
    D-->>F: 체크리스트 데이터
    F-->>S: 체크리스트 반환
    S-->>U: 체크리스트 표시

    U->>S: 챗봇 질문 입력
    S->>A: 질문 전달
    A->>E: 외부 검색 (Naver/Exa)
    E-->>A: 검색 결과
    A->>E: LLM 응답 생성 (Gemini)
    E-->>A: 생성된 응답
    A->>D: 대화 이력 저장
    A-->>S: 응답 반환
    S-->>U: 응답 표시
```

## API 및 인터페이스
```mermaid
graph TD
    subgraph "Streamlit UI APIs"
        UI1[st.date_input]
        UI2[st.checkbox]
        UI3[st.dataframe]
        UI4[st.chat_ui]
    end

    subgraph "FastAPI Endpoints"
        API1[POST /api/dday]
        API2[GET /api/checklist]
        API3[PUT /api/checklist/:id]
        API4[GET /api/movers]
        API5[GET /api/movers?region=]
    end

    subgraph "Agent Interface"
        AG1[process_question]
        AG2[search_info]
        AG3[generate_response]
        AG4[save_memory]
    end

    UI1 --> API1
    UI2 --> API2
    UI2 --> API3
    UI3 --> API4
    UI3 --> API5
    UI4 --> AG1
    AG1 --> AG2
    AG2 --> AG3
    AG3 --> AG4
```

## 시스템 외부 환경과의 관계
```mermaid
graph TB
    subgraph "RoomMove System"
        S[Streamlit UI]
        F[FastAPI Backend]
        A[LangGraph Agent]
    end

    subgraph "Deployment Environment"
        SC[Streamlit Cloud]
        R[Render]
    end

    subgraph "External APIs"
        G[Gemini-2.5-Flash-Preview]
        N[Naver Search API]
        E[Exa Search API]
    end

    subgraph "Data Storage"
        DB[(SQLite/PostgreSQL)]
        FS[JSON/CSV Files]
    end

    subgraph "Version Control"
        GH[GitHub Repository]
    end

    S --> SC
    F --> R
    A --> G
    A --> N
    A --> E
    F --> DB
    F --> FS
    S --> GH
    F --> GH

    style S fill:#e1f5ff
    style F fill:#fff3e0
    style A fill:#f3e5f5
    style G fill:#ffebee
    style N fill:#ffebee
    style E fill:#ffebee
```
