# 결정 사항 기록

현재 개인화 완성 상태: **TBD**. 기능 검증용 중립 UI는 최종 디자인이 아닙니다.
`TBD → CONFIRMED → APPLIED → VERIFIED` 순서로 관리합니다. 사용자가 명시한 정보만 CONFIRMED로 변경합니다. 재결정 시 영향을 받는 항목을 다시 검증합니다.

모든 개인화 값의 기본 위치는 `js/config.js`의 `personal`입니다. 아래의 키는 그 객체 안의 키입니다. `value: null`은 미정이고, `placeholder`는 화면용 안내 문구입니다. 미정 상태에서 `value`만 수정해도 화면에 적용되지 않습니다.

| 항목 ID | 항목 이름 | 현재 상태 | 결정될 내용 | 영향을 받는 파일과 UI 영역 | 확정 시 적용 방법 |
| --- | --- | --- | --- | --- | --- |
| TBD_DISPLAY_NAME | 공개 표시 이름 | TBD | 공개할 이름 | config.js / Hero, 문서 제목 | displayName.value 문자열 및 상태 갱신 |
| TBD_PERSONAL_BACKGROUND | 개인 배경 | TBD | 공개할 배경 | config.js / About | personalBackground.value 문자열 |
| TBD_INTRODUCTION_DIRECTION | 소개 방향 | TBD | 자기소개 방향과 범위 | config.js / Hero·About 문구 | introductionDirection 기록 후 관련 문구를 각각 확정 |
| TBD_INTERESTS | 관심 분야 | TBD | 공개할 관심사 | config.js / About | interests.value 문자열 |
| TBD_ACTIVITIES | 활동·경험 | TBD | 공개할 실제 경험 | config.js / About | activities.value 문자열 |
| TBD_DESIGN_CONCEPT | 디자인 콘셉트 | TBD | 최종 콘셉트 | config.js, css/style.css / 전체 | designConcept 기록 후 레이아웃·변수 변경 및 전체 회귀 검증 |
| TBD_DESIGN_PREFERENCES | 색상·분위기 | TBD | 색상, 폰트, 형태 | config.js, css/style.css / 전체 | designPreferences 기록, :root·다크 테마 변수 변경 |
| TBD_PERSONAL_CONTENT | 추가 개인화 콘텐츠 | TBD | 공개할 추가 내용 또는 미사용 결정 | config.js, index.html / 확정되는 영역 | personalContent에 기록 후 의미 구조를 유지하여 추가 |
| TBD_PUBLIC_CONTACT | 공개 연락처 | TBD | 공개할 연락처 또는 비공개 결정 | config.js / Contact | publicContact.value 문자열, 링크가 필요하면 별도 검증 |
| TBD_SOCIAL_LINKS | 소셜 링크 | TBD | 실제 링크 또는 미사용 결정 | config.js / Footer | socialLinks.value에 {label, url} 배열, 미사용은 [] |
| TBD_PROFILE_IMAGE | 프로필 이미지 | TBD | 본인 승인 이미지·대체 텍스트 | config.js, images/ / About | profileImage.value에 {src, alt}, 실제 파일 추가 |
| TBD_LOGO_CONTENT | 로고 내용 | TBD | 로고에 쓸 문자열 또는 시각 요소 | config.js / Header | logoContent.value 문자열, 시각 로고는 구조·alt 별도 검증 |
| TBD_HERO_GREETING | 인사말 | TBD | 인사 문구 | config.js / Hero | heroGreeting.value 문자열 |
| TBD_HERO_HEADLINE | 소개 제목 | TBD | 대표 제목 | config.js / Hero | heroHeadline.value 문자열 |
| TBD_HERO_DESCRIPTION | 소개 문구 | TBD | 대표 설명 | config.js / Hero | heroDescription.value 문자열 |
| TBD_HERO_PERSONAL_VISUAL | Hero 시각 요소 | TBD | 이미지·장식 여부와 표현 | config.js, css/style.css, index.html / Hero | heroPersonalVisual 기록, 문자열은 자동 반영·이미지는 구조 적용 |
| TBD_ABOUT_INTRODUCTION | About 소개 | TBD | 본문 소개 | config.js / About | aboutIntroduction.value 문자열 |
| TBD_SKILL_LIST | 기술 목록 | TBD | 확인된 기술명 | config.js / Skills | skillList.value에 기술명 문자열 배열 |
| TBD_SKILL_CATEGORIES | 기술 분류 | TBD | 기술별 분류 | config.js / Skills | skillCategories.value에 기술명을 키로 하는 객체 |
| TBD_SKILL_DESCRIPTIONS | 기술 설명 | TBD | 기술별 실제 학습·경험 설명 | config.js / Skills | skillDescriptions.value에 기술명을 키로 하는 객체 |
| TBD_PROJECT_PRESENTATION_PREFERENCE | 프로젝트 표시 방식 | TBD | 선별·강조 방식 | config.js, main.js / Projects | 현재 API 순서 전체 공개 목록 유지, 결정 후 렌더링만 변경 |
| TBD_CONTACT_INTRO_TEXT | 연락 안내 | TBD | 안내 문구 | config.js / Contact | contactIntroText.value 문자열 |
| TBD_CONTACT_VISUAL_STYLE | Contact 시각 스타일 | TBD | 폼의 최종 표현 | config.js, css/style.css / Contact | contactVisualStyle 기록 후 스타일·접근성 검증 |
| TBD_FOOTER_DISPLAY_NAME | 저작권 표시 이름 | TBD | 저작권 영역 이름 | config.js / Footer | footerDisplayName.value 문자열, 표시 이름과 자동 동일시하지 않음 |
| TBD_FOOTER_PERSONAL_MESSAGE | 푸터 문구 | TBD | 마지막 문구 또는 미사용 결정 | config.js / Footer | footerPersonalMessage.value 문자열 |

