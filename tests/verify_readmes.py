"""읽기 전용 GitHub 검사. 실행할 때만 README 메타데이터 캐시를 갱신합니다.
앱 방문마다 저장소별 요청을 하지 않습니다. 토큰/로그인/원격 변경 없음.
"""
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def get(url):
    try:
        with urlopen(Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'codyssey-readonly-verification'}), timeout=20) as response:
            return response.status, json.load(response), response.headers.get('link', '')
    except HTTPError as error:
        if error.code == 404:
            return 404, None, ''
        raise


def main():
    config_path = ROOT / 'js/config.js'
    source = config_path.read_text()
    match = re.search(r'window.PortfolioConfig = (\{.*\});', source, re.S)
    config = json.loads(match.group(1))
    repos, page = [], 1
    while True:
        _, data, link = get(config['github']['endpoint'] + f'?per_page=100&page={page}')
        repos.extend(data)
        if 'rel="next"' not in link:
            break
        page += 1
    verified = {}
    checked = datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
    for repo in repos:
        name, branch = repo['name'], repo['default_branch']
        status, readme, _ = get(f'https://api.github.com/repos/gareal2117/{quote(name, safe="")}/readme?ref={quote(branch, safe="")}')
        record = {'status': status, 'branch': branch, 'pushedAt': repo['pushed_at'], 'checkedAt': checked}
        if status == 200:
            url = urlparse(readme['html_url'])
            expected = f'/gareal2117/{name}/blob/'
            assert url.scheme == 'https' and url.netloc == 'github.com' and url.path.startswith(expected)
            record.update({'path': readme['path'], 'url': readme['html_url'], 'sha': readme['sha']})
        verified[name] = record
        print(name, status, record.get('path', 'README 없음'))
    target = config['release']['repositoryName']
    status, repo, _ = get(f'https://api.github.com/repos/gareal2117/{target}')
    report = {'checkedAt': checked, 'targetRepository': {'name': target, 'status': status, 'url': repo['html_url'] if repo else None}, 'repositories': verified}
    config['github']['readmes'] = verified
    config['release']['repositoryUrl'] = repo['html_url'] if repo else None
    config_path.write_text(source[:match.start(1)] + json.dumps(config, ensure_ascii=False, indent=2) + source[match.end(1):])
    (ROOT / 'docs/readme-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('목표 저장소 공개 조회:', status)


if __name__ == '__main__':
    main()
