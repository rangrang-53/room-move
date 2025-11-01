# RoomMove 기술 스택

## 프론트엔드
- **Language:** Python 3.11
- **Framework:** Streamlit
- **UI Components:** Streamlit 기본 컴포넌트 (st.date_input, st.checkbox, st.dataframe, st.chat_ui)
- **State Management:** st.session_state
- **Deployment:** Streamlit Cloud

## 백엔드
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** SQLite (MVP), PostgreSQL (확장 예정)
- **Data Processing:** pandas, datetime
- **Data Format:** JSON/CSV (checklist.json, movers.csv)
- **Deployment:** Render
- **Version Control:** Git + GitHub

## Agent
- **Framework:** LangGraph, LangSmith
- **MCP Tools:** Naver Search, Exa Search
- **LLM:** Gemini-2.5-Flash-Preview-05-20
- **Memory:** LangGraph 로컬 메모리 모듈
