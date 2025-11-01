from datetime import date, datetime
from ..schemas.dday import DdayRequest, DdayResponse


class DdayService:
    """D-day 계산 서비스"""

    @staticmethod
    def calculate_dday(request: DdayRequest) -> DdayResponse:
        """D-day 계산"""
        current_date = date.today()
        move_date = request.move_date

        # D-day 계산 (이사 날짜 - 현재 날짜)
        delta = (move_date - current_date).days

        # 메시지 생성
        if delta > 0:
            message = f"이사까지 {delta}일 남았습니다"
        elif delta == 0:
            message = "오늘이 이사 날입니다!"
        else:
            message = f"이사 날짜가 {abs(delta)}일 지났습니다"

        return DdayResponse(
            d_day=delta,
            move_date=move_date.isoformat(),
            current_date=current_date.isoformat(),
            message=message
        )


dday_service = DdayService()
