# 2차 검증 보고서

최신 상태(2026-10-30): 사용자 직접 Formspree 테스트 발송·스팸함 수신 확인 완료. Hero·프로필 이니셜 `JL` 통일 및 README 체크박스 11개 삭제. 이번 실행 결과는 마지막 최신 검증 절을 따릅니다. **아래 1~10절의 미설정·BLOCKED·대기 기록은 각 검증 당시 이력**이며 현재 메일/Pages 미완료를 뜻하지 않습니다. 디자인 사용자 최종 승인 기록은 없습니다.

검증일: **2026-10-28 (Asia/Seoul)**. 사용자 지정 2차 프롬프트를 읽고 기존 워크스페이스를 수정했습니다. 새 프로젝트 생성, 원격 push, 공개 배포, 외부 계정 생성, 실제 메일 발송은 수행하지 않았습니다.

## 1. 완료 상태를 구분한 판정

| 상태 | 판정 | 실제 근거 |
| --- | --- | --- |
| LOCAL_IMPLEMENTATION | PASS | 필수 및 보너스 4개 코드, 실제 프로필 그래픽, 개인화 25항목, 학습 README 구현 |
| LOCAL_VERIFIED | PASS | 정적 검사·Chrome 109 PASS·로컬 릴리스 검사·소스 해시 일치 |
| EMAIL_LIVE_VERIFIED | BLOCKED | formId 없음, enabled=false, 실제 발송/수신 미실행 |
| GITHUB_PAGES_VERIFIED | BLOCKED | 실제 Pages URL 없음, 배포 승인 전 |
| SUBMISSION_READY | BLOCKED | 실제 목표 저장소/Pages URL·실전 이메일 증거·디자인/공개 승인 필요 |

디자인은 Blueberry Signal 제안이며 사용자 최종 시각 승인 상태가 아닙니다. 위 PASS는 로컬 구현/검증 범위입니다. 과제 전체 제출 완료라고 선언하지 않습니다.

## 2. 시작 시 소스·Git 확인과 1차와의 차이

작업 전에 index.html, style.css, config.js, main.js, DECISIONS, README, TEST_REPORT, 세 검사 파일, browser-results.json 및 images/를 확인했습니다. 앱은 1차 개인화 TBD 상태였고 프로필 실파일은 없었습니다. 기존 Chrome 결과는 57 PASS였습니다.

Git 상태는 1차 문서와 달랐습니다. 현재 `.git`이 존재하며 `main`에 커밋은 없고, 기존 16개 파일이 스테이징되어 있습니다. `git remote -v`는 빈 결과, `gh`는 미설치였습니다. 수정 후 AM은 기존 스테이징 이후 작업 파일 변경, 새 문서/이미지는 untracked입니다. 기존 index를 임의로 add/reset/commit하지 않았습니다.

실제 공개 API 목록은 이전 7개에서 **8개**가 되었고 `my-portfolio`가 포함됩니다. 그러나 로컬 origin이 없어 같은 프로젝트라고 확정하지 않았습니다. 목표 `gareal2117/codyssey-b1-1-personal-portfolio`의 공개 조회는 **404**였습니다. 비공개 충돌·소유자 인증은 확인하지 못했습니다. rename/remote 변경/원격 생성/force push는 수행하지 않았습니다.

## 3. 변경 파일별 핵심

