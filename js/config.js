/* 사용자 확정값 25개. APPLIED는 코드 적용, VERIFIED는 동작 검증을 뜻합니다.
 * 디자인의 사용자 최종 승인과 외부 배포/메일 검증은 release에서 별도로 관리합니다.
 * formId는 공개용 식별자만 입력합니다. 비밀키·수신 이메일을 넣지 마세요.
 */
(() => {
  'use strict';
  window.PortfolioConfig = {
  "github": {
    "username": "gareal2117",
    "endpoint": "https://api.github.com/users/gareal2117/repos",
    "featured": [
      "codyssey-mission01-docker-workstation",
      "codyssey-mission02-python-quiz-game",
      "codyssey-mission03-mini-npu-simulator"
    ],
    "readmes": {
      "codyssey-mission01-docker-workstation": {
        "status": 200,
        "branch": "main",
        "pushedAt": "2026-08-17T21:53:40Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00",
        "path": "README.md",
        "url": "https://github.com/gareal2117/codyssey-mission01-docker-workstation/blob/main/README.md",
        "sha": "590081b1bead20c5b2ce972f9849558154247243"
      },
      "codyssey-mission02-python-quiz-game": {
        "status": 200,
        "branch": "main",
        "pushedAt": "2026-08-17T22:40:57Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00",
        "path": "README.md",
        "url": "https://github.com/gareal2117/codyssey-mission02-python-quiz-game/blob/main/README.md",
        "sha": "d25f8a60a9107114f8c589aa23001a8a1c9e430f"
      },
      "codyssey-mission03-mini-npu-simulator": {
        "status": 200,
        "branch": "main",
        "pushedAt": "2026-08-17T22:20:53Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00",
        "path": "README.md",
        "url": "https://github.com/gareal2117/codyssey-mission03-mini-npu-simulator/blob/main/README.md",
        "sha": "e0021aec225bc4241622d5044742d19e2031d435"
      },
      "fastapi-course-records": {
        "status": 404,
        "branch": "main",
        "pushedAt": "2026-06-03T07:44:31Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00"
      },
      "find-your-vibe": {
        "status": 404,
        "branch": "main",
        "pushedAt": "2026-06-17T11:08:36Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00"
      },
      "kw-open-source-software-exercise1": {
        "status": 200,
        "branch": "main",
        "pushedAt": "2026-03-26T16:19:51Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00",
        "path": "README.md",
        "url": "https://github.com/gareal2117/kw-open-source-software-exercise1/blob/main/README.md",
        "sha": "e51433147d0dc8026f1e246f4de6b749a45334ca"
      },
      "music-genre-quiz": {
        "status": 200,
        "branch": "main",
        "pushedAt": "2026-04-27T11:58:47Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00",
        "path": "README.md",
        "url": "https://github.com/gareal2117/music-genre-quiz/blob/main/README.md",
        "sha": "412e60282aef54bf163b7e32f662eb253dc28052"
      },
      "my-portfolio": {
        "status": 404,
        "branch": "main",
        "pushedAt": "2026-10-28T12:25:28Z",
        "checkedAt": "2026-10-28T22:05:35.457516+09:00"
      }
    }
  },
  "email": {
    "provider": "formspree",
    "formId": "mdeezyjq",
    "enabled": true,
    "timeoutMs": 15000
  },
  "release": {
    "repositoryName": "codyssey-b1-1-personal-portfolio",
    "repositoryUrl": "https://github.com/gareal2117/codyssey-b1-1-personal-portfolio",
    "pagesUrl": null,
    "designApproved": false,
    "publishApproved": true,
    "pagesApproved": false,
    "emailLiveVerified": false,
    "pagesVerified": false
  },
  "personal": {
    "displayName": {
      "id": "TBD_DISPLAY_NAME",
      "status": "VERIFIED",
      "value": "이준성 | Junseong Lee"
    },
    "personalBackground": {
      "id": "TBD_PERSONAL_BACKGROUND",
      "status": "VERIFIED",
      "value": "광운대학교 정보융합학부 재학, 코디세이 AI 올인원 과정 학습"
    },
    "introductionDirection": {
      "id": "TBD_INTRODUCTION_DIRECTION",
      "status": "VERIFIED",
      "value": "개발자 포트폴리오/개인 브랜딩, 개발 중심·음악 취미 간단히"
    },
    "interests": {
      "id": "TBD_INTERESTS",
      "status": "VERIFIED",
      "value": "프로그래밍과 다양한 개발 기술"
    },
    "activities": {
      "id": "TBD_ACTIVITIES",
      "status": "VERIFIED",
      "value": "코디세이 과제 학습·수행, 취미로 다양한 음악 활동"
    },
    "designConcept": {
      "id": "TBD_DESIGN_CONCEPT",
      "status": "VERIFIED",
      "value": "Blueberry Signal"
    },
    "designPreferences": {
      "id": "TBD_DESIGN_PREFERENCES",
      "status": "VERIFIED",
      "value": "Blueberry Burst 네이비/블루/스카이블루, 비대칭 타이포 중심, 주요 이름 정자체"
    },
    "personalContent": {
      "id": "TBD_PERSONAL_CONTENT",
      "status": "VERIFIED",
      "value": ""
    },
    "publicContact": {
      "id": "TBD_PUBLIC_CONTACT",
      "status": "VERIFIED",
      "value": "이메일과 전화번호는 공개하지 않습니다."
    },
    "socialLinks": {
      "id": "TBD_SOCIAL_LINKS",
      "status": "VERIFIED",
      "value": [
        {
          "label": "GitHub",
          "url": "https://github.com/gareal2117"
        }
      ]
    },
    "profileImage": {
      "id": "TBD_PROFILE_IMAGE",
      "status": "VERIFIED",
      "value": {
        "src": "./images/profile-monogram.svg",
        "alt": "이준성의 영문 이니셜 JL을 표현한 파란색 프로필 모노그램 그래픽"
      }
    },
    "logoContent": {
      "id": "TBD_LOGO_CONTENT",
      "status": "VERIFIED",
      "value": "JL"
    },
    "heroGreeting": {
      "id": "TBD_HERO_GREETING",
      "status": "VERIFIED",
      "value": "안녕하세요."
    },
    "heroHeadline": {
      "id": "TBD_HERO_HEADLINE",
      "status": "VERIFIED",
      "value": "개발자로 성장하고 있는 이준성입니다."
    },
    "heroDescription": {
      "id": "TBD_HERO_DESCRIPTION",
      "status": "VERIFIED",
      "value": "새로운 기술을 배우고 직접 구현하며, 개발 역량을 쌓아가고 있습니다."
    },
    "heroPersonalVisual": {
      "id": "TBD_HERO_PERSONAL_VISUAL",
      "status": "VERIFIED",
      "value": "블루베리 시그널 추상 CSS 그래픽"
    },
    "aboutIntroduction": {
      "id": "TBD_ABOUT_INTRODUCTION",
      "status": "VERIFIED",
      "value": "광운대학교 정보융합학부에 재학 중이며, 코디세이 AI 올인원 과정에서 다양한 과제를 수행하며 소프트웨어 개발을 공부하고 있습니다.\n프로그래밍과 다양한 개발 기술에 관심을 가지고 있습니다.\n개발 외에는 다양한 음악 활동을 즐기는 것이 취미입니다."
    },
    "skillList": {
      "id": "TBD_SKILL_LIST",
      "status": "VERIFIED",
      "value": [
        "Python",
        "Git",
        "GitHub",
        "Docker"
      ]
    },
    "skillCategories": {
      "id": "TBD_SKILL_CATEGORIES",
      "status": "VERIFIED",
      "value": {
        "Python": "Programming",
        "Git": "Version Control",
        "GitHub": "Repository Hosting",
        "Docker": "Development Environment"
      }
    },
    "skillDescriptions": {
      "id": "TBD_SKILL_DESCRIPTIONS",
      "status": "VERIFIED",
      "value": {
        "Python": "기초 프로그래밍 및 과제 구현",
        "Git": "버전 관리 및 브랜치 실습(merge·충돌 해결 경험)",
        "GitHub": "저장소 생성 및 코드 관리",
        "Docker": "컨테이너 및 개발환경 구성 실습"
      }
    },
    "projectPresentationPreference": {
      "id": "TBD_PROJECT_PRESENTATION_PREFERENCE",
      "status": "VERIFIED",
      "value": "Featured 3개 + All Repositories + GitHub 및 실존 README 링크"
    },
    "contactIntroText": {
      "id": "TBD_CONTACT_INTRO_TEXT",
      "status": "VERIFIED",
      "value": "아래 폼으로 문의를 남길 수 있습니다. 개인 이메일 주소는 공개하지 않습니다."
    },
    "contactVisualStyle": {
      "id": "TBD_CONTACT_VISUAL_STYLE",
      "status": "VERIFIED",
      "value": "Blueberry Signal 톤, 폼 가독성과 상태 안내 우선"
    },
    "footerDisplayName": {
      "id": "TBD_FOOTER_DISPLAY_NAME",
      "status": "VERIFIED",
      "value": "이준성 | Junseong Lee"
    },
    "footerPersonalMessage": {
      "id": "TBD_FOOTER_PERSONAL_MESSAGE",
      "status": "VERIFIED",
      "value": ""
    }
  }
};
})();
