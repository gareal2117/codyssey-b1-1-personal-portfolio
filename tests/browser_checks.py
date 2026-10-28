"""표준 라이브러리 + 설치된 Chrome으로 실제 브라우저 QA를 수행합니다.

앱의 실행 의존성이 아닙니다. 임시 Chrome 프로필/로컬 서버는 종료 시 정리합니다.
실제 API 화면을 캡처한 뒤 테스트 페이지에만 fetch 대역을 주입합니다.
"""
import base64
import hashlib
import functools
import http.server
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import urllib.request
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CHROME = os.environ.get('CHROME_BIN', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
RESULTS = []


class CDP:
    """로컬 Chrome DevTools WebSocket의 최소 클라이언트입니다."""
    def __init__(self, url):
        parsed = urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=20)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f'GET {parsed.path} HTTP/1.1\r\nHost: {parsed.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        response = b''
        while not response.endswith(b'\r\n\r\n'):
            response += self.sock.recv(1)
        assert response.split(b'\r\n')[0].split()[1] == b'101', response
        self.counter = 0
        self.exceptions = []
        self.console_errors = []

    def read(self, length):
        data = b''
        while len(data) < length:
            chunk = self.sock.recv(length - len(data))
            if not chunk:
                raise RuntimeError('Chrome 연결이 종료되었습니다.')
            data += chunk
        return data

    def call(self, method, params=None):
        self.counter += 1
        payload = json.dumps({'id': self.counter, 'method': method, 'params': params or {}}).encode()
        mask = os.urandom(4)
        length = len(payload)
        prefix = bytes([0x81, 0x80 | length]) if length < 126 else bytes([0x81, 0xfe]) + struct.pack('!H', length) if length < 65536 else bytes([0x81, 0xff]) + struct.pack('!Q', length)
        self.sock.sendall(prefix + mask + bytes(value ^ mask[index % 4] for index, value in enumerate(payload)))
        message = b''
        while True:
            first, second = self.read(2)
            size = second & 127
            if size == 126:
                size = struct.unpack('!H', self.read(2))[0]
            elif size == 127:
                size = struct.unpack('!Q', self.read(8))[0]
            message += self.read(size)
            if not first & 128:
                continue
            data = json.loads(message)
            message = b''
            if data.get('method') == 'Runtime.exceptionThrown':
                self.exceptions.append(data['params'])
            if data.get('method') == 'Runtime.consoleAPICalled' and data['params']['type'] == 'error':
                self.console_errors.append(data['params'])
            if data.get('id') == self.counter:
                if 'error' in data:
                    raise RuntimeError(data['error'])
                return data.get('result', {})

    def evaluate(self, expression):
        result = self.call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
        if 'exceptionDetails' in result:
            raise RuntimeError(result['exceptionDetails'])
        return result.get('result', {}).get('value')


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.startswith('/codyssey-b1-1-personal-portfolio/'):
            path = path[len('/codyssey-b1-1-personal-portfolio'):]
        return super().translate_path(path)

    def log_message(self, *_args):
        pass


def check(name, condition, detail=''):
    status = 'PASS' if condition else 'FAIL'
    RESULTS.append({'name': name, 'status': status, 'detail': detail})
    print(f'{status}: {name}', flush=True)


def wait_for(browser, expression, seconds=8):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if browser.evaluate(expression):
            return True
        time.sleep(.1)
    return False