| 파일 | 변경 내용 |
| --- | --- |
| index.html | 승인된 Hero/About/Skills/Footer, 완전한 no-JS 대체문구, 실제 img, Featured/All/필터, 전송 상태·개인정보 고지 |
| css/style.css | 네이비·블루·스카이블루, Hero 추상 그래픽·비대칭 형태·Featured 강조, 두 테마, 프로필 비율 보정 |
| js/config.js | 기존 25개 키/ID 보존, VERIFIED 값, Featured·README 검증 캐시·Formspree 공개 설정·별도 release 상태 |
| js/main.js | 안전한 동적 HTML, Featured/All/filter, 타이핑, 시스템 테마, 실제 fetch 전송 상태·예외·중복 잠금 |
| images/profile-monogram.svg | 직접 작성한 실제 프로필/파비콘 그래픽; 얼굴 사진/외부 저작물 아님 |
| DECISIONS.md | 25개 항목의 확정값·적용 위치·상태, 의도적 빈값·공개 범위·외부 보류 |
| README.md | 0~18의 19절 자습 교재로 전면 재작성, 실제 함수·선택자·실습·복습 해설 |
| docs/REQUIREMENTS_MATRIX.md | 구현 전 추적표를 작성하고 A~J 41개 행으로 실제 증거 갱신 |
| docs/EMAIL_SETUP.md | 계정·수신설정·공개 ID·승인된 실제 1건 발송/수신 확인 절차 |
| tests/static_checks.py | TBD 강제 제거, 25개 승인 계약/문서/정적 대체문구, SVG·비밀키 형태 검사 |
| tests/browser_checks.py | 기존 목적 보존 + 보너스·메일 mock·이미지·색상·30초 유지 검사, 목표 하위 경로, 소스 해시 |
| tests/release_check.py | --local과 전체 제출 검사 분리, 오래된 결과/실제 외부 조건 차단 |
| tests/verify_readmes.py | 필요 시 읽기 전용 README·기본 브랜치·경로 확인, 매 방문 호출 없음 |
| docs/history/phase1/ | 과거 README/DECISIONS/TEST_REPORT/57개 결과/캡처 원본 보존 |
| docs/browser-results.json, screenshots/ | 최종 실제 실행이 생성한 새 결과와 실제 API 화면 3종 |

## 4. 실행한 검사와 실제 결과

환경: macOS 설치 **Chrome/146.0.7680.165**, 임시 프로필, Python 표준 HTTP 서버, DevTools 프로토콜. npm·외부 Python 패키지 없이 실행했습니다. 검증 경로는 `/codyssey-b1-1-personal-portfolio/`입니다. 모든 메일 테스트에서 Formspree 호스트는 네트워크 차단하고 fetch 대역으로만 응답했습니다.

| 명령/검증 | 결과 | 범위 |
| --- | --- | --- |
| python3 tests/static_checks.py | PASS / exit 0 | 구조·경로·금지 요소·25개 계약·SVG·정적 대체문구 |
| python3 tests/browser_checks.py | **109 PASS / 0 FAIL**, exit 0 | [새 실행 JSON](./docs/browser-results.json) |
| python3 tests/release_check.py --local | PASS / exit 0 | 25개 VERIFIED·검사 소스 해시·캡처·문서 |
| python3 tests/release_check.py | BLOCKED / exit 2 | 실제 메일·저장소·Pages·디자인/공개 승인 |
| python3 tests/verify_readmes.py | PASS / exit 0 | README 5개 200, 3개 404, 목표 저장소404; [기록](./docs/readme-verification.json) |
| 실제 GitHub API 페이지 | PASS | 공개 저장소 8개, 실제 Featured 3개 |
| 메일 모의 전송 | PASS | 성공/422/429/500/네트워크/서비스 오류/JSON/timeout/중복/설정/honeypot |
| 메일 실전 발송·수신 | BLOCKED | 미실행 |
| 실제 Pages 배포 | BLOCKED | 미실행 |

텍스트 대비의 검사 범위는 기본/보조/오류/성공/강조 글자 대 배경/카드/연한 배경과 주 버튼 글자/배경입니다. 최소값은 **light 5.53:1, dark 7.51:1**로 일반 텍스트 4.5:1 이상입니다. 모든 그라데이션 장식·보조기기 환경에 대한 인증이 아닙니다.

375/768/1024/1440px에서 두 테마의 가로 넘침이 없었고 메뉴·Grid 표시를 확인했습니다. 프로필은 naturalWidth=480 및 실제 표시 가로/세로 비율을 검사했습니다. 30초 렌더 유지 후 타이핑이 재시작하지 않고 카드/폼이 유지됨을 확인했습니다. 수 시간 내구 시험은 아닙니다. 미처리 JS 예외와 console.error는 0건입니다.

API의 15초 초과는 AbortError 분기와 타이머 소스 검토로 확인했으며 실제로 15초 네트워크 지연을 기다리지는 않았습니다. 메일 타이머는 테스트에서 timeoutMs를 40ms로 줄이고 signal의 실제 abort를 확인했습니다. 실제 외부 서비스에 오류를 유발하지 않았습니다.

### 과거 57개와 신규 검사 비교

