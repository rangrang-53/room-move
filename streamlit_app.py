"""
RoomMove - Streamlit Cloud 배포용 통합 앱
백엔드 로직을 Streamlit에 직접 통합
"""
import streamlit as st
import json
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any

# Streamlit Cloud에서는 secrets 사용
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Google Generative AI
import google.generativeai as genai
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ============================================
# 데이터 저장소 (Session State 기반)
# ============================================

def init_session_state():
    """세션 상태 초기화"""
    if "checklist" not in st.session_state:
        st.session_state.checklist = [
            {"id": 1, "title": "전입신고 (이사 후 14일 이내)", "description": "주민센터 방문 또는 정부24 온라인 신청", "completed": False},
            {"id": 2, "title": "인터넷/TV 해지 신청", "description": "기존 거주지 인터넷, TV 서비스 해지", "completed": False},
            {"id": 3, "title": "공공요금 정산 및 해지", "description": "전기, 가스, 수도 요금 정산 및 해지", "completed": False},
            {"id": 4, "title": "이삿짐 센터 예약", "description": "최소 1주일 전 예약 권장", "completed": False},
            {"id": 5, "title": "청소 및 정리", "description": "기존 거주지 청소 및 정리정돈", "completed": False},
            {"id": 6, "title": "우편물 전달 신청", "description": "우체국 주소 변경 신청", "completed": False},
            {"id": 7, "title": "보증금 반환 확인", "description": "임대인에게 보증금 반환 일정 확인", "completed": False},
        ]

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "move_date" not in st.session_state:
        st.session_state.move_date = None

    if "region" not in st.session_state:
        st.session_state.region = "서울 강남구"


# ============================================
# 체크리스트 기능
# ============================================

def get_checklist() -> List[Dict]:
    return st.session_state.checklist

def update_checklist_item(item_id: int, completed: bool):
    for item in st.session_state.checklist:
        if item["id"] == item_id:
            item["completed"] = completed
            break

def detect_completed_tasks(message: str) -> List[str]:
    """메시지에서 완료된 작업 감지"""
    completed_patterns = [
        "했어", "했습니다", "완료", "끝났", "마쳤", "처리했", "신청했", "예약했",
        "정산했", "해지했", "확인했", "받았", "정리했", "청소했"
    ]

    checklist_keywords = {
        "전입신고": ["전입신고", "전입 신고", "주민등록"],
        "인터넷": ["인터넷", "TV", "티비", "케이블"],
        "공공요금": ["공공요금", "전기", "가스", "수도", "요금"],
        "이삿짐": ["이삿짐", "이사짐", "이삿짐센터", "이사업체", "포장이사", "센터"],
        "청소": ["청소", "정리"],
        "우편물": ["우편물", "우편", "주소변경"],
        "보증금": ["보증금", "월세", "전세금", "반환"]
    }

    detected = []
    has_completion = any(pattern in message for pattern in completed_patterns)

    if has_completion:
        for category, keywords in checklist_keywords.items():
            for kw in keywords:
                if kw in message:
                    detected.append(category)
                    break

    return list(set(detected))

def auto_check_from_message(message: str) -> Dict[str, Any]:
    """메시지에서 완료된 작업을 감지하여 자동 체크"""
    detected_tasks = detect_completed_tasks(message)
    checked_items = []

    for task_keyword in detected_tasks:
        for item in st.session_state.checklist:
            if task_keyword.lower() in item["title"].lower() and not item["completed"]:
                item["completed"] = True
                checked_items.append(item["title"])
                break

    if checked_items:
        message = f"'{', '.join(checked_items)}' 항목을 완료 처리했습니다."
    else:
        message = ""

    return {"checked_items": checked_items, "message": message}


# ============================================
# AI 챗봇 기능
# ============================================

