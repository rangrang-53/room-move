"""초기 데이터 로드 스크립트"""
import json
import csv
import sys
from pathlib import Path

# backend 폴더를 Python 경로에 추가
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.db.database import SessionLocal, init_db
from app.models.checklist import ChecklistItem
from app.models.movers import Mover


def load_checklist_data():
    """체크리스트 초기 데이터 로드"""
    db = SessionLocal()
    try:
        # 기존 데이터 확인
        existing_count = db.query(ChecklistItem).count()
        if existing_count > 0:
            print(f"체크리스트 데이터가 이미 존재합니다 ({existing_count}개)")
            return

        # JSON 파일에서 데이터 읽기
        with open('data/checklist.json', 'r', encoding='utf-8') as f:
            checklist_data = json.load(f)

        # 데이터베이스에 삽입
        for item in checklist_data:
            checklist_item = ChecklistItem(
                title=item['title'],
                description=item['description'],
                completed=item['completed']
            )
            db.add(checklist_item)

        db.commit()
        print(f"체크리스트 데이터 {len(checklist_data)}개 로드 완료")

    except Exception as e:
        print(f"체크리스트 데이터 로드 실패: {e}")
        db.rollback()
    finally:
        db.close()


def load_movers_data():
    """이사업체 초기 데이터 로드"""
    db = SessionLocal()
    try:
        # 기존 데이터 확인
        existing_count = db.query(Mover).count()
        if existing_count > 0:
            print(f"이사업체 데이터가 이미 존재합니다 ({existing_count}개)")
            return

        # CSV 파일에서 데이터 읽기
        with open('data/movers.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            movers_data = list(reader)

        # 데이터베이스에 삽입
        for item in movers_data:
            mover = Mover(
                name=item['name'],
                region=item['region'],
                phone=item['phone'],
                price=int(item['price']),
                description=item['description']
            )
            db.add(mover)

        db.commit()
        print(f"이사업체 데이터 {len(movers_data)}개 로드 완료")

    except Exception as e:
        print(f"이사업체 데이터 로드 실패: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("데이터베이스 초기화 중...")
    init_db()

    print("\n초기 데이터 로드 시작...")
    load_checklist_data()
    load_movers_data()
    print("\n초기 데이터 로드 완료!")
