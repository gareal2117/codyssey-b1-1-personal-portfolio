# 개인화 결정 기록 — 2차

사용자가 실행하도록 지정한 2차 프롬프트의 25개 키/값을 적용했습니다. 1차 TBD 기록은 docs/history/phase1/DECISIONS.md에 보존했습니다.

25개 항목은 CONFIRMED(사용자 2차 프롬프트) → APPLIED(코드 적용) → VERIFIED(새 Chrome·승인 계약 검사)로 진행했습니다. VERIFIED는 로컬 적용 검증입니다. 디자인 동작 검증은 사용자의 시각적 최종 승인과 다르며, `release.designApproved`는 false입니다. 이메일 실전 발송·공개 게시도 별도이며 최신 상태는 마지막 후속 기록을 따릅니다.

| 항목 ID | 키 | 상태 | 결정 내용 | 영향 영역 / 적용 방법 |
| --- | --- | --- | --- | --- |
| TBD_DISPLAY_NAME | displayName | VERIFIED | 이준성 &#124; Junseong Lee | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_PERSONAL_BACKGROUND | personalBackground | VERIFIED | 광운대학교 정보융합학부 재학, 코디세이 AI 올인원 과정 학습 | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_INTRODUCTION_DIRECTION | introductionDirection | VERIFIED | 개발자 포트폴리오/개인 브랜딩, 개발 중심·음악 취미 간단히 | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_INTERESTS | interests | VERIFIED | 프로그래밍과 다양한 개발 기술 | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_ACTIVITIES | activities | VERIFIED | 코디세이 과제 학습·수행, 취미로 다양한 음악 활동 | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_DESIGN_CONCEPT | designConcept | VERIFIED | Blueberry Signal | config.js, style.css / Blueberry Signal, 사용자 최종 시각 승인 대기 |
| TBD_DESIGN_PREFERENCES | designPreferences | VERIFIED | Blueberry Burst 네이비/블루/스카이블루, 비대칭 타이포 중심, 주요 이름 정자체 | config.js, style.css / Blueberry Signal, 사용자 최종 시각 승인 대기 |
| TBD_PERSONAL_CONTENT | personalContent | VERIFIED | 의도적인 미사용(빈 문자열) | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_PUBLIC_CONTACT | publicContact | VERIFIED | 이메일과 전화번호는 공개하지 않습니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_SOCIAL_LINKS | socialLinks | VERIFIED | [{"label": "GitHub", "url": "https://github.com/gareal2117"}] | config.js / #social-links, 중복 제거 |
| TBD_PROFILE_IMAGE | profileImage | VERIFIED | {"src": "./images/profile-monogram.svg", "alt": "이준성의 영문 이니셜 JL을 표현한 파란색 프로필 모노그램 그래픽"} | images/profile-monogram.svg / img src·alt 및 안전한 경로 |
| TBD_LOGO_CONTENT | logoContent | VERIFIED | JL | config.js, index.html / Header의 마침표만 제거, CSS 유지 |
| TBD_HERO_GREETING | heroGreeting | VERIFIED | 안녕하세요. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_HEADLINE | heroHeadline | VERIFIED | 개발자로 성장하고 있는 이준성입니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_DESCRIPTION | heroDescription | VERIFIED | 새로운 기술을 배우고 직접 구현하며, 개발 역량을 쌓아가고 있습니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_PERSONAL_VISUAL | heroPersonalVisual | VERIFIED | 블루베리 시그널 추상 CSS 그래픽 | config.js, style.css / Blueberry Signal, 사용자 최종 시각 승인 대기 |
| TBD_ABOUT_INTRODUCTION | aboutIntroduction | VERIFIED | 광운대학교 정보융합학부에 재학 중이며, 코디세이 AI 올인원 과정에서 다양한 과제를 수행하며 소프트웨어 개발을 공부하고 있습니다. / 프로그래밍과 다양한 개발 기술에 관심을 가지고 있습니다. / 개발 외에는 다양한 음악 활동을 즐기는 것이 취미입니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_SKILL_LIST | skillList | VERIFIED | ["Python", "Git", "GitHub", "Docker"] | config.js / renderPersonalContent, #skills-list |
| TBD_SKILL_CATEGORIES | skillCategories | VERIFIED | {"Python": "Programming", "Git": "Version Control", "GitHub": "Repository Hosting", "Docker": "Development Environment"} | config.js / renderPersonalContent, #skills-list |
| TBD_SKILL_DESCRIPTIONS | skillDescriptions | VERIFIED | {"Python": "기초 프로그래밍 및 과제 구현", "Git": "버전 관리 및 브랜치 실습(merge·충돌 해결 경험)", "GitHub": "저장소 생성 및 코드 관리", "Docker": "컨테이너 및 개발환경 구성 실습"} | config.js / renderPersonalContent, #skills-list |
| TBD_PROJECT_PRESENTATION_PREFERENCE | projectPresentationPreference | VERIFIED | Featured 3개 + All Repositories + GitHub 및 실존 README 링크 | config.js, main.js / Featured·All·README 캐시 |
| TBD_CONTACT_INTRO_TEXT | contactIntroText | VERIFIED | 아래 폼으로 문의를 남길 수 있습니다. 개인 이메일 주소는 공개하지 않습니다. | config.js, index.html / 활성 폼 안내와 정적 대체문구 동기화 |
| TBD_CONTACT_VISUAL_STYLE | contactVisualStyle | VERIFIED | Blueberry Signal 톤, 폼 가독성과 상태 안내 우선 | config.js, style.css / Blueberry Signal, 사용자 최종 시각 승인 대기 |
| TBD_FOOTER_DISPLAY_NAME | footerDisplayName | VERIFIED | 이준성 &#124; Junseong Lee | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_FOOTER_PERSONAL_MESSAGE | footerPersonalMessage | VERIFIED | 의도적인 미사용(빈 문자열) | config.js, index.html / 정적 대체문구와 동기화 |