def get_ai_response(question: str) -> str:
    """Gemini AI로 응답 생성"""
    knowledge_base = {
        "전입신고": "전입신고는 이사 후 14일 이내에 하셔야 합니다. 주민센터 방문 또는 정부24 온라인으로 신청 가능합니다. 필요 서류는 신분증과 임대차계약서입니다.",
        "공공요금": "이사 전에 전기, 가스, 수도 요금을 정산하고 해지 신청을 해야 합니다. 한전, 도시가스, 수도사업소에 각각 연락하세요.",
        "인터넷": "인터넷과 TV는 이사 2주 전에 해지 또는 이전 신청을 하는 것이 좋습니다. 위약금 여부를 확인하세요.",
        "보증금": "보증금 반환은 이사 전 임대인과 일정을 조율하세요. 계약 종료일에 맞춰 반환받는 것이 일반적입니다.",
        "청소": "퇴거 청소는 입주 시 상태로 복원하는 것이 원칙입니다. 전문 청소업체를 이용하면 보증금 분쟁을 줄일 수 있습니다."
    }

    # 간단한 키워드 매칭으로 컨텍스트 찾기
    context = ""
    for keyword, info in knowledge_base.items():
        if keyword in question:
            context += f"\n- {info}"

    # 이삿짐센터 관련 질문인지 확인
    movers_keywords = ["이삿짐", "이사짐", "이사센터", "이삿짐센터", "포장이사", "용달", "업체", "리스트", "목록", "추천"]
    is_movers_question = any(kw in question for kw in movers_keywords)

    movers_info = ""
    if is_movers_question:
        region = st.session_state.get("region", "서울 강남구")
        movers_info = get_movers_info_text(region)
        context += f"\n\n[{region} 지역 이삿짐 센터 목록]\n{movers_info}"

    if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 20:
        # API 키가 없으면 기본 응답
        if context:
            return context.strip()
        return "이사 관련 질문에 대해 더 구체적으로 말씀해 주시면 도와드리겠습니다."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # 이삿짐센터 질문인 경우 프롬프트 조정
        if is_movers_question and movers_info:
            prompt = f"""당신은 1인 가구 이사를 도와주는 친절한 AI 어시스턴트 '룸무브'입니다.

사용자가 이삿짐 센터 정보를 요청했습니다. 아래 목록을 보기 좋게 정리해서 안내해주세요.

=== 사용자 질문 ===
{question}

=== 이삿짐 센터 목록 ===
{movers_info}

=== 답변 지침 ===
1. 위 이삿짐 센터 목록을 보기 좋게 정리해서 보여주세요.
2. 각 업체의 이름, 가격, 연락처, 특징을 포함하세요.
3. 친근한 말투로 안내하세요.
4. 예약 시 팁이나 주의사항도 간단히 알려주세요.

답변:"""
        else:
            prompt = f"""당신은 1인 가구 이사를 도와주는 친절한 AI 어시스턴트 '룸무브'입니다.

사용자의 질문에 친절하고 정확하게 답변해주세요.

=== 사용자 질문 ===
{question}

=== 참고 정보 ===
{context if context else '일반적인 이사 관련 질문입니다.'}

=== 답변 지침 ===
1. 친근하고 이해하기 쉬운 말투로 답변하세요.
2. 구체적인 절차나 주의사항이 있다면 포함하세요.
3. 답변은 3-5문장으로 간결하게 작성하세요.

답변:"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if context:
            return context.strip()
        return f"죄송합니다. 응답 생성 중 오류가 발생했습니다."


# ============================================
# D-day 계산
# ============================================

def calculate_dday(move_date: date) -> Dict[str, Any]:
    today = date.today()
    delta = (move_date - today).days

    if delta > 0:
        display = f"D-{delta}"
        message = f"이사까지 {delta}일 남았습니다"
    elif delta == 0:
        display = "D-Day"
        message = "오늘이 이사 날입니다!"
    else:
        display = f"D+{abs(delta)}"
        message = f"이사 후 {abs(delta)}일 지났습니다"

    return {
        "dday": delta,
        "display": display,
        "message": message,
        "move_date": move_date.strftime("%Y년 %m월 %d일")
    }


# ============================================
# 이삿짐 센터 데이터 (CSV에서 로드)
# ============================================

def load_movers_from_csv() -> List[Dict]:
    """CSV 파일에서 이삿짐 센터 데이터 로드"""
    import pandas as pd

    # CSV 파일 경로 (Streamlit Cloud에서는 상대 경로 사용)
    csv_paths = [
        "backend/data/movers.csv",
        "data/movers.csv",
        "movers.csv"
    ]

    for csv_path in csv_paths:
        try:
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                movers = df.to_dict('records')
                return movers
        except:
            continue

    # CSV 로드 실패 시 기본 데이터 반환
    return [
        {"id": 1, "name": "강남 이사 전문", "region": "서울 강남구", "phone": "02-1234-5678", "price": 300000, "description": "강남구 전문 이삿짐 센터"},
        {"id": 2, "name": "서울 빠른 이사", "region": "서울 강남구", "phone": "02-2345-6789", "price": 280000, "description": "빠른 서비스 제공"},
        {"id": 3, "name": "믿음 이삿짐", "region": "서울 강남구", "phone": "02-3456-7890", "price": 320000, "description": "20년 경력의 전문 업체"},
        {"id": 4, "name": "1인 가구 전문", "region": "서울 강남구", "phone": "02-5678-9012", "price": 250000, "description": "1인 가구 특화 서비스"},
        {"id": 5, "name": "서울 이삿짐", "region": "서울 송파구", "phone": "02-6789-0123", "price": 270000, "description": "송파구 지역 전문"},
    ]

def get_movers(region: Optional[str] = None) -> List[Dict]:
    """이삿짐 센터 목록 조회"""
    movers_data = load_movers_from_csv()

    if region:
        return [m for m in movers_data if region in m.get("region", "")]
    return movers_data

def get_movers_info_text(region: Optional[str] = None) -> str:
    """AI 응답용 이삿짐 센터 정보 텍스트 생성"""
    movers = get_movers(region)

    if not movers:
        return "해당 지역의 이삿짐 센터 정보가 없습니다."

    info_lines = []
    for m in movers[:5]:  # 최대 5개까지만 표시
        price = m.get('price', 0)
        price_str = f"{price:,}원" if price else "가격 문의"
        info_lines.append(f"- {m['name']}: {price_str} / 📞 {m.get('phone', '전화번호 없음')} / {m.get('description', '')}")

    return "\n".join(info_lines)


# ============================================
# UI 컴포넌트
# ============================================

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("### 🏠 RoomMove")
        st.caption("1인 가구 이사 준비 도우미")

        st.markdown("---")

        # 이사 날짜 입력
        st.markdown("#### 📅 이사 날짜 입력")
        move_date = st.date_input(
            "",
            value=st.session_state.move_date or date.today(),
            label_visibility="collapsed"
        )
        st.session_state.move_date = move_date

        # D-Day 표시
        if move_date:
            dday_info = calculate_dday(move_date)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem; border-radius: 1rem; text-align: center; margin: 1rem 0;">
                <div style="font-size: 2.5rem; font-weight: bold; color: white;">{dday_info['display']}</div>
                <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">{dday_info['message']}</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin-top: 0.3rem;">
                    이사 예정일: {dday_info['move_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 지역 선택
        st.markdown("#### 📍 지역 선택")
        regions = ["서울 강남구", "서울 서초구", "서울 송파구", "서울 마포구", "서울 영등포구"]
        region = st.selectbox("", regions, index=regions.index(st.session_state.region) if st.session_state.region in regions else 0, label_visibility="collapsed")
        st.session_state.region = region

        # 이삿짐 업체 정보
        with st.expander("🚚 이삿짐 업체 정보"):
            movers = get_movers(region)
            for mover in movers:
                st.markdown(f"""
                **{mover['name']}**
                ⭐ {mover['rating']} | {mover['price_range']}
                📞 {mover['phone']}
                """)
                st.markdown("---")


def render_checklist_panel():
    """체크리스트 패널 렌더링"""
    st.markdown("#### ✅ 이사 체크리스트")

    checklist = get_checklist()

    for item in checklist:
        col1, col2 = st.columns([0.08, 0.92])

        with col1:
            checked = st.checkbox(
                "",
                value=item["completed"],
                key=f"check_{item['id']}",
                label_visibility="collapsed"
            )

            if checked != item["completed"]:
                update_checklist_item(item["id"], checked)
                st.rerun()

        with col2:
            if checked:
                st.markdown(f'<s>{item["title"]}</s>', unsafe_allow_html=True)
                if item.get("description"):
                    st.caption(f"~~{item['description']}~~")
            else:
                st.markdown(f'**{item["title"]}**')
                if item.get("description"):
                    st.caption(item["description"])

        st.markdown('<hr style="margin: 0.3rem 0; border: none; border-top: 1px solid #e0e0e0;">', unsafe_allow_html=True)

    # 진행률
    completed_count = sum(1 for item in checklist if item["completed"])
    total_count = len(checklist)
    progress = completed_count / total_count if total_count > 0 else 0

    st.progress(progress)
    st.caption(f"완료: {completed_count}/{total_count} ({int(progress * 100)}%)")


def render_chat():
    """채팅 UI 렌더링"""
    # 메신저 스타일 CSS
    st.markdown("""
    <style>
    .message-row { display: flex; margin: 0.5rem 0; }
    .message-row.user { justify-content: flex-end; }
    .message-row.assistant { justify-content: flex-start; }
    .message-bubble {
        max-width: 70%;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        word-wrap: break-word;
    }
    .message-bubble.user {
        background-color: #667eea;
        color: white;
        border-bottom-right-radius: 0.25rem;
    }
    .message-bubble.assistant {
        background-color: #e9ecef;
        color: #212529;
        border-bottom-left-radius: 0.25rem;
    }
    .message-bubble p { margin: 0; line-height: 1.5; }
    </style>
    """, unsafe_allow_html=True)

    # 환영 메시지
    if len(st.session_state.chat_messages) == 0:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "안녕하세요! 이사 준비에 대해 궁금한 점을 물어보세요. 도와드리겠습니다."
        })

    # 대화 이력
    for message in st.session_state.chat_messages:
        role = message["role"]
        content = message["content"]
        st.markdown(f"""
        <div class="message-row {role}">
            <div class="message-bubble {role}">
                <p>{content}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 입력
    user_input = st.chat_input("메시지를 입력하세요...")

    # 빠른 질문 처리
    quick_question = st.session_state.get("quick_question")
    if quick_question:
        st.session_state.quick_question = None
        user_input = quick_question

    if user_input:
        # 사용자 메시지 추가
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })

        # 자동 체크
        auto_check_result = auto_check_from_message(user_input)

        # AI 응답
        answer = get_ai_response(user_input)

        # 자동 체크 메시지가 있으면 별도 말풍선
        if auto_check_result["checked_items"]:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"✅ {auto_check_result['message']}"
            })

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    # 초기화 버튼
    if len(st.session_state.chat_messages) > 1:
        if st.button("🗑️ 초기화", key="reset_chat"):
            st.session_state.chat_messages = []
            st.rerun()