- 과거 **2026-10-28 1차 57 PASS**: [보존 JSON](./docs/history/phase1/browser-results.json), [보존 보고서](./docs/history/phase1/TEST_REPORT.md). 현재 결과로 재사용하지 않았습니다.
- 핵심 메뉴/스크롤 경계/API 상태·예외/폼 검증/저장소 예외/Observer/no-JS 목적을 유지했습니다.
- “25개 모두 TBD”는 “25개 승인 ID·값·실제 UI 일치”로 변경했습니다.
- 폼의 정상 입력 안내는 실제 전송 success가 아니라 연동 전 미전송 상태를 확인하도록 바꿨습니다.
- 카드 h3→h4와 정렬 변경에 맞춰 선택자/대상 식별을 수정했습니다. 악성 fixture를 첫 카드로 가정하지 않습니다.
- Observer는 카드가 실제로 화면에 들어오는 조건을 재현합니다. threshold를 낮춰 통과시키지 않았습니다.
- 목표 하위 경로 및 저장소 조회를 codyssey-b1-1-personal-portfolio로 변경했습니다.
- 새 검사는 계약/프로필/필터/Featured/README/타이핑/시스템 테마/메일/대비·양쪽 테마/30초 유지입니다. 최종 집계는 109개이며 과거보다 52개 늘었습니다.

## 5. 개인화와 보너스 판정

25개 기존 키·고유 ID는 유지되었습니다. 사용자 지정 프롬프트의 CONFIRMED 값을 적용한 뒤 APPLIED 상태로 시험하고, 새 검사 통과 후 VERIFIED로 갱신하여 다시 최종 실행했습니다. [승인 계약](./docs/personalization-contract.json), config.js, DECISIONS의 ID/값/상태 및 정적 HTML 문구를 대조했습니다.

`personalContent`와 `footerPersonalMessage`는 의도적인 빈 문자열입니다. 별도 경력이나 SNS를 만들지 않았습니다. 공개 이메일/전화번호는 없고 Footer의 GitHub 프로필 링크는 하나입니다. 필수 Contact 구조·프로필 img·Skills는 삭제하지 않았습니다. 디자인 관련 VERIFIED는 기술 적용 검증이며 `designApproved=false`입니다.

| 보너스 | 구현/로컬 시험 | 실전 상태 |
| --- | --- | --- |
| 언어 필터 | PASS: 동적 옵션, filter, 건수/aria, 0건, null언어, API 추가 요청 없음, Featured 보존 | 로컬 실제 API 및 fixture 확인 |
| Hero 타이핑 | PASS: 실제 글자 변화, 1회, 완전한 정적 문구, sr-only, motion/배경 탭 처리 | 로컬 실제 Chrome 확인 |
| Formspree 이메일 | PASS: 순수 fetch 코드 및 mock 상태/예외 | **BLOCKED: 실제 계정/ID/발송/수신 전** |
| 시스템 테마 | PASS: 시스템 초기값, 수동·저장 우선, change, 저장 차단 | 로컬 실제 Chrome 에뮬레이션 확인 |

## 6. 요구사항 표와 README 교육 깊이

[A~J 추적표](./docs/REQUIREMENTS_MATRIX.md) 41행의 결과는 **37 PASS / 1 PARTIAL / 0 FAIL / 3 BLOCKED**입니다. 브라우저 109개 집계와 다른 단위입니다. PARTIAL은 Live Server 확장 UI 자체의 미조작, BLOCKED는 이메일 실전·목표 원격·Pages 제출입니다. 실제 스크린리더·다른 OS/브라우저·실기기 검증도 완료 주장 범위에서 제외했습니다.

README는 0~18의 19절로 신규 집필했습니다. 3~11절마다 정의·필요성·현행 파일/함수·예제/단계·예외·확인 방법을 제공했습니다. HTML 의미/DOM, CSS cascade/Flex/Grid, defer/스코프/안전한 HTML, 세 상태 흐름, 비동기/API/README 캐시, 폼의 접수와 실제 수신을 구분합니다. 11개 최소 실습에는 수정 위치·사전 상태·실행·예상 결과·원복을 적고, 설명형 질문 15개에 해설을 붙였습니다.

실제 함수/선택자 목록과 README를 다시 대조했습니다. 예제는 현행 코드 발췌인지 독립 학습 예제인지 표시했으며, 60/300/0.2/768/1024/15초 및 100/254/5000 기준을 소스와 확인했습니다. 사용자가 느낀 점이나 이미 이해했다는 주장은 쓰지 않았습니다.

## 7. 최신 스크린샷과 실제 실패 수정

