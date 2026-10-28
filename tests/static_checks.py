"""빌드 도구 없이 구조·경로·금지 패턴·TBD 구성을 점검합니다."""
from html.parser import HTMLParser
from pathlib import Path
import re
import json
from html import unescape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.anchors, self.labels, self.inputs = [], [], [], []
        self.tags, self.errors = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.add(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in attrs:
            if key == 'style' or key.startswith('on'):
                self.errors.append(f'금지 속성: {key}')
        if tag == 'script' and 'defer' not in attrs:
            self.errors.append('defer 누락')
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag == 'label':
            self.labels.append(attrs.get('for'))
        if tag in ('input', 'textarea'):
            self.inputs.append(attrs.get('id'))
        if tag == 'img' and not attrs.get('alt'):
            self.errors.append('alt 누락')
        if attrs.get('target') == '_blank' and not {'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()):
            self.errors.append('안전한 rel 누락')
        for key in ('src', 'href'):
            value = attrs.get(key, '')
            if value.startswith('./') and not (ROOT / value).is_file():
                self.errors.append(f'파일 경로 없음: {value}')


audit = Audit()
audit.feed((ROOT / 'index.html').read_text())
assert not audit.errors, audit.errors
assert len(audit.ids) == len(set(audit.ids)), '중복 id'
assert set(audit.anchors) <= set(audit.ids), '앵커 대상 누락'
assert set(audit.inputs) <= set(audit.labels), 'label 누락'
assert {'header', 'nav', 'main', 'section', 'footer'} <= audit.tags
assert {'home', 'about', 'skills', 'projects', 'contact'} <= set(audit.ids)
js = (ROOT / 'js/main.js').read_text()
css = (ROOT / 'css/style.css').read_text()
assert not re.search(r'\bvar\s+\w+', js)
for token in ['querySelector', 'querySelectorAll', 'textContent', 'innerHTML', 'classList.add', 'classList.remove', 'classList.toggle', '.map(', '.forEach(', 'async ', 'await ', 'try {', "'click'", "'submit'", "'scroll'", "'input'", 'threshold: 0.2', 'response.ok']:
    assert token in js, token
for token in ['auto-fit', 'minmax(', 'min-width: 768px', 'min-width: 1024px', '[data-theme="dark"]', 'prefers-reduced-motion', ':focus-visible']:
    assert token in css, token
assert 'article.innerHTML = `${featured ?' in js, '안전한 동적 골격 검토 필요'
assert '${description}' not in js and '${htmlUrl}' not in js, '외부 데이터 HTML 보간 금지'
assert 'createElement(\'article\')' in js
config = (ROOT / 'js/config.js').read_text()
data = json.loads(re.search(r'window.PortfolioConfig = (\{.*\});', config, re.S).group(1))
contract = json.loads((ROOT / 'docs/personalization-contract.json').read_text())
records = data['personal']
ids = [record['id'] for record in records.values()]
assert len(ids) == 25 and len(set(ids)) == 25
assert set(records) == set(contract)
decisions = (ROOT / 'DECISIONS.md').read_text()
for key, record in records.items():
    assert record['id'] == contract[key]['id'] and record['value'] == contract[key]['value'], key
    assert record['status'] in ('APPLIED', 'VERIFIED'), key
    row = next(line for line in decisions.splitlines() if line.startswith('| ' + record['id'] + ' |'))
    assert f"| {key} | {record['status']} |" in row, key
assert not re.search(r'\[[^\]]*미정\]', (ROOT / 'index.html').read_text())
html = (ROOT / 'index.html').read_text()
for match in re.finditer(r'data-content="([^"]+)">([^<]*)<', html):
    key, text = match.groups()
    assert ' '.join(unescape(text).split()) == ' '.join(records[key]['value'].split()), f'정적 대체문구 불일치: {key}'
app_source = '\n'.join((ROOT/name).read_text() for name in ['index.html','js/config.js','js/main.js'])
assert not re.search(r'(?:ghp_|github_pat_|sk-proj-|AKIA)[A-Za-z0-9_-]{12,}', app_source), '비밀키 형태'
assert not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', app_source), '공개 이메일 문자열'
assert data['email']['enabled'] is False and data['email']['formId'] == '', '실전 설정 변경 시 별도 승인/검증 필요'
svg = ET.parse(ROOT / records['profileImage']['value']['src']).getroot()
for element in svg.iter():
    assert element.tag.split('}')[-1] not in ('script', 'foreignObject', 'image', 'use')
    assert not any(k.lower().startswith('on') or 'href' in k for k in element.attrib)
assert '.filter(' in js and "prefers-color-scheme: dark" in js and 'setupTyping' in js and 'https://formspree.io/f/' in js
print('PASS: HTML 구조/앵커/label/defer/파일 경로/금지 속성/외부 링크')
print('PASS: 필수 JS 문법·API, CSS 반응형·테마·접근성 패턴')
print(f'PASS: 개인화 {len(ids)}개 ID·승인 값·결정 상태·안전한 SVG 일치')
print('주의: 정적 검사는 브라우저 동작 검증을 대체하지 않습니다.')
