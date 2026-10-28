# 코디세이 포트폴리오

AI/SW 기초 · 웹 기초와 프론트엔드 필수 과제 **「나를 소개하는 웹페이지 처음부터 만들기」**를 위한 정적 웹사이트입니다. 학습시간 기준은 80시간이며, 시맨틱 HTML, 반응형 CSS, DOM 이벤트와 상태 관리, 외부 API, 입력 검증을 학습합니다.

개인화 콘텐츠와 최종 디자인은 아직 **TBD**입니다. 현재 화면은 중립적인 기능 검증용 UI입니다. GitHub ID `gareal2117` 외의 이름·경력·기술·연락처는 임의로 만들지 않았습니다. 기능 검증과 개인화·공개 준비 상태는 [TEST_REPORT.md](./TEST_REPORT.md)에서 구분합니다.

## 실행 방법

1. VS Code에서 현재 `my-portfolio` 폴더를 엽니다. 이 폴더 자체가 프로젝트 루트이며 `codyssey-portfolio` 폴더를 중복 생성할 필요가 없습니다.
2. Live Server 확장이 설치되어 있다면 `index.html`을 우클릭하고 **Open with Live Server**를 실행합니다.
3. 브라우저에서 열린 로컬 주소를 확인합니다. API 조회에는 인터넷 연결이 필요합니다.

대안으로 Python이 설치되어 있다면 프로젝트 루트에서 다음을 실행한 뒤 `http://localhost:5500`을 엽니다.

```sh
python3 -m http.server 5500 --bind 127.0.0.1
```

별도 백엔드, npm 설치, 빌드 과정이 필요하지 않습니다. `file://`로 직접 열기보다 HTTP 서버를 권장합니다. 폼은 입력 검증용이며 데이터를 저장·전송하지 않습니다.

## 기술과 구조

HTML5, CSS3, Vanilla JavaScript(ES6+), GitHub REST API를 사용합니다. 외부 폰트·아이콘·UI 라이브러리는 사용하지 않았습니다. Google Fonts와 Font Awesome 사용 여부는 디자인 확정 후 결정합니다.

```text
my-portfolio/                 # 원격 저장소 이름 제안: codyssey-portfolio
├── index.html                # 의미 구조, 정적 플레이스홀더
├── css/style.css             # 변수, 중립 UI, 반응형, 테마
├── js/config.js              # 확정 계정 및 개인화 TBD 25항목
├── js/main.js                # 상태, 이벤트, 렌더링, API, 검증
├── images/.gitkeep           # 승인된 프로필 이미지 저장 위치
├── tests/
│   ├── static_checks.py      # 구조·경로·필수 패턴 검사
│   ├── browser_checks.py     # 설치된 Chrome의 실제 동작 검사
│   └── release_check.py      # 공개 전 미정·미검증 결정 검사
├── docs/
│   ├── browser-results.json  # 실제 브라우저 자동화 결과
│   └── screenshots/          # 실제 로컬 페이지 캡처
├── README.md
├── DECISIONS.md
├── TEST_REPORT.md
└── .gitignore
```

## 주요 기능과 상태 흐름

- Header와 Home/About/Skills/Projects/Contact, Footer의 시맨틱 구조 및 건너뛰기 링크.
- 모바일 메뉴 열기/닫기, 링크 선택·Escape·바깥 클릭·초점 이탈 시 닫기, `aria-expanded` 동기화.
- 앵커 부드러운 스크롤과 헤더 가림 방지, **300px 이상**에서 Scroll-to-top 표시, **60px 이상**에서 헤더 배경 변경.
- 다크 모드 및 `localStorage` 유지. 저장소 접근이 차단되어도 현재 테마 전환 가능.
- `IntersectionObserver`의 **threshold: 0.2**를 사용한 화면 진입 애니메이션. Observer/JavaScript 미지원에서도 본문이 보이며, reduced-motion은 움직임을 중단합니다.
- GitHub 공개 저장소 카드와 실제 재요청하는 오류 복구 버튼.
- 이름·이메일·메시지 검증, 필드별 오류, 수정 시 갱신, 검증 완료 안내. 실제 전송 기능 없음.

핵심은 **이벤트 → 상태 변경 → DOM 업데이트**입니다.

| 영역 | 이벤트 | 상태 | 화면 갱신 |
| --- | --- | --- | --- |
| Theme | 버튼 click | state.theme, localStorage 저장 시도 | renderTheme: data-theme, 버튼·aria |
| Projects | 최초 로드 / 재시도 click | loading → success / error / empty | renderProjects: 상태 문구·카드·재시도 |
| Form | input / submit | values, errors, submitted, success | renderFormState: 오류·aria-invalid·결과 |
| Menu | click / Escape / 화면 전환 | menuOpen | renderMenu: active 클래스·aria-expanded |