- [desktop.png](./docs/screenshots/desktop.png): 1440×900 뷰포트의 전체 페이지.
- [mobile.png](./docs/screenshots/mobile.png): 375×900 뷰포트의 전체 페이지.
- [dark.png](./docs/screenshots/dark.png): 1440×900 다크 전체 페이지.

PNG 폭은 스크롤바를 제외한 콘텐츠 폭일 수 있습니다. 실제 API 응답을 표시한 페이지를 모의 응답 주입 전에 캡처했습니다. 1차 캡처는 history/phase1/screenshots에 보존했습니다. 최신 화면도 사용자 최종 디자인 승인이나 실제 배포 화면이라는 뜻은 아닙니다.

| 이번 실제 문제 | 원인 | 해결 및 결과 |
| --- | --- | --- |
| README 조회 DNS 실패 | 샌드박스 외부 연결 제한 | 읽기 전용 조회 권한으로 실제 경로/브랜치 확인 |
| 첫 2차 시험 106 PASS/2 FAIL | 정렬된 첫 카드를 악성 fixture라고 가정, 새 레이아웃에서 Observer 카드가 화면 밖 | 대상 텍스트로 카드 식별, 카드 중앙 이동 후 검사 |
| 프로필 그래픽 잘림 | 고정 HTML 높이와 CSS 축소 너비 | height:auto 추가, 표시 비율 검사와 최신 캡처 |
| 다음 실행 108 PASS/0 FAIL | 위 수정 검증 | 이후 25개 상태 갱신, 비율/no-JS/30초 시험 보강 후 최종 109 PASS |

1차 실제 문제는 WebSocket 응답 문구 비교와 키보드 자동화 focus/Enter 이벤트였고 과거 보고서에 보존되어 있습니다. 이번 앱의 장애인 것처럼 새로 꾸며 기록하지 않았습니다.

## 8. 별도 두 번째 검토와 남은 조치

구현·검증 후 별도 순서로 (1) 원문 A~J와 소스/테스트, (2) 승인된 25개 값/README 교육 깊이/공개 범위를 다시 대조했습니다. 다른 사람이나 서브에이전트의 승인으로 표현하지 않습니다.

- 앱의 정적 HTML/동적 화면에 `[...미정]` 문구 없음. 역사 문서의 과거 TBD는 의도적으로 보존.
- 앱 파일에 공개 이메일 문자열·토큰 형태(ghp/github_pat/sk-proj/AKIA) 없음. 비밀 저장소 전체를 탐색하거나 키를 출력하지 않음.
- 인라인 onclick/style, var, 외부 UI 프레임워크 없음. 동적 HTML은 내부 골격/숫자만, API/사용자 값은 안전한 DOM 처리.
- 정적 대체 문구·프로필 alt·Footer·문서 제목이 승인 값과 일치. SVG에는 script/foreignObject/외부 href가 없음.
- 사이트의 기술 적용 상태와 디자인 최종 승인, mock 전송과 실제 수신, 하위 경로 시험과 실제 Pages를 구분.

사용자에게 남은 최소 조치:

1. 최신 캡처를 보고 디자인을 검토합니다.
2. Formspree 계정·수신 주소를 서비스 내에서 설정하고 공개 폼 ID만 제공합니다. 실제 발송 활성화와 테스트 한 건을 승인한 뒤 수신함을 확인합니다. [상세 절차](./docs/EMAIL_SETUP.md).
3. 공개 목록의 my-portfolio가 이 프로젝트 저장소인지 확인하고 목표 이름으로 rename/연결할 대상을 확정합니다. 인증된 환경과 별도 공개 push·Pages 승인이 필요합니다.
4. 승인 후 실행할 커밋/원격/Pages/실제 URL/모바일·다크·폼 재검증은 README 14절 배포 절차와 18절 제출 정보를 따릅니다.

최종 로컬 파일은 검토 가능한 상태이며 위 외부 조치가 남아 있는 동안 **전체 과제 완료/제출 준비 완료는 BLOCKED**입니다.

## 9. 코드 게시 후속 승인과 사전 점검

사용자가 코드 커밋·일반 push·기존 포트폴리오 재사용 및 이름 변경을 승인했습니다. Pages 배포는 독립 코드 검토 이후로 명시적으로 보류했습니다. 앞 절의 origin 없음·gh 미설치·목표404는 2차 개발 당시 이력입니다.

