# 개인화 결정 기록 — 2차

사용자가 실행하도록 지정한 2차 프롬프트의 25개 키/값을 적용했습니다. 1차 TBD 기록은 docs/history/phase1/DECISIONS.md에 보존했습니다.

25개 항목은 CONFIRMED(사용자 2차 프롬프트) → APPLIED(코드 적용) → VERIFIED(새 Chrome·승인 계약 검사)로 진행했습니다. VERIFIED는 로컬 적용 검증입니다. 디자인 동작 검증은 사용자의 시각적 최종 승인과 다르며, `release.designApproved`는 false입니다. 이메일 실전 발송·공개 게시도 별도입니다.

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
| TBD_LOGO_CONTENT | logoContent | VERIFIED | JL. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_GREETING | heroGreeting | VERIFIED | 안녕하세요. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_HEADLINE | heroHeadline | VERIFIED | 개발자로 성장하고 있는 이준성입니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_DESCRIPTION | heroDescription | VERIFIED | 새로운 기술을 배우고 직접 구현하며, 개발 역량을 쌓아가고 있습니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_HERO_PERSONAL_VISUAL | heroPersonalVisual | VERIFIED | 블루베리 시그널 추상 CSS 그래픽 | config.js, style.css / Blueberry Signal, 사용자 최종 시각 승인 대기 |
| TBD_ABOUT_INTRODUCTION | aboutIntroduction | VERIFIED | 광운대학교 정보융합학부에 재학 중이며, 코디세이 AI 올인원 과정에서 다양한 과제를 수행하며 소프트웨어 개발을 공부하고 있습니다. / 프로그래밍과 다양한 개발 기술에 관심을 가지고 있습니다. / 개발 외에는 다양한 음악 활동을 즐기는 것이 취미입니다. | config.js, index.html / 정적 대체문구와 동기화 |
| TBD_SKILL_LIST | skillList | VERIFIED | ["Python", "Git", "GitHub", "Docker"] | config.js / renderPersonalContent, #skills-list |
| TBD_SKILL_CATEGORIES | skillCategories | VERIFIED | {"Python": "Programming", "Git": "Version Control", "GitHub": "Repository Hosting", "Docker": "Development Environment"} | config.js / renderPersonalContent, #skills-list |
| TBD_SKILL_DESCRIPTIONS | skillDescriptions | VERIFIED | {"Python": "기초 프로그래밍 및 과제 구현", "Git": "버전 관리 및 브랜치 실습(merge·충돌 해결 경험)", "GitHub": "저장소 생성 및 코드 관리", "Docker": "컨테이너 및 개발환경 구성 실습"} | config.js / renderPersonalContent, #skills-list |
| TBD_PROJECT_PRESENTATION_PREFERENCE | projectPresentationPreference | VERIFIED | Featured 3개 + All Repositories + GitHub 및 실존 README 링크 | config.js, main.js / Featured·All·README 캐시 |
| TBD_CONTACT_INTRO_TEXT | contactIntroText | VERIFIED | 문의 전송 서비스 연동 전입니다. 현재는 입력 검증만 가능하며 메시지는 전송되지 않습니다. | config.js, index.html / 정적 대체문구와 동기화 |
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
