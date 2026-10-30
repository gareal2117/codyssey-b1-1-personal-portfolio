# 요구사항 추적표 — 최신 상태 (2026-10-30)

구현 전 A~J 기준표를 먼저 작성한 뒤 실제 소스와 새 시험에 대조했습니다. 1차 57 PASS는 과거 이력으로만 사용합니다. 사용자 대화의 과제 원문과 실행하도록 지정한 2차 프롬프트가 조항의 기준입니다.

| 원문 조항 | 구현 파일·함수 | 테스트 케이스 | 결과 | 실제 증거 |
| --- | --- | --- | --- | --- |
| A1. 파일 구조·HTML/CSS/Vanilla JS·외부 CSS/defer | index.html; config.js → main.js | static_checks.py 구조/경로; 하위 경로 CSS·JS 로딩 | PASS | 정적 HTTP 실행, 빌드/UI 라이브러리 없음 |
| A2. VS Code+Live Server·최소 실행 경로 | README 2절 | Python HTTP 실제 실행 / VS Code 확장 UI 미조작 | PARTIAL | 명령·Windows 대안·file://와 프로젝트 경로 설명 |
| A3. JS 미지원·프로젝트 하위 경로 | index.html 정적 콘텐츠; 상대 에셋 | JavaScript 미지원 정적 콘텐츠·안전한 폼 / 하위 경로 CSS·JS 로딩 | PASS | 목표 /codyssey-b1-1-personal-portfolio/에서 검사 |
| B1. header/nav/main/section/article/footer·전체 필수 섹션 | index.html; makeProjectCard | 정적 구조 / API 성공·map 카드·article | PASS | Home/About/Skills/Projects/Contact 및 Footer |
| B2. Hero CTA·앵커·키보드 | 앵커 click 리스너 | 앵커 이동·메뉴 닫기·헤더 가림 방지 | PASS | id·href 검사와 실제 스크롤/초점 |
| B3. About 프로필 이미지·alt·실제 파일 | profile-monogram.svg; renderPersonalContent | 프로필 img 실제 로드·alt·SVG 경로 / 프로필 표시 비율 보존 | PASS | 정적 SVG script/외부 참조 검사, 실제 naturalWidth=480 |
| B4. label/for/id·heading 계층 | index.html; makeProjectCard h4 | 정적 label/중복 id + 문서 계층 검토 | PASS | h1 → 구역 h2 → 그룹 h3 → 카드 h4 |
| B5. 25개 개인화·무중복·공개 범위 | config.js; DECISIONS; personalization-contract.json | 25개 ID·값 승인 계약과 정확히 일치 / Footer GitHub 중복 없음·비공개 연락처 | PASS | 모든 값 VERIFIED, 디자인 최종 승인과 외부 완료 별도 |
| C1. CSS 변수·data-theme | style.css :root/[data-theme] | 테마·대비 시험 / 정적 변수 검사 | PASS | 색상·폰트·간격·배경·카드·경계·그림자 변수 |
| C2. mobile-first 768/1024·Flex nav·auto-fit/minmax Grid | navigation; project-grid; 미디어쿼리 | 375/768/1024/1440px 카드 Grid·메뉴 전환 | PASS | 4 너비 실브라우저 computed style·overflow |
| C3. hover/transition/shadow/focus-visible | button; project-card; :focus-visible | 스타일 직접 대조 + 키보드 입력/초점 시험 | PASS | 스크린샷과 computed contrast; 전체 보조기기 인증 아님 |
| C4. 가독성·두 테마·reduced-motion | style.css; setupTyping; reducedMotion | light/dark 일반 텍스트 대비 4.5:1 / reduced-motion 타이핑 생략 | PASS | 대비 결과 JSON, motion에서 움직임 중단 |
| D1. querySelector/All·textContent·안전한 innerHTML | select; makeProjectCard; renderPersonalContent | API HTML 삽입 방지·URL 검증; 정적 검사 | PASS | 외부 HTML 문자열은 태그가 아닌 글자로 렌더 |
| D2. 템플릿 리터럴 동적 HTML | makeProjectCard | Featured 실제 배열에서만 선별·동적 HTML | PASS | 내부 featured bool과 숫자 순번만 HTML 보간 |
| D3. classList add/remove/toggle; click/submit/scroll/input; preventDefault | renderMenu/renderScroll/renderFormState; 이벤트 | 메뉴·경계값·입력·제출 실제 시험 | PASS | README 5~7절에 쓰임새/실행 순서 설명 |
| D4. const/let·화살표·구조분해·map/filter/forEach·async/await/try/catch | main.js | 정적 요구 문법 + 카드/필터/API 동작 시험 | PASS | var·인라인 이벤트·style 속성 없는 앱 |
| E1. 햄버거·aria-expanded·Escape·focus | renderMenu/closeMenu | 모바일 메뉴 열기/다시 닫기 / Escape / Enter | PASS | 링크 선택 후 메뉴 닫힘 포함 |
| E2. 부드러운 앵커·탑 300·헤더 60 | 앵커 리스너; renderScroll | 59/60/299/300px / Scroll-to-top 상단 이동 | PASS | rAF 예약·passive scroll; 기준값 README 일치 |
| E3. 테마 저장/새로고침/예외 | initializeTheme/setTheme/renderTheme | 테마 새로고침 유지 / localStorage 읽기·쓰기 차단 복구 | PASS | 저장 실패가 다른 기능을 중단하지 않음 |
| E4. IntersectionObserver >=0.2·fallback | Observer threshold:0.2 | Observer 화면 진입 애니메이션 / Observer 미지원 시 콘텐츠 표시 | PASS | 기본 콘텐츠를 숨기지 않음 |
| E5. 폼 실시간 오류/성공 | validateField/renderFormState/submitContact | input 수정 시 오류 갱신 / 메일 mock 성공 후에만 reset | PASS | 설정 전 검증 안내와 실제 응답 success 구분 |
| F1. 테마 상태 흐름 | state.theme/manualTheme → renderTheme | 시스템/수동/저장 시험 | PASS | README 6·8절 이벤트→상태→DOM |
| F2. API·필터 상태 흐름 | state.projects → renderProjects/renderRepositoryList | API 4상태 / 필터·건수·무재호출 | PASS | API 원본 보존, 화면 상태에서 렌더 |
| F3. 폼 상태 흐름 | state.form.status → renderFormState | invalid/idle/submitting/success/error 시험 | PASS | 실제 수신은 사용자 확인; 자동 시험은 mock |
| G1. 확정 GitHub endpoint·실제 데이터 | fetchProjects | 실제 GitHub API 연결 | PASS | 8개 공개 저장소 확인; 수치는 조회 시점 기준 |
| G2. fetch/async/await/response.ok/try-catch·loading/success/error/empty | fetchProjects/renderProjects | API Loading/Empty/성공/HTTP 오류 | PASS | 공개 데이터만 사용, 토큰 없음 |
| G3. 403/429·rate limit·재시도·중복 방지 | fetchProjects 오류 분기 | HTTP 403/429/500 및 재시도 / 불필요한 API 중복 요청 없음 | PASS | 시간당 60/IP 한도 설명·무한 재시도 없음 |
| G4. 네트워크·null·비정상 응답·JSON | fetchProjects/makeProjectCard | 네트워크/객체/null응답/null항목/JSON파싱 오류 / null 속성 | PASS | fixture 재현, GitHub 실제 장애 유발 안 함 |
| G5. 페이지네이션·timeout·안전URL·콘솔 | fetchProjects; safeHttpsUrl | API 페이지네이션 / AbortError / 미처리 예외 없음 | PASS | API 15초 실제 기다림은 미수행, 분기·타이머 코드 검토 |
| G6. README 실제 경로·브랜치·캐시·실패 격리 | verify_readmes.py; getReadmeUrl | 검증된 README·브랜치만 링크 / 오래된 README 캐시 숨김 | PASS | readme-verification.json: 5개 200, 나머지404; 앱 방문별 개별 API 없음 |
| H1. name/email/message 필수·공백·형식·길이 | index.html; validateField | 빈폼/공백/이메일/input수정/길이 제한 | PASS | 100/254/5000; label·오류 인접 |
| H2. preventDefault·aria-live·성공 조건 | submitContact/renderFormState | 정상 입력 검증·미전송 명시 / 접수와 수신함 도착 구분 | PASS | 설정 누락은 접수 성공으로 표시하지 않음 |
| I1. 언어 필터·Array.filter·All만·0건·키보드 | renderFilters/renderRepositoryList | 언어/null/0건/Enter/Featured 영향 없음 | PASS | 동적 옵션·aria-pressed·건수·무재호출 |
| I2. Hero 실제 타이핑·완전한 초기 문구·접근성·motion | setupTyping | 중간 상태/완료/1회/배경탭/reduced-motion | PASS | sr-only 정적 텍스트와 aria-hidden 시각 텍스트 분리 |
| I3a. Formspree 코드·전송 상태·스팸/중복/설정/timeout | canSendEmail/submitContact; EMAIL_SETUP | 메일 mock 성공/422/429/500/네트워크/서비스/JSON/timeout/중복/honeypot | PASS | 모든 메일 시험은 mock, 외부 호스트 차단 |
| I3b. Formspree 실제 발송·수신 확인 | 사용자 외부 계정/수신설정/테스트 승인 | 사용자 직접 발송·스팸함 수신 확인 | PASS | 2026-10-30 사용자 보고; formId=mdeezyjq, enabled=true, emailLiveVerified=true; 추가 발송 없음 |
| I4. prefers-color-scheme·수동 저장 우선 | initializeTheme/systemTheme change | 시스템 dark/변경/수동 우선/reload/저장 차단 | PASS | 첫 페인트는 CSS 시스템 감지; 수동 저장 복원 전 플래시 한계 명시 |
| J1. 프로젝트 설명·학습 README·19절·실습·복습 | README 0~18 | 목차/실제 함수·선택자·수치 대조 | PASS | 11개 실습, 15개 설명형 문제와 해설 |
| J2. desktop/mobile/dark 실제 캡처 | docs/screenshots | 실제 화면 스크린샷 6종 | PASS | 실제 API 응답으로 캡처, fixture는 이후에 주입 |
| J3. 실제 GitHub 저장소 URL·origin·rename | Git 현황·인증 API | 기존 빈 포트폴리오 rename, origin 연결, 실제 URL 확인 | PASS | gareal2117/codyssey-b1-1-personal-portfolio; Pages 접속은 사용자 확인 완료 |
| J4. 작동 Pages URL·공개 승인·제출 완료 | release 설정; README18 | Pages HTTP 200; 최신 배포 검증은 TEST_REPORT 참조 | BLOCKED | 실제 URL은 README 18절; 제출 완료는 디자인 최종 승인 기록 없음으로 차단 |