- 인증 계정 gareal2117 확인. 기존 my-portfolio는 원격 참조와 커밋이 없는 빈 저장소였으며 목표 이름으로 변경해 재사용했습니다.
- origin: https://github.com/gareal2117/codyssey-b1-1-personal-portfolio.git. GitHub API에서 has_pages=false 확인. 다른 과제 저장소 변경 없음.
- .gitignore에 로컬 도구 설정·인증 파일·키 파일 제외를 보강하고 git check-ignore로 확인했습니다.
- 전체 커밋 후보에서 비밀키/토큰 형태·개인 이메일·로컬 사용자 경로를 점검했습니다. 이메일 형태는 테스트용 qa@example.test뿐입니다.
- Git 작성자에는 계정별 GitHub noreply 주소를 사용합니다. 인증값은 소스·README·커밋에 넣지 않습니다.
- 승인 및 원격 URL 메타데이터를 반영하고 새 Chrome 결과·캡처·소스 해시와 로컬 릴리스 검사를 확인합니다.
- 요구사항 표 J3는 실제 저장소 URL 확인으로 PASS입니다. 현재 표는 38 PASS / 1 PARTIAL / 0 FAIL / 2 BLOCKED이며, 앞 절의 37/1/0/3은 2차 개발 완료 시점 기록입니다.

## 10. Formspree 연결과 Header 로고 수정

- `email.formId=mdeezyjq`, `email.enabled=true` 적용. 승인된 공개 ID만 추가했고 개인 이메일·비밀키는 추가하지 않았습니다.
- Header의 config/정적 HTML을 `JL.` → `JL`로 변경했습니다. CSS 가상 요소에 마침표가 없음을 확인했고 CSS, Hero, 프로필 SVG, main.js 전송 로직은 수정하지 않았습니다.
- 활성화 상태에 맞춰 Contact 소개·개인정보 고지·정적 버튼 문구와 개인화 계약을 동기화했습니다. README 강의노트는 유지하고 관련 상태 안내만 수정했습니다.
- 정적 검사, 로컬 릴리스 검사, diff 공백 검사 통과. Chrome **114 PASS / 0 FAIL**: 기존 109개 목적을 유지하고 활성 설정·데스크톱/모바일 Header·Home 이동·정확한 endpoint의 5개 검사를 추가했습니다.
- 필수값/공백/이메일/길이/필드 오류, 전송 중 중복 잠금, 응답 대기, 성공 후 초기화, HTTP/서비스/네트워크/타임아웃 오류를 모의 응답으로 검증했습니다. Formspree 호스트를 차단하고 fetch를 대체하여 실제 POST는 수행하지 않았습니다.
- `emailLiveVerified=false` 유지. 사용자가 배포된 사이트에서 직접 발송하고 수신함·스팸함 도착을 확인해야 합니다.
- 기존 Pages 설정은 main / (root), build_type=legacy, status=built로 읽기 확인했습니다. 설정을 변경하지 않으며 이번 push의 자동 재배포와 실제 새 파일 반영은 push 후 별도 확인 대상입니다.

## 11. 2026-10-30 최종 수정 및 현재 검증

