# checkspeed — 스피드체크

브라우저에서 바로 인터넷 속도(핑·지터·다운로드·업로드)를 재는 단일 페이지 웹앱.
측정 서버는 Cloudflare 공개 엔드포인트(`speed.cloudflare.com`)를 사용하고,
빌드 도구나 의존성 없이 `index.html` 파일 하나로 동작한다.

## 파일 구성

- `index.html` — 전부. HTML + CSS + JS가 한 파일에 인라인으로 들어 있다.
  (게이지 SVG, 실시간 그래프 canvas, 측정 로직, 셀룰러 차단 로직)

## 배포

GitHub Pages(main 브랜치 루트)로 서비스된다 — https://stepersjmj-hash.github.io/checkspeed/
`main`에 푸시하면 자동 배포. 별도 빌드 단계 없음.

## 측정 로직 요약 (index.html 하단 `<script>`)

- `measurePing(samples, signal)` — `__down?bytes=0` 왕복 시간. 최솟값을 핑,
  연속 샘플 차이의 평균을 지터로 쓴다. 워밍업 1회로 커넥션 수립 비용 제외.
- `measureDownload(durationMs, onProgress, extSignal)` — 50MB 요청 × 4 병렬 스트림,
  기본 10초. 스트림을 읽으면서 0.2초 구간마다 순간 속도를 보고한다.
- `measureUpload(durationMs, onProgress, extSignal)` — 8MB 랜덤 Blob을 XHR로 × 3 병렬,
  기본 8초. `xhr.upload.onprogress`로 진행률을 잰다.
- `runTest()` — 핑 → 다운로드 → 업로드 순서로 돌리고 등급 문구를 표시.
- `stopTest()` — 측정 중 버튼이 "중지"로 바뀌며, `runCtl`(AbortController)을 abort해
  진행 중인 fetch/XHR를 즉시 끊는다. 각 단계 뒤 `throwIfCancelled()`로 흐름을 빠져나가고,
  중지 시점까지 나온 값은 카드에 그대로 남긴다.

## 함정 / 주의

- **데이터 소모** — 한 번 측정에 수백 MB가 나갈 수 있다. 그래서
  `navigator.connection.type === "cellular"`이면 시작 버튼을 비활성화하고 경고를 띄운다.
  연결 종류를 알 수 없는 브라우저(iOS Safari 등)에는 상시 안내 문구를 대신 보여준다.
- 새 측정 시작 시 `graphData`만 비우면 캔버스에 이전 그래프가 남는다 —
  `drawGraph()`를 함께 호출해야 지워진다.
- **지터 계산 순서** — `times` 배열을 정렬한 뒤 연속 차이를 더하면 중간 항이 전부 상쇄되어
  `(최댓값-최솟값)/(n-1)`이 되어버린다(과거 버그). 지터는 반드시 측정 순서 그대로 계산하고,
  핑 최솟값은 `Math.min`으로 따로 구한다.
- 취소 경로에서 `measureDownload`/`measureUpload`는 예외를 던지지 않고 부분 결과를
  반환한다. 중지 판정은 반드시 `runTest` 쪽 `throwIfCancelled()`가 한다.
- 로컬에서 `file://`로 열어도 Cloudflare 엔드포인트는 CORS 허용이라 그대로 테스트된다.

## 관례

- 코드는 한 파일 유지 — 프레임워크·번들러 도입하지 않는다. UI 문구는 한국어.
- 커밋 메시지는 한국어 한 줄 요약 (예: `측정 중 중지 버튼 추가`).