## 확정된 기능 조건

| 항목 ID | 항목 이름 | 현재 상태 | 결정될 내용 | 영향을 받는 파일과 UI 영역 | 확정 시 적용 방법 |
| --- | --- | --- | --- | --- | --- |
| GITHUB_ACCOUNT | GitHub 계정 | VERIFIED | gareal2117 (사용자 제공) | config.js, index.html / Projects·Footer | 실제 API로 공개 저장소 7개 조회, 링크 렌더링 검증 |
| STACK | 기술 스택 | VERIFIED | HTML5, CSS3, Vanilla JavaScript | 전체 소스 | 정적 검사 및 Chrome 실행 검증, 외부 UI 라이브러리·빌드 의존성 없음 |

## 선택 과제 및 외부 작업

언어 필터, 타이핑 효과, 시스템 테마 감지는 **선택 미정**이며 현재 구현하지 않았습니다. 필수 기능 완료와 별개입니다.
실제 문의 전송은 **보류**입니다. 외부 서비스·전송 방식·공개 연락처의 결정 및 승인 이후 진행합니다.
저장소 생성, 원격 push, GitHub Pages 공개 배포는 **승인 전 미실행**입니다. 저장소 이름 `codyssey-portfolio`는 제안일 뿐입니다.

## 변경 절차

1. 사용자가 결정한 해당 항목만 CONFIRMED로 기록합니다.
2. `config.js`의 같은 키에 value를 넣습니다. 데이터 형식은 README의 개인화 절차를 따릅니다.
3. CSS·이미지·구조 변경이 필요한 항목은 해당 파일도 수정한 뒤 APPLIED로 기록합니다.
4. 기존 기능, 모바일·다크 모드, 안전한 렌더링을 검증한 뒤 VERIFIED로 기록합니다.
5. 관련되지 않은 다른 TBD는 유지합니다. 전체 개인화가 확정되기 전에는 기능 완료를 최종 제출 완료로 해석하지 않습니다.
