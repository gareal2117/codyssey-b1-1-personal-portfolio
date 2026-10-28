"""--local은 로컬 검증, 기본 실행은 이메일/배포/승인까지 검사합니다.
종료 코드: 0=해당 범위 통과, 1=로컬 결함, 2=외부 검증/승인 BLOCKED.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--local', action='store_true')
args = parser.parse_args()
config = json.loads(re.search(r'window.PortfolioConfig = (\{.*\});', (root/'js/config.js').read_text(), re.S).group(1))
errors = []
for key, record in config['personal'].items():
    if record['status'] != 'VERIFIED': errors.append(f'{key}: 적용 후 검증 필요')
if re.search(r'\[[^\]]*미정\]', (root/'index.html').read_text()): errors.append('정적 HTML 미정 문구')
report = json.loads((root/'docs/browser-results.json').read_text())
if report.get('phase') != 2 or any(r['status'] != 'PASS' for r in report['results']): errors.append('새 브라우저 검사 미통과')
for name in ['index.html','css/style.css','js/config.js','js/main.js','images/profile-monogram.svg']:
    digest = hashlib.sha256((root/name).read_bytes()).hexdigest()
    if report.get('sourceHashes', {}).get(name) != digest: errors.append(f'검사 이후 소스 변경: {name}')
for name in ['desktop.png','mobile.png','dark.png']:
    path = root/'docs/screenshots'/name
    if not path.exists() or path.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n': errors.append(f'실제 PNG 없음: {name}')
for name in ['README.md','DECISIONS.md','TEST_REPORT.md','docs/REQUIREMENTS_MATRIX.md','docs/EMAIL_SETUP.md']:
    if not (root/name).is_file(): errors.append(f'문서 없음: {name}')
if errors:
    print('FAIL: 로컬 준비 검사\n'+'\n'.join(errors));sys.exit(1)
print('PASS: 로컬 개인화·소스 해시·브라우저 결과·캡처·문서')
if args.local: sys.exit(0)
release = config['release']
blocked = []
if not config['email']['enabled'] or not config['email']['formId'] or not release['emailLiveVerified']: blocked.append('EMAIL_LIVE_VERIFIED: 서비스 설정 및 실제 발송/수신 확인')
if not release['repositoryUrl']: blocked.append('실제 목표 GitHub 저장소 확인 및 연결')
if not release['pagesUrl'] or not release['pagesVerified']: blocked.append('GITHUB_PAGES_VERIFIED: 실제 배포 URL과 동작 확인')
if not release['designApproved']: blocked.append('디자인 사용자 시각 검토')
if not release['publishApproved']: blocked.append('공개 게시 승인')
if blocked:
    print('BLOCKED: 전체 제출 준비\n'+'\n'.join(blocked));sys.exit(2)
print('PASS: 기록상 전체 제출 조건 충족. 승인·실전 증거의 진위는 TEST_REPORT와 대조하세요.')