def run(browser, base_url):
    browser.call('Page.enable')
    browser.call('Page.bringToFront')
    browser.call('Runtime.enable')
    browser.call('Network.enable')
    browser.call('Network.setBlockedURLs', {'urls': ['*://formspree.io/*']})
    version = browser.call('Browser.getVersion')['product']
    browser.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-color-scheme', 'value': 'light'}]})
    fixture_id = None

    def viewport(width):
        browser.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})

    def load(script=None):
        nonlocal fixture_id
        if fixture_id:
            browser.call('Page.removeScriptToEvaluateOnNewDocument', {'identifier': fixture_id})
            fixture_id = None
        if script:
            fixture_id = browser.call('Page.addScriptToEvaluateOnNewDocument', {'source': script})['identifier']
        browser.call('Page.navigate', {'url': base_url + '/codyssey-b1-1-personal-portfolio/'})
        assert wait_for(browser, "document.readyState === 'complete' && !!document.querySelector('#contact-fields') && !document.querySelector('#contact-fields').disabled")

    def js(expression):
        return browser.evaluate(expression)

    def click(selector):
        js(f'document.querySelector({json.dumps(selector)}).click()')

    def screenshot(name):
        js("window.scrollTo({top:0,behavior:'instant'})")
        time.sleep(.2)
        layout = browser.call('Page.getLayoutMetrics')['cssContentSize']
        data = browser.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True,
            'clip': {'x': 0, 'y': 0, 'width': layout['width'], 'height': layout['height'], 'scale': 1}})['data']
        (ROOT / 'docs/screenshots' / name).write_bytes(base64.b64decode(data))

    viewport(1440)
    load()
    settled = wait_for(browser, "!document.querySelector('#project-grid').getAttribute('aria-busy').includes('true')", 25)
    actual_status = js("document.querySelector('#projects-status').textContent")
    real_ok = settled and js("document.querySelectorAll('.project-card').length > 0 || document.querySelector('#projects-status').textContent.includes('표시할 프로젝트가 없습니다')")
    RESULTS.append({'name': '실제 GitHub API 연결', 'status': 'PASS' if real_ok else 'PARTIAL', 'detail': actual_status})
    wait_for(browser, "!document.querySelector('.typing-visual') || document.querySelector('[data-content=heroGreeting]').classList.contains('typing-complete')")
    screenshot('desktop.png')
    viewport(375)
    screenshot('mobile.png')
    click('#theme-toggle')
    viewport(1440)
    screenshot('dark.png')
    check('실제 화면 스크린샷 3종', all((ROOT / 'docs/screenshots' / name).exists() for name in ['desktop.png', 'mobile.png', 'dark.png']))
    collision = js("fetch('https://api.github.com/repos/gareal2117/codyssey-b1-1-personal-portfolio').then(r => ({status:r.status})).catch(e => ({error:e.message}))")

    # 이후 응답은 테스트 전용입니다. 공개 코드나 제출 스크린샷에 샘플 저장소를 넣지 않습니다.
    fixture = [{'name': 'QA fixture — <img src=x onerror=alert(1)>', 'description': '<script>alert(1)</script>', 'language': 'JavaScript', 'stargazers_count': 7, 'html_url': 'https://github.com/gareal2117/qa-only'},
               {'name': 'null 속성 테스트', 'description': None, 'language': None, 'stargazers_count': None, 'html_url': None},
               {'name': '긴문자열' * 40, 'description': 'LongDescription' * 30, 'language': 'HTML', 'stargazers_count': 0, 'html_url': 'javascript:alert(1)'}]
    success_script = 'window.__calls=0; window.fetch=async () => {window.__calls++; return new Response(' + json.dumps(json.dumps(fixture)) + ', {status:200});};'
    load(success_script)
    check('테마 새로고침 유지', js("document.documentElement.dataset.theme === 'dark'"))
    click('#theme-toggle')
    check('다크 모드 버튼·aria 동기화', js("document.documentElement.dataset.theme === 'light' && document.querySelector('#theme-toggle').getAttribute('aria-pressed') === 'false'"))
    check('API 성공·map 카드·article', js("document.querySelectorAll('article.project-card').length === 3"))
    check('API HTML 삽입 방지·URL 검증', js("document.querySelectorAll('#project-grid script, #project-grid img').length === 0 && document.querySelectorAll('#project-grid a').length === 1 && [...document.querySelectorAll('#project-grid h4')].some(el=>el.textContent.includes('<img'))"))
    check('API null 속성 기본 문구', js("[...document.querySelectorAll('.project-card')].find(el=>el.textContent.includes('null 속성 테스트')).textContent.includes('등록된 설명이 없습니다.') && [...document.querySelectorAll('.project-card')].find(el=>el.textContent.includes('null 속성 테스트')).textContent.includes('언어 미지정')"))
    check('불필요한 API 중복 요청 없음', js('window.__calls === 1'))
    for width in (375, 768, 1024, 1440):
        viewport(width)
        time.sleep(.15)
        check(f'{width}px 가로 넘침 없음', js('document.documentElement.scrollWidth <= innerWidth'))
        check(f'{width}px 카드 Grid·메뉴 전환', js("getComputedStyle(document.querySelector('#project-grid')).display === 'grid' && (innerWidth < 768 ? getComputedStyle(document.querySelector('#menu-toggle')).display !== 'none' && getComputedStyle(document.querySelector('#nav-menu')).display === 'none' : getComputedStyle(document.querySelector('#nav-menu')).display === 'flex' && getComputedStyle(document.querySelector('#menu-toggle')).display === 'none')"))
    viewport(375)
    click('#menu-toggle')
    check('모바일 메뉴 열기', js("document.querySelector('#nav-menu').classList.contains('active') && document.querySelector('#menu-toggle').getAttribute('aria-expanded') === 'true'"))
    click('#menu-toggle')
    check('모바일 메뉴 다시 닫기', js("!document.querySelector('#nav-menu').classList.contains('active')"))
    click('#menu-toggle')
    js("document.querySelector('#menu-toggle').focus()")
    browser.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
    browser.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
    check('Escape 닫기·키보드 초점 복구', js("document.activeElement.id === 'menu-toggle' && document.querySelector('#menu-toggle').getAttribute('aria-expanded') === 'false'"), str(js("({focus:document.activeElement.id, expanded:document.querySelector('#menu-toggle').getAttribute('aria-expanded')})")))
    browser.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13, 'text': '\r', 'unmodifiedText': '\r'})
    browser.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13})
    check('키보드 Enter 메뉴 열기', js("document.querySelector('#nav-menu').classList.contains('active')"))
    click('#nav-menu a[href="#projects"]')
    time.sleep(1)
    check('앵커 이동·메뉴 닫기·헤더 가림 방지', js("document.activeElement.id === 'projects' && !document.querySelector('#nav-menu').classList.contains('active') && document.querySelector('#projects').getBoundingClientRect().top >= document.querySelector('#site-header').getBoundingClientRect().bottom"))
    js("document.querySelector('.project-card').scrollIntoView({block:'center',behavior:'instant'})")
    check('Observer 화면 진입 애니메이션', wait_for(browser, "document.querySelector('.project-card').classList.contains('is-visible')"))
    for y in (59, 60, 299, 300):
        js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        time.sleep(.1)
        check(f'스크롤 기준 {y}px', js(f"document.querySelector('#site-header').classList.contains('scrolled') === {str(y >= 60).lower()} && document.querySelector('#back-to-top').hidden === {str(y < 300).lower()}"))
    click('#back-to-top')
    check('Scroll-to-top 상단 이동', wait_for(browser, 'scrollY === 0'))

    def fill(name, value):
        js(f"(() => {{const el=document.querySelector('#contact-{name}'); el.value={json.dumps(value)}; el.dispatchEvent(new Event('input', {{bubbles:true}}));}})()")

    click('button[type="submit"]')
    check('빈 폼 제출 방지·필드 오류·초점', js("document.querySelectorAll('[aria-invalid=\"true\"]').length === 3 && document.activeElement.id === 'contact-name'"))
    for name in ('name', 'email', 'message'):
        fill(name, '   ')
    click('button[type="submit"]')
    check('공백만 입력 거부', js("document.querySelectorAll('[aria-invalid=\"true\"]').length === 3"))
    fill('email', 'invalid@')
    check('잘못된 이메일 검사', js("document.querySelector('#email-error').textContent.includes('올바른 이메일')"))
    fill('name', 'QA 입력 (실제 개인정보 아님)')
    fill('email', 'qa@example.test')
    fill('message', '<img src=x onerror=alert(1)>')
    check('input 수정 시 오류 갱신', js("document.querySelectorAll('[aria-invalid=\"true\"]').length === 0"))
    click('button[type="submit"]')
    check('정상 입력 검증·미전송 명시', js("document.querySelector('#form-status').dataset.state === 'error' && document.querySelector('#form-status').textContent.includes('전송되지 않았습니다') && window.__calls === 1"))
    fill('message', '수정된 QA 입력')
    check('수정 후 이전 성공 상태 해제', js("document.querySelector('#form-status').textContent === ''"))

    load('window.__calls=0; window.fetch=() => {window.__calls++; return new Promise(resolve => {window.__resolve = resolve;});};')
    check('API Loading UI', js("document.querySelector('#project-grid').getAttribute('aria-busy') === 'true' && document.querySelector('#projects-status').textContent.includes('불러오는 중')"))
    js("window.__resolve(new Response('[]',{status:200}))")
    check('API Empty UI', wait_for(browser, "document.querySelector('#projects-status').textContent === '표시할 프로젝트가 없습니다.'"))
    for code in (403, 429, 500):
        load(f"window.__calls=0; window.fetch=async () => {{window.__calls++; return new Response('{{}}',{{status:{code}}});}};")
        check(f'API HTTP {code} 오류·재시도 표시', js("document.querySelector('#projects-status').textContent.includes('프로젝트를 불러올 수 없습니다.') && !document.querySelector('#projects-retry').hidden"))
        if code in (403, 429):
            check(f'API {code} 제한 안내', js("document.querySelector('#projects-status').textContent.includes('요청 한도 또는 접근 제한')"))
        js("window.fetch=async () => {window.__calls++; return new Response('[]',{status:200});}")
        click('#projects-retry')
        check(f'API {code} 재시도 실제 재호출', wait_for(browser, "window.__calls === 2 && document.querySelector('#projects-status').textContent.includes('표시할 프로젝트가 없습니다')"))
    for name, body in [('네트워크', "throw new TypeError('Failed to fetch')"), ('시간 초과', "throw new DOMException('timeout','AbortError')"), ('객체 응답', "return new Response('{}')"), ('null 응답', "return new Response('null')"), ('null 항목', "return new Response('[null]')"), ('JSON 파싱', "return new Response('broken-json')")]:
        load(f'window.fetch=async () => {{{body};}};')
        check(f'API {name} 오류 처리', js("document.querySelector('#projects-status').textContent.includes('프로젝트를 불러올 수 없습니다.')"))
    load("window.__calls=0; window.fetch=async () => {window.__calls++; return new Response('[{}]', {headers:window.__calls === 1 ? {link:'<https://api.github.com/test?page=2>; rel=\"next\"'} : {}});};")
    check('API 페이지네이션', js("window.__calls === 2 && document.querySelectorAll('.project-card').length === 2"))
    load(success_script + "Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}});")
    click('#theme-toggle')
    check('localStorage 읽기·쓰기 차단 복구', js("document.documentElement.dataset.theme === 'dark' && !document.querySelector('#contact-fields').disabled"))
    load(success_script + 'delete window.IntersectionObserver;')
    check('Observer 미지원 시 콘텐츠 표시', js("getComputedStyle(document.querySelector('.reveal')).visibility === 'visible' && getComputedStyle(document.querySelector('.reveal')).opacity === '1'"))
    browser.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
    load(success_script)
    click('a[href="#projects"]')
    check('reduced-motion 스크롤·애니메이션', js("getComputedStyle(document.documentElement).scrollBehavior === 'auto' && getComputedStyle(document.querySelector('.project-card')).animationName === 'none'"))
    browser.call('Emulation.setEmulatedMedia', {'features': []})
    check('하위 경로 CSS·JS 로딩', js("[...performance.getEntriesByType('resource')].some(r=>r.name.includes('/codyssey-b1-1-personal-portfolio/css/style.css')) && !!window.PortfolioConfig && getComputedStyle(document.querySelector('#project-grid')).display === 'grid'"))
    check('개인화 25항목 승인 값·UI 일치', js("Object.values(window.PortfolioConfig.personal).length === 25 && Object.values(window.PortfolioConfig.personal).every(v=>['APPLIED','VERIFIED'].includes(v.status)) && !document.body.innerText.includes('[미정]')"))
    browser.call('Emulation.setScriptExecutionDisabled', {'value': True})
    browser.call('Page.reload')
    time.sleep(.5)
    check('JavaScript 미지원 정적 콘텐츠·안전한 폼', js("document.querySelectorAll('main section').length === 5 && document.querySelector('#home-title').textContent === '개발자로 성장하고 있는 이준성입니다.' && !/\[[^\]]*미정\]/.test(document.body.innerText) && document.querySelector('#contact-fields').disabled && getComputedStyle(document.querySelector('#nav-menu')).display === 'flex' && getComputedStyle(document.querySelector('.reveal')).visibility === 'visible'"))
    browser.call('Emulation.setScriptExecutionDisabled', {'value': False})
    # 2차 추가 검증: 결정 계약, 이미지, 보너스, 실제 응답과 mock 전송의 경계.
    load(success_script)
    contract = json.loads((ROOT / 'docs/personalization-contract.json').read_text())
    actual = js("window.PortfolioConfig.personal")
    check('25개 ID·값 승인 계약과 정확히 일치', all(actual[k]['id'] == v['id'] and actual[k]['value'] == v['value'] for k, v in contract.items()))
    check('정적·동적 개인화 문구 동기화', js("[...document.querySelectorAll('[data-content]')].every(el=>el.textContent===window.PortfolioConfig.personal[el.dataset.content].value || el.dataset.content==='heroGreeting')"))
    check('프로필 img 실제 로드·alt·SVG 경로', wait_for(browser, "document.querySelector('#profile-image').complete && document.querySelector('#profile-image').naturalWidth === 480 && document.querySelector('#profile-image').alt.includes('모노그램')"))
    check('프로필 표시 비율 보존', js("Math.abs(document.querySelector('#profile-image').getBoundingClientRect().width-document.querySelector('#profile-image').getBoundingClientRect().height)<1"))
    check('Footer GitHub 중복 없음·비공개 연락처', js("document.querySelectorAll('#social-links a').length === 1 && !document.querySelector('a[href^=\"mailto:\"]') && !document.querySelector('a[href^=\"tel:\"]')"))
    check('Hero 실제 타이핑 중간 상태', js("document.querySelector('.typing-visual').textContent.length < window.PortfolioConfig.personal.heroGreeting.value.length"))
    check('Hero 타이핑 완료·정적 접근성 텍스트', wait_for(browser, "document.querySelector('.typing-visual').textContent === '안녕하세요.' && document.querySelector('[data-content=heroGreeting] .sr-only').textContent === '안녕하세요.'"))
    before = js("document.querySelector('[data-content=heroGreeting]').getBoundingClientRect().height")
    time.sleep(2)
    check('타이핑 1회 종료·레이아웃 유지', js("document.querySelector('[data-content=heroGreeting]').classList.contains('typing-complete')") and before == js("document.querySelector('[data-content=heroGreeting]').getBoundingClientRect().height"))
    click('[data-language="JavaScript"]')
    check('언어 필터·건수·API 재호출 없음', js("document.querySelectorAll('#project-grid article').length === 1 && document.querySelector('#filter-status').textContent.includes('1 / 3') && window.__calls === 1"))
    check('필터 선택 후 버튼 초점 유지 준비', js("document.querySelector('[data-language=JavaScript]').getAttribute('aria-pressed') === 'true'"))
    click('[data-language="언어 미지정"]')
    check('null 언어 필터', js("document.querySelectorAll('#project-grid article').length === 1 && document.querySelector('#project-grid').textContent.includes('null 속성 테스트')"))
    js("document.querySelector('[data-language=HTML]').dataset.language='없는언어'")
    click('[data-language="없는언어"]')
    check('필터 0건 메시지', js("document.querySelector('#filter-status').textContent.includes('이 조건에 맞는 저장소가 없습니다') && document.querySelectorAll('#project-grid article').length === 0"))
    click('[data-language="all"]')
    js("document.querySelector('[data-language=JavaScript]').focus()")
    browser.call('Input.dispatchKeyEvent', {'type':'keyDown','key':'Enter','code':'Enter','windowsVirtualKeyCode':13,'text':'\r'})
    browser.call('Input.dispatchKeyEvent', {'type':'keyUp','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
    check('필터 키보드 Enter·초점 보존', js("document.activeElement.dataset.language === 'JavaScript' && document.activeElement.getAttribute('aria-pressed') === 'true'"))
    real_record = next((name, record) for name, record in js('window.PortfolioConfig.github.readmes').items() if record['status'] == 200)
    name, record = real_record
    featured_fixture = [{'name':name, 'description':'QA 학습용', 'language':'Python', 'stargazers_count':0, 'html_url':f'https://github.com/gareal2117/{name}', 'default_branch':record['branch'], 'pushed_at':record['pushedAt']}, {'name':'unfeatured', 'language':'HTML'}]
    def fixture_script(items):
        return 'window.__calls=0;window.fetch=async()=>{window.__calls++;return new Response('+json.dumps(json.dumps(items))+');};'
    load(fixture_script(featured_fixture))
    check('Featured 실제 배열에서만 선별·동적 HTML', js("document.querySelectorAll('#featured-grid article').length === 1 && document.querySelector('#featured-grid .project-index').textContent.includes('01')"))
    check('검증된 README·브랜치만 링크', js("document.querySelectorAll('#project-grid a').length === 2 && [...document.querySelectorAll('#project-grid a')].some(a=>a.textContent.includes('README'))"))
    click('[data-language="HTML"]')
    check('All 필터가 Featured에 영향 없음', js("document.querySelectorAll('#featured-grid article').length === 1 && document.querySelectorAll('#project-grid article').length === 1"))
    featured_fixture[0]['pushed_at'] = 'changed'
    load(fixture_script(featured_fixture))
    check('오래된 README 캐시 숨김', js("![...document.querySelectorAll('.project-links a')].some(a=>a.textContent.includes('README'))"))
    load(success_script)
    check('없는 Featured 유령 카드 없음', js("document.querySelectorAll('#featured-grid article').length === 0 && document.querySelector('#featured-status').textContent.includes('없습니다')"))

    def media(theme, motion='no-preference'):
        browser.call('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-color-scheme','value':theme},{'name':'prefers-reduced-motion','value':motion}]})
    js('localStorage.clear()')
    media('dark')
    load(success_script)
    check('저장값 없으면 시스템 dark', js("document.documentElement.dataset.theme==='dark'"))
    media('light')
    check('수동 선택 없을 때 시스템 변경 반영', wait_for(browser, "document.documentElement.dataset.theme==='light'"))
    click('#theme-toggle')
    media('dark')
    media('light')
    check('수동 선택이 시스템 변경보다 우선', js("document.documentElement.dataset.theme==='dark'"))
    load(success_script)
    check('시스템 light보다 저장된 dark 우선', js("document.documentElement.dataset.theme==='dark'"))
    js('localStorage.clear()')
    load(success_script+"Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}});")
    click('#theme-toggle')
    media('dark')
    media('light')
    check('저장 차단 중 수동 선택 유지', js("document.documentElement.dataset.theme==='dark'"))
    media('light','reduce')
    load(success_script)
    check('reduced-motion 타이핑 생략', js("!document.querySelector('.typing-visual') && document.querySelector('[data-content=heroGreeting]').textContent==='안녕하세요.'"))
    media('light')
    load(success_script)
    js("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
    check('백그라운드 전환 타이핑 종료', js("document.querySelector('[data-content=heroGreeting]').classList.contains('typing-complete')"))

    # Formspree 호스트는 CDP에서 차단되어 있으므로 fixture 실수로도 실제 발송하지 않습니다.
    load(success_script)
    js("window.PortfolioConfig.email.enabled=true;window.PortfolioConfig.email.formId='qatest00';window.__posts=0;")
    def valid_form():
        fill('name','QA 학습용 입력')
        fill('email','qa@example.test')
        fill('message','모의 전송 테스트이며 실제 발송하지 않음')
    valid_form()
    js("window.fetch=(url,options)=>{window.__posts++;window.__body=Object.fromEntries(options.body.entries());return new Promise(resolve=>{window.__postResolve=resolve});}")
    click('button[type="submit"]')
    check('메일 submitting·중복 버튼 비활성', js("document.querySelector('#form-status').dataset.state==='submitting' && document.querySelector('#contact-fields').disabled && window.__posts===1"))
    js("document.querySelector('#contact-form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))")
    check('메일 중복 submit 네트워크 방지', js('window.__posts===1'))
    check('메일 payload·공개 식별자만 사용', js("window.__body.name==='QA 학습용 입력' && Object.keys(window.__body).sort().join(',')==='_gotcha,email,message,name'"))
    js("window.__postResolve(new Response(JSON.stringify({ok:true}),{status:200}))")
    check('메일 mock 성공 후에만 reset', wait_for(browser, "document.querySelector('#form-status').dataset.state==='success' && document.querySelector('#contact-name').value===''"))
    check('접수와 수신함 도착 구분', js("document.querySelector('#form-status').textContent.includes('수신함 도착 여부는 별도')"))
    fill('name','다시 입력')
    check('메일 성공 뒤 수정하면 idle', js("document.querySelector('#form-status').dataset.state==='idle'"))
    for case, body in [('HTTP 422',"return new Response('{}',{status:422})"),('HTTP 429',"return new Response('{}',{status:429})"),('HTTP 500',"return new Response('{}',{status:500})"),('네트워크',"throw new TypeError('offline')"),('서비스 오류',"return new Response(JSON.stringify({errors:[{message:'QA error'}]}))"),('잘못된 JSON',"return new Response('bad')")]:
        valid_form()
        js('window.fetch=async()=>{'+body+';}')
        click('button[type="submit"]')
        check('메일 mock '+case+'·입력 유지', wait_for(browser,"document.querySelector('#form-status').dataset.state==='error' && document.querySelector('#contact-name').value==='QA 학습용 입력' && !document.querySelector('#contact-fields').disabled"))
    valid_form()
    js("window.PortfolioConfig.email.timeoutMs=40;window.fetch=(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('timeout','AbortError'))));")
    click('button[type="submit"]')
    check('메일 실제 타이머 abort·중복 전송 주의', wait_for(browser,"document.querySelector('#form-status').dataset.state==='error' && document.querySelector('#form-status').textContent.includes('중복 전송')"))
    valid_form()
    js("window.__posts=0;window.fetch=async()=>{window.__posts++;return new Response('{\"ok\":true}')};document.querySelector('#contact-website').value='spam'")
    click('button[type="submit"]')
    check('메일 honeypot 차단', js("window.__posts===0 && document.querySelector('#form-status').dataset.state==='error'"))
    js("document.querySelector('#contact-website').value='';window.PortfolioConfig.email.formId='https://invalid.example';")
    click('button[type="submit"]')
    check('잘못된 폼 ID 전송 금지', js("window.__posts===0 && document.querySelector('#form-status').textContent.includes('연동 전')"))
    fill('name','x'*101)
    check('폼 길이 제한 검증', js("document.querySelector('#name-error').textContent.includes('100자')"))

    load(success_script)
    js("localStorage.setItem('portfolio-theme','light')")
    contrast = {}
    def luminance(rgb):
        values=[int(x)/255 for x in __import__('re').findall(r'\d+',rgb)[:3]]
        values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
        return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))
    for theme in ['light','dark']:
        js(f"document.documentElement.dataset.theme='{theme}'")
        colors=js("Object.fromEntries(['text','muted','error','success','accent','on-accent','background','card','soft'].map(key=>{const el=document.createElement('span');el.className='sr-only';el.style.color=getComputedStyle(document.documentElement).getPropertyValue('--color-'+key);document.body.append(el);const value=getComputedStyle(el).color;el.remove();return [key,value]}))")
        ratios=[]
        for fg in ['text','muted','error','success','accent']:
            for bg in ['background','card','soft']:
                a,b=sorted([luminance(colors[fg]),luminance(colors[bg])]);ratios.append((b+.05)/(a+.05))
        a,b=sorted([luminance(colors['accent']),luminance(colors['on-accent'])]);ratios.append((b+.05)/(a+.05))
        contrast[theme]=round(min(ratios),2)
        check(theme+' 일반 텍스트 대비 4.5:1', min(ratios)>=4.5, str(contrast[theme]))
        for width in [375,768,1024,1440]:
            viewport(width)
            check(theme+f' {width}px overflow 없음', js('document.documentElement.scrollWidth<=innerWidth'))
    time.sleep(30)
    check('30초 렌더 유지 후 필터·폼·타이핑 안정', js("document.querySelectorAll('#project-grid article').length===3 && !document.querySelector('#contact-fields').disabled && document.querySelector('[data-content=heroGreeting]').classList.contains('typing-complete')"))
    check('미처리 JavaScript 예외·console.error 없음', not browser.exceptions and not browser.console_errors, json.dumps(browser.exceptions + browser.console_errors, ensure_ascii=False))
    return {'phase': 2, 'sourceHashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['index.html','css/style.css','js/config.js','js/main.js','images/profile-monogram.svg']}, 'contrast': contrast, 'email_live': 'BLOCKED: no configured service; all email tests mocked and external endpoint blocked', 'pages_live': 'BLOCKED: not deployed', 'browser': version, 'actual_api': actual_status, 'repository_name_check': collision, 'results': RESULTS}


def main():
    (ROOT / 'docs/screenshots').mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory(prefix='codyssey-chrome-') as profile:
        process = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--remote-debugging-port=0', f'--user-data-dir={profile}', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        browser = None
        try:
            port_file = Path(profile) / 'DevToolsActivePort'
            for _ in range(100):
                if port_file.exists():
                    break
                if process.poll() is not None:
                    raise RuntimeError(f'Chrome 종료 코드: {process.returncode}')
                time.sleep(.1)
            port = int(port_file.read_text().splitlines()[0])
            pages = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json'))
            browser = CDP(next(page for page in pages if page['type'] == 'page')['webSocketDebuggerUrl'])
            report = run(browser, f'http://127.0.0.1:{server.server_port}')
            (ROOT / 'docs/browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps({'browser': report['browser'], 'actual_api': report['actual_api'], 'repository_name_check': report['repository_name_check'], 'pass': sum(r['status'] == 'PASS' for r in RESULTS), 'fail': sum(r['status'] == 'FAIL' for r in RESULTS)}, ensure_ascii=False), flush=True)
        finally:
            if browser:
                browser.sock.close()
            process.terminate()
            process.wait(timeout=10)
            server.shutdown()
    if any(result['status'] == 'FAIL' for result in RESULTS):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