`config.js`와 `main.js`는 순서가 보장되는 두 개의 `defer` 스크립트입니다. 설정의 전역 객체 `window.PortfolioConfig` 하나만 공개하고 실행 로직은 즉시 실행 함수 안에 둡니다. 개인화 문자열과 API 데이터는 `textContent`로 표시합니다. 필수 `innerHTML`은 개발자가 작성한 고정 카드 골격에만 사용합니다. 외부 URL은 HTTPS 및 저장소 호스트를 검사하고 새 창 링크에 `noopener noreferrer`를 적용합니다.

## GitHub API

기본 엔드포인트: `https://api.github.com/users/gareal2117/repos`

한 페이지당 최대 100개를 요청하고 `Link` 응답 헤더에 다음 페이지가 있을 때만 순차적으로 이어갑니다. 특정 프로젝트를 임의로 강조하지 않고 API 제공 순서로 전체 공개 목록을 표시합니다. `fetch` + `async/await`, `response.ok`, `try/catch`를 사용합니다.

설명·언어·Star·URL이 null이면 해당 정보가 없음을 표시합니다. 배열이 아닌 응답, 잘못된 JSON, null 항목, 네트워크 오류, HTTP 오류, 403/429, 요청 시간 초과를 오류 UI로 전환합니다. 각 요청 제한시간은 15초이며 자동 재시도는 없습니다. 한 번의 목록 요청이 진행 중이면 중복 요청을 무시합니다. 인증되지 않은 요청의 기본 한도는 보통 시간당 60회이므로 새로고침과 재시도를 불필요하게 반복하지 않습니다. 토큰이나 비밀키는 없습니다. [GitHub REST API 공식 문서](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user)를 참고했습니다.

테스트는 대부분 브라우저의 `fetch`를 테스트 페이지에서만 교체하여 실행합니다. 가짜 저장소를 실제 프로젝트 데이터나 제출 스크린샷으로 사용하지 않습니다.

## 반응형과 디자인 교체

모바일 기본 스타일에 **768px** 태블릿, **1024px** 데스크톱 미디어 쿼리를 추가했습니다. 네비게이션은 Flexbox, 프로젝트는 `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` Grid입니다. 좁은 화면과 긴 저장소 이름에서도 가로 넘침을 방지합니다.

`css/style.css`의 `:root`에서 색상·폰트·간격·배경·카드·테두리·그림자·버튼 형태를 바꿀 수 있습니다. 다크 모드 변수는 `[data-theme="dark"]`에 있습니다. Hero 시각 요소, 프로필 이미지, 장식은 사용자 결정 후 적용합니다. 임시 중립 색상은 개인 취향을 확정한 것이 아닙니다.

## 개인화 적용 방법

전체 목록과 영향 범위는 [DECISIONS.md](./DECISIONS.md)에 있습니다. 사용자 확인 없이 상태를 바꾸지 않습니다.

1. 해당 `personal` 항목의 `value`에 승인된 값을 넣고 `status`를 `CONFIRMED`로 바꿉니다. 일반 문구는 문자열입니다.
2. 적용 후 `APPLIED`, 브라우저 검증 후 `VERIFIED`로 설정과 결정 문서를 함께 갱신합니다.
3. 기술 목록은 `skillList.value` 문자열 배열, `skillCategories.value`와 `skillDescriptions.value`는 기술명을 키로 하는 객체입니다. 숙련도 퍼센트는 생성하지 않습니다.
4. 프로필은 `images/`에 승인된 파일을 넣고 `profileImage.value`를 `{ src: './images/파일명.webp', alt: '승인된 대체 텍스트' }`로 설정합니다. 파일명은 영문·숫자·하이픈·밑줄을 사용합니다. 로딩 실패 시 미정 이미지 영역으로 돌아갑니다.
5. 소셜 링크는 `{ label, url }` 객체 배열이며 HTTPS만 허용합니다. 공개하지 않기로 확정하면 빈 배열을 사용합니다. 연락처는 문자열로 표시하며 전송 서비스와 연결되지 않습니다.
6. 디자인 콘셉트·추가 콘텐츠·Hero 시각 요소·프로젝트 표시 선호는 설정에 결정을 기록한 뒤 필요한 CSS/HTML/렌더링 변경을 별도로 적용합니다. 모든 항목이 단순 문자열 교체로 처리되는 것은 아닙니다.

문구를 설정에서 바꿔도 JavaScript가 없는 환경은 정적 HTML 플레이스홀더를 표시합니다. **최종 제출 시 index.html의 대체 콘텐츠도 확정된 내용으로 동기화**하고, 문서 제목·설명·미정 안내와 실제 렌더링을 검토해야 합니다. 의도적인 미사용은 빈 문자열/배열 및 결정 사유로 기록하고 해당 구조를 검토합니다.

현재 `pending(...)` 호출을 아래 형식의 객체로 교체하면 개별 값을 입력할 수 있습니다. 아래는 문서의 형식 설명이며 실제 사용자 정보가 아닙니다.

