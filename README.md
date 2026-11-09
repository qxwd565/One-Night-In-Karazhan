# HSdeck One Night in Karazhan 카드 API

기존 원본 카드 57개를 한국 날짜 기준 최초 스펙과 이후 변경값으로 관리합니다. 각 `data/<ID>.json`이 canonical 데이터이며, `metadata/<ID>.json`에는 변경 전 원본과 출처·확신도·현재 전용 정보를 보존합니다.

`cards.json`, `render.json`, `history.json`은 기존 schema 1 호환 출력입니다. `cards-date.json`, `render-date.json`, `history-date.json`은 필드 부재·명시적 제거를 보존하는 정밀 출력입니다. `data/history.json`은 보존된 과거 집계 자료이며 canonical 입력이 아닙니다.

후속 주간 카드 39개의 날짜는 확인된 사용 가능 상한이고, 더 이른 무작위 생성의 최초 실사용일은 미확정입니다. 확신도와 기존 fallback을 함께 보존합니다. 자세한 결과는 [검증 보고서](AUDIT.md), 구조와 재현 명령은 [스키마 문서](docs/date-schema.md)를 참조하세요.

`art/`, `golden/`, `frame/`은 원본 리소스와 연결을 유지합니다. 날짜별 과거 원화·황금 효과를 보장하지 않습니다. canonical 데이터를 수정한 뒤 `python tools/build-api.py`를 실행하면 양쪽 API가 갱신됩니다.
