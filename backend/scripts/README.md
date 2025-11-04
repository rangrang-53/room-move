# Scripts

백엔드 유틸리티 스크립트 모음

## 사용 가능한 스크립트

### init_data.py
초기 데이터를 데이터베이스에 로드하는 스크립트

**사용법:**
```bash
cd backend
python scripts/init_data.py
```

**기능:**
- 체크리스트 초기 데이터 로드 (data/checklist.json)
- 이사업체 초기 데이터 로드 (data/movers.csv)
- 기존 데이터가 있으면 건너뜀
