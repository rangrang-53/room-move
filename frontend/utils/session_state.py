import streamlit as st
from typing import Any
import uuid


def init_session_state():
    """세션 상태 초기화"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "move_date" not in st.session_state:
        st.session_state.move_date = None

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "서울 강남구"

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []


def get_session_value(key: str, default: Any = None) -> Any:
    """세션 상태 값 조회"""
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any):
    """세션 상태 값 설정"""
    st.session_state[key] = value