- 시작: `main`, 로컬 변경 없음. 원격 main은 `7e5dfe3`이었고 실제 Pages HTML은 HTTP 200으로 응답했습니다.
- README 마지막 체크박스 11개만 삭제했습니다. HTML/CSS/JS 강의노트와 과제 요구사항 표·과거 보고서·증거는 보존했습니다.
- 실제 발견·수정: Hero·프로필 SVG의 잔여 `JL.` → `JL`, 현재 완료 상태와 충돌하던 설정·문서·정적 검사 조건을 갱신했습니다. CSS·main.js는 변경하지 않았고 추가 앱 동작 오류는 발견하지 못했습니다.
- Formspree: `mdeezyjq`, enabled=true. **실제 테스트 메시지 발송과 스팸함 수신은 사용자가 직접 확인**했다고 2026-10-30 보고했습니다. `emailLiveVerified=true`. 수신 주소와 메시지 원문은 기록하지 않으며 이번 작업에서 실제 발송은 하지 않았습니다.
- Pages: 실제 URL 및 pagesApproved=true 반영. 최신 수정본 동작 검증 전에는 pagesVerified=false를 유지하며 후속 배포 검증 성공 시에만 갱신합니다. 디자인 최종 승인 기록은 없어 designApproved=false입니다.
- 정적 검사 PASS. Chrome 146.0.7680.165 로컬 **116 PASS / 0 FAIL**. 실제 GitHub API는 공개 저장소 8개를 로드했습니다. 375/768/1024/1440px 양 테마 overflow, 모바일 메뉴/키보드, 필터, 타이핑, 이미지 로드, 폼 입력·오류·중복·timeout, 콘솔/미처리 예외 검사를 통과했습니다. Formspree는 네트워크 차단 및 mock만 사용했습니다.
- 로컬 릴리스 PASS(exit 0). 전체 릴리스는 최신 Pages 검증 및 디자인 최종 승인 전 BLOCKED(exit 2)로 정상 차단됩니다. 우회하지 않았습니다.
- `docs/screenshots/desktop.png`, `dark.png`, `mobile.png`, `mobile-dark.png`, `projects.png`, `contact.png` 6종을 실제 API 로딩 후 **로컬**에서 촬영하고 열어 확인했습니다. 이미지 손상·가로 잘림·깨진 프로필 없음. Contact 입력란은 비어 있습니다. Projects 캡처는 섹션 상단이며 전체 카드는 전체 페이지 캡처에 포함됩니다.
- 샌드박스 내부 DNS와 로컬 서버 바인딩 제한은 승인된 외부 실행으로 해결했습니다. 앱 오류가 아닙니다. 실제 스크린리더·다른 브라우저/실기기 및 VS Code 확장 UI 조작은 검증 범위 밖입니다.

### 원격 게시 시도 및 실제 Pages 재점검

- 로컬 일반 커밋 `09ee4b2` 생성 성공. `git push origin main`은 `could not read Username for https://github.com`으로 실패했습니다. GitHub 연결 도구의 저장소 메타데이터는 push=true였으나 실제 blob 쓰기는 **403 Resource not accessible by integration**으로 거부되었습니다. 원격 branch/ref는 변경하지 않았고 강제 push·이력 초기화도 수행하지 않았습니다.
- 실제 기존 Pages를 `BROWSER_BASE_URL=https://gareal2117.github.io`로 기존 Chrome 검사에 연결하여 재점검했습니다. **115 PASS / 2 FAIL**(exit 1). 실패는 Hero에 남은 `JL.` 및 배포 HTML/CSS/JS/SVG 해시와 새 로컬 소스의 불일치입니다. 이는 수정본이 아직 push되지 않았다는 실제 증거이며 테스트를 무조건 성공시키지 않았습니다. 메뉴·테마·실제 API·필터·타이핑·빈 폼 및 mock 전송·키보드·양 테마 4개 너비·이미지·콘솔 검사는 통과했습니다.
- [현재 배포 검사 JSON](./docs/pages-browser-results.json)의 comparisonLocalSourceHashes는 비교 대상 로컬 해시이며 배포된 해시라고 주장하지 않습니다. 과거 배포 캡처는 `/tmp`에 분리했고 README에는 최신 로컬 캡처 6종만 연결했습니다.
- 최종 설정: pagesUrl은 실제 URL, pagesApproved=true, emailLiveVerified=true, **pagesVerified=false**, **designApproved=false**. 현재 사이트 접속은 성공하지만 이번 변경의 최신 배포 검증은 미완료입니다.
- 남은 조치: 저장소의 Git HTTPS 인증을 복구한 뒤 main 일반 push, 자동 Pages 배포 완료 대기, 배포 자산 일치와 Chrome 검사를 재실행합니다. 성공한 경우에만 pagesVerified=true로 변경하고 소스 변경에 따른 로컬 재검증·증거 커밋을 수행합니다. 디자인 사용자 최종 승인도 별도로 필요합니다.
- 재현: `BROWSER_BASE_URL=https://gareal2117.github.io SCREENSHOT_PREFIX=/tmp/portfolio-published- BROWSER_REPORT=/tmp/portfolio-published-results.json python3 tests/browser_checks.py`. 기존 기본 명령은 로컬 검증·README 캡처를 계속 생성합니다.
- 최종 diff 공백 검사 및 추적/신규 텍스트 파일의 비밀키·개인 이메일·로컬 사용자 경로 검사 PASS(테스트용 qa@example.test 제외). README 체크박스 없음, README 상대 링크 대상 파일 존재 확인. 릴리스 검사는 6종 PNG 실재 여부도 검사합니다.