```js
displayName: {
  id: 'TBD_DISPLAY_NAME',
  status: 'CONFIRMED',
  value: '사용자가 직접 확정한 표시 이름',
  placeholder: '[표시 이름 미정]'
},
```

## 테스트와 스크린샷

```sh
python3 tests/static_checks.py
python3 tests/browser_checks.py
python3 tests/release_check.py
```

브라우저 검사는 macOS의 설치된 Chrome을 기본 사용하며 다른 환경은 `CHROME_BIN`에 실행 파일 경로를 설정합니다. Python 표준 라이브러리만 사용합니다. 로컬 포트와 Chrome 실행 권한이 필요합니다. 임시 프로필과 서버는 종료 시 정리됩니다. 앱 런타임은 Python에 의존하지 않습니다.

`release_check.py`는 현재 개인화 TBD가 남아 있어 **종료 코드 1이 정상적인 차단 결과**입니다. 기능 실패와 구별합니다. 이 검사가 통과해도 최종 화면의 미정 문구·링크·이미지·스크린샷과 공개 승인은 별도 확인해야 합니다.

아래 이미지는 실제 로컬 사이트 캡처입니다. 최종 디자인이나 최종 제출 완료 화면이 아니며 개인화 후 다시 캡처해야 합니다.

- [데스크톱 1440px](./docs/screenshots/desktop.png)
- [모바일 375px](./docs/screenshots/mobile.png)
- [다크 모드 1440px](./docs/screenshots/dark.png)

상세 PASS/PARTIAL/FAIL/BLOCKED 구분은 [TEST_REPORT.md](./TEST_REPORT.md), 자동화의 개별 결과는 [browser-results.json](./docs/browser-results.json)을 확인합니다.

## GitHub 및 GitHub Pages 배포 준비

현재 로컬 Git 저장소와 원격 저장소는 생성하지 않았습니다. GitHub 인증, 원격 push, 공개 배포도 수행하지 않았습니다.

- 확정된 GitHub 프로필: https://github.com/gareal2117
- 저장소 이름 제안: `codyssey-portfolio`
- **저장소 URL 후보(생성 완료 아님)**: `https://github.com/gareal2117/codyssey-portfolio`
- **배포 URL 예시(실제 배포 확인 안 됨)**: `https://gareal2117.github.io/codyssey-portfolio/`
- 실제 저장소 이름 충돌 점검 결과는 TEST_REPORT의 C 항목을 확인합니다. 비공개 저장소는 인증 없이 확인할 수 없으므로 생성 직전 계정에서 재확인해야 합니다.

다음 절차는 사용자 승인 후 수행할 배포 안내이며 실행 기록이 아닙니다.

1. 개인화 항목을 확정·적용·검증하고 `release_check.py` 및 최종 제출 체크리스트를 확인합니다.
2. GitHub에서 `codyssey-portfolio` 이름의 기존 저장소 유무를 다시 확인합니다. 기존 원격 저장소를 덮어쓰지 않습니다.
3. 공개 범위와 배포 승인을 받은 뒤 저장소를 만들고, 로컬 Git 초기화·커밋 및 해당 원격으로 push합니다. 배포 루트에 `index.html`, `css/`, `js/`, `images/`가 위치하도록 합니다.
4. 저장소 **Settings → Pages**에서 브랜치 기반 배포를 선택하고 `main` 브랜치의 `/(root)`를 소스로 지정합니다.
5. 배포 작업 성공 후 GitHub가 표시한 실제 URL을 열어 앵커, 에셋, API, 폼, 모바일·다크 모드를 재검증합니다.
6. 검증된 실제 저장소·배포 URL과 최종 스크린샷으로 이 문서를 갱신합니다.

설정 절차는 [GitHub Pages 공식 생성 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)를 기준으로 정리했습니다. 로컬 하위 경로 검증과 실제 GitHub Pages 배포 검증은 별개입니다.

## 알려진 제한과 학습 순서

- 개인화 25항목과 최종 디자인 미정. 프로필 이미지와 실제 기술 목록은 없음.
- 실제 이메일 전송, 프로젝트 언어 필터, 타이핑 효과, 시스템 테마 감지는 선택 과제로 보류.
- API 상태는 GitHub 네트워크·요청 제한에 영향을 받음. 오프라인 캐시는 없음.
- 자동화로 스크린리더의 실제 음성 출력이나 모든 OS/브라우저를 검증하지는 않음.
- 제출·공개 완료를 선언하기 전에 사용자 검토 이후 독립적인 최종 재검토가 필요함.

학습은 `index.html`의 의미 구조와 label → CSS 변수·Flexbox/Grid·미디어 쿼리 → `state`와 `renderTheme()` → 폼의 `input → validateField → renderFormState` → `fetchProjects()`의 비동기·오류·페이지네이션 → 접근성·보안 → Git과 GitHub Pages 순서로 진행하면 좋습니다.