# ============================================
# 메인 앱
# ============================================

def main():
    st.set_page_config(
        page_title="RoomMove - AI 이사 도우미",
        page_icon="🏠",
        layout="wide"
    )

    # 세션 상태 초기화
    init_session_state()

    # 사이드바
    render_sidebar()

    # 메인 레이아웃
    col_main, col_right = st.columns([3, 1])

    with col_main:
        st.title("💬 AI 이사 도우미")

        # 빠른 질문 버튼
        st.markdown("##### 💡 빠른 질문")
        q1, q2, q3, q4 = st.columns(4)

        with q1:
            if st.button("📋 전입신고", use_container_width=True):
                st.session_state.quick_question = "전입신고는 어떻게 해?"
                st.rerun()
        with q2:
            if st.button("💰 공공요금", use_container_width=True):
                st.session_state.quick_question = "공공요금 정산은 어떻게 해?"
                st.rerun()
        with q3:
            if st.button("🚚 이삿짐", use_container_width=True):
                st.session_state.quick_question = "이삿짐 센터는 언제 예약해야 해?"
                st.rerun()
        with q4:
            if st.button("🌐 인터넷", use_container_width=True):
                st.session_state.quick_question = "인터넷 해지는 어떻게 해?"
                st.rerun()

        st.markdown("---")

        # 채팅
        render_chat()

    with col_right:
        render_checklist_panel()


if __name__ == "__main__":
    main()