요구사항 행 집계(브라우저 테스트 개수와 다름): PASS 39, PARTIAL 1, FAIL 0, BLOCKED 1. I3b는 사용자 수신 확인으로 갱신했으며 J4의 전체 제출은 디자인 최종 승인 전입니다.

증거: [브라우저 JSON](./browser-results.json), [검증 보고서](../TEST_REPORT.md), [README 검증](./readme-verification.json), [사용자 결정](../DECISIONS.md).

## 과거 2차 검증 당시 별도 두 번째 대조 검토 (이력)

1. **A~J → 소스/테스트 재대조:** 필수 문법을 단순 문자열 검사에만 의존하지 않고 실제 메뉴·카드·필터·폼의 DOM 결과와 연결했습니다. 동적 HTML은 고정 골격/내부 순번이며 외부 문자열은 textContent입니다. 이미지 실파일·no-JS·하위 경로를 추가 확인했습니다.
2. **25개 확정값·학습 깊이·공개 범위 재대조:** config/정적 HTML/승인 계약/DECISIONS를 비교했습니다. 빈 personalContent/footerPersonalMessage는 의도적 생략, publicContact는 비공개 안내, Footer 소셜은 GitHub 하나입니다. README 3~11절의 정의·이유·실제 함수·예제·예외·확인 방법, 11개 실습과 15개 해설을 점검했습니다. 디자인 기술 검증은 최종 사용자 승인과 분리했습니다.
3. **보류 판단:** 메일 mock을 실전 발송으로, 로컬 하위 경로를 실제 Pages로 간주하지 않았습니다. 계정·서비스 설정·실제 발송 승인·원격 게시·최종 시각 검토가 필요합니다. 실제 스크린리더/다른 OS·브라우저/VS Code 확장 UI 조작은 이번 검증 범위 밖입니다.

검토는 동일 에이전트가 구현 후 별도 대조 순서로 수행했으며 별도 사람/서브에이전트가 승인한 것으로 표현하지 않습니다.