## 외부 의존성과 승인

- Formspree: formId 빈값, enabled=false. 공개 이메일·전화번호 미표시. 실제 수신 주소는 서비스에서 사용자가 설정. 실전 발송/수신 확인 BLOCKED.
- GitHub 목표 이름: gareal2117/codyssey-b1-1-personal-portfolio. 공개 조회 404. 현재 로컬 main은 커밋 전, origin 없음, gh 미설치. 공개 목록에 my-portfolio 후보가 있으나 현재 로컬과의 연결은 확인되지 않음.
- 공개 push/배포/계정 생성/실제 발송은 이번 작업에서 실행하지 않음.
- designApproved/publishApproved/emailLiveVerified/pagesVerified는 false이며, 사용자 승인 또는 실제 증거 없이 true로 변경하지 않음.

## 코드 게시 후속 승인

위 외부 의존성 목록은 2차 개발 당시 기록입니다. 이후 사용자가 코드 커밋·일반 push와 기존 포트폴리오 재사용/rename을 승인했습니다. 빈 my-portfolio를 codyssey-b1-1-personal-portfolio로 변경하고 origin을 연결했습니다. release.publishApproved=true는 **코드 게시 승인만** 뜻합니다. pagesApproved=false, pagesVerified=false, pagesUrl=null이며 GitHub Pages는 독립 코드 검토 후 별도 승인 대상입니다. 디자인과 이메일 실전 상태는 변경하지 않았습니다.

## Formspree·Header 후속 변경

사용자가 공개 Form ID `mdeezyjq`의 활성화를 승인하여 enabled=true를 적용했습니다. 비밀키나 수신 이메일은 추가하지 않았습니다. Header는 `JL.`에서 `JL`로 변경하고 색상·크기·폰트·위치·Home 링크는 유지했습니다. 실제 시험 메일은 발송하지 않으며 emailLiveVerified=false를 유지합니다. 기존 Pages의 main / (root) 자동 배포 설정은 변경하지 않습니다. 이번 push의 재배포 결과와 실제 메일 수신은 별도로 확인합니다.

## 2026-10-30 최종 정리

- 사용자가 저장소 공개·push, Pages 접속, Formspree `mdeezyjq` 연결 및 실제 메시지 발송·스팸함 수신을 직접 확인했다고 보고했습니다. `emailLiveVerified=true`, `pagesApproved=true`, 실제 `pagesUrl`을 반영합니다. 수신 주소·메시지 원문은 기록하지 않고 추가 실제 발송도 하지 않습니다.
- 위 과거 절의 빈 ID·메일 미확인·Pages 미승인·미배포는 당시 이력입니다. 최신 배포 검증 결과는 TEST_REPORT에 기록하며 성공한 경우에만 `pagesVerified=true`로 변경합니다.
- 디자인 사용자 최종 승인 기록은 없으므로 `designApproved=false`를 유지합니다. 코드·Pages 배포 승인은 최종 수정 요청으로 재확인했습니다.
- README 마지막 체크박스 11개만 삭제하며 학습 강의노트·요구사항 표·검증 증거는 보존합니다. 체크리스트 삭제는 전체 완료 판정이 아닙니다.
- Hero·프로필 SVG 이니셜을 `JL`로 통일합니다. CSS 및 main.js를 변경하지 않아 크기·위치·색상·애니메이션 정의는 보존합니다.

### 원격 게시 결과

로컬 일반 커밋 `09ee4b2`를 생성했으나 `git push origin main`은 HTTPS 인증 부재로 실패했습니다. 연결된 GitHub 도구는 저장소 메타데이터의 push 권한과 달리 실제 blob 생성에서 403(Resource not accessible by integration)을 반환했습니다. 원격 ref 변경이나 강제 push는 수행하지 않았습니다. Git 인증 복구 후 일반 push와 최신 배포 재검증이 필요하며, 그 전에는 pagesVerified=false를 유지합니다.

### 인증 복구 후 배포 검증 완료 (2026-10-30)

사용자가 VS Code GitHub 로그인을 완료했다고 알린 뒤 일반 push가 성공 응답(Everything up-to-date)했으며 원격 main이 cfafbed까지 반영된 것을 확인했습니다. Pages 실행 41031479626은 success입니다. 실제 배포 5개 자산이 로컬과 일치하고 원격 Chrome 117 PASS / 0 FAIL을 확인한 뒤에만 pagesVerified=true로 변경했습니다. 이전 인증 차단은 과거 시도 이력으로 보존합니다. 디자인 승인 값은 false 유지, 실제 메일 추가 발송 없음입니다.
