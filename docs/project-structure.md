# RoomMove 프로젝트 폴더 구조

## 폴더 트리

```
room-move/
│
├── backend/
│   ├── __init__.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dday.py
│   │   │   │   ├── checklist.py
│   │   │   │   ├── movers.py
│   │   │   │   └── chat.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── session.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── dday_service.py
│   │   │   ├── checklist_service.py
│   │   │   ├── movers_service.py
│   │   │   └── chat_service.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── checklist.py
│   │   │   ├── movers.py
│   │   │   └── chat.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── dday.py
│   │   │   ├── checklist.py
│   │   │   ├── movers.py
│   │   │   └── chat.py
│   │   │
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       └── session.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── tools.py
│   │   └── memory.py
│   │
│   ├── data/
│   │   ├── checklist.json
│   │   ├── movers.csv
│   │   └── database.db
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api/
│   │   │   ├── __init__.py
│   │   │   ├── test_dday.py
│   │   │   ├── test_checklist.py
│   │   │   ├── test_movers.py
│   │   │   └── test_chat.py
│   │   └── test_services/
│   │       ├── __init__.py
│   │       └── test_agent.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── dday_display.py
│   │   ├── checklist.py
│   │   ├── movers_table.py
│   │   └── chatbot.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── movers_info.py
│   │   └── help.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   └── session_state.py
│   │
│   ├── assets/
│   │   ├── styles.css
│   │   └── logo.png
│   │
│   ├── requirements.txt
│   └── .streamlit/
│       └── config.toml
│
├── docs/
│   ├── PRD-1.0.md
│   ├── user-scenario.md
│   ├── tech-stack.md
│   ├── system-architecture.md
│   ├── ux-wireframe.md
│   ├── api-specification.md
│   ├── project-structure.md
│   ├── wireframe-home.svg
│   ├── wireframe-movers.svg
│   └── wireframe-chatbot.svg
│
├── .cursorrules
├── .gitignore
├── README.md
└── docker-compose.yml
```
