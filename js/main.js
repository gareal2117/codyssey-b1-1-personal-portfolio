(() => {
  'use strict';
  const { github, personal, email } = window.PortfolioConfig;
  const select = (selector) => document.querySelector(selector);
  const root = document.documentElement;
  const themeButton = select('#theme-toggle');
  const menuButton = select('#menu-toggle');
  const menu = select('#nav-menu');
  const header = select('#site-header');
  const topButton = select('#back-to-top');
  const projectGrid = select('#project-grid');
  const projectStatus = select('#projects-status');
  const featuredGrid = select('#featured-grid');
  const filters = select('#language-filters');
  const retryButton = select('#projects-retry');
  const form = select('#contact-form');
  const formStatus = select('#form-status');
  const fieldNames = ['name', 'email', 'message'];
  const fields = Object.fromEntries(fieldNames.map((name) => [name, form.elements.namedItem(name)]));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = window.matchMedia('(min-width: 768px)');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const state = {
    theme: 'light',
    manualTheme: false,
    menuOpen: false,
    projects: { status: 'idle', items: [], error: '', language: 'all' },
    form: { status: 'idle', values: { name: '', email: '', message: '' }, errors: {}, message: '' }
  };

  // 설정값도 외부 입력으로 취급하고, 문자열은 항상 textContent로 표시합니다.
  const resolved = (entry) => entry && ['CONFIRMED', 'APPLIED', 'VERIFIED'].includes(entry.status) && entry.value !== null;
  const contentText = (entry) => resolved(entry) && typeof entry.value === 'string' ? entry.value : entry.placeholder;
  const safeHttpsUrl = (value) => {
    try {
      const url = new URL(value);
      return url.protocol === 'https:' && !url.username && !url.password ? url : null;
    } catch { return null; }
  };
  const externalLink = (label, url) => {
    const link = document.createElement('a');
    link.textContent = label;
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    const hint = document.createElement('span');
    hint.className = 'sr-only';
    hint.textContent = ' (새 창)';
    link.append(hint);
    return link;
  };

  const renderPersonalContent = () => {
    document.querySelectorAll('[data-content]').forEach((element) => {
      element.textContent = contentText(personal[element.dataset.content]);
    });
    document.title = `${personal.displayName.value} · 포트폴리오`;
    select('#copyright-year').textContent = String(new Date().getFullYear());
    // SVG는 직접 작성하고 검사한 이 로컬 파일 하나만 허용합니다.
    const { src, alt } = personal.profileImage.value;
    const image = select('#profile-image');
    const localRaster = /^\.\/images\/[a-zA-Z0-9_-]+\.(webp|png|jpe?g|avif)$/i.test(src);
    if ((localRaster || src === './images/profile-monogram.svg') && typeof alt === 'string' && alt.trim()) {
      image.src = src;
      image.alt = alt;
    }
    image.addEventListener('error', () => { image.hidden = true; select('#profile-fallback').hidden = false; });
    const cards = personal.skillList.value.map((name) => {
      const item = document.createElement('li');
      item.className = 'skill-card';
      const category = document.createElement('p');
      category.className = 'skill-category';
      category.textContent = personal.skillCategories.value[name];
      const title = document.createElement('h3');
      title.textContent = name;
      const description = document.createElement('p');
      description.textContent = personal.skillDescriptions.value[name];
      item.append(category, title, description);
      return item;
    });
    select('#skills-list').replaceChildren(...cards);
    const socialContainer = select('#social-links');
    socialContainer.replaceChildren();
    const usedUrls = new Set();
    personal.socialLinks.value.forEach(({ label, url }) => {
      const safeUrl = safeHttpsUrl(url);
      if (safeUrl && !usedUrls.has(safeUrl.href)) {
        usedUrls.add(safeUrl.href);
        socialContainer.append(externalLink(`${label} ↗`, safeUrl.href));
      }
    });
  };

  const setupTyping = () => {
    const greeting = select('[data-content="heroGreeting"]');
    const text = greeting.textContent;
    if (reducedMotion.matches || document.hidden) return;
    const accessible = document.createElement('span');
    accessible.className = 'sr-only';
    accessible.textContent = text;
    const frame = document.createElement('span');
    frame.className = 'typing-frame';
    frame.setAttribute('aria-hidden', 'true');
    const reserve = document.createElement('span');
    reserve.className = 'typing-reserve';
    reserve.textContent = text;
    const visual = document.createElement('span');
    visual.className = 'typing-visual';
    frame.append(reserve, visual);
    greeting.replaceChildren(accessible, frame);
    let index = 0;
    let timer;
    const finish = () => {
      window.clearTimeout(timer);
      visual.textContent = text;
      greeting.classList.add('typing-complete');
      document.removeEventListener('visibilitychange', onVisibility);
      reducedMotion.removeEventListener('change', finish);
    };
    const onVisibility = () => { if (document.hidden) finish(); };
    const typeNext = () => {
      index += 1;
      visual.textContent = text.slice(0, index);
      if (index < text.length) timer = window.setTimeout(typeNext, 120);
      else finish();
    };
    document.addEventListener('visibilitychange', onVisibility);
    reducedMotion.addEventListener('change', finish);
    timer = window.setTimeout(typeNext, 180);
  };

  const renderTheme = () => {
    root.dataset.theme = state.theme;
    const isDark = state.theme === 'dark';
    themeButton.setAttribute('aria-pressed', String(isDark));
    themeButton.textContent = isDark ? '라이트 모드' : '다크 모드';
    themeButton.setAttribute('aria-label', isDark ? '라이트 모드로 전환' : '다크 모드로 전환');
  };
  const setTheme = (theme) => {
    state.theme = theme;
    state.manualTheme = true;
    try { window.localStorage.setItem('portfolio-theme', theme); } catch {
      // 저장이 차단되어도 현재 화면의 테마는 정상 전환합니다.
    }
    renderTheme();
  };
  const initializeTheme = () => {
    let stored = null;
    try { stored = window.localStorage.getItem('portfolio-theme'); } catch { /* 시스템 설정으로 진행합니다. */ }
    state.manualTheme = stored === 'dark' || stored === 'light';
    state.theme = state.manualTheme ? stored : systemTheme.matches ? 'dark' : 'light';
    renderTheme();
  };
  initializeTheme();
  systemTheme.addEventListener('change', (event) => {
    if (!state.manualTheme) { state.theme = event.matches ? 'dark' : 'light'; renderTheme(); }
  });
  themeButton.hidden = false;
  themeButton.addEventListener('click', () => setTheme(state.theme === 'light' ? 'dark' : 'light'));

  const renderMenu = () => {
    menu.classList.toggle('active', state.menuOpen);
    menuButton.setAttribute('aria-expanded', String(state.menuOpen));
  };
  const closeMenu = () => { state.menuOpen = false; renderMenu(); };
  root.classList.add('js-menu');
  menuButton.hidden = false;
  menuButton.addEventListener('click', () => { state.menuOpen = !state.menuOpen; renderMenu(); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && state.menuOpen) { closeMenu(); menuButton.focus(); }
  });
  document.addEventListener('click', (event) => {
    if (state.menuOpen && !header.contains(event.target)) closeMenu();
  });
  header.addEventListener('focusout', (event) => {
    if (state.menuOpen && !header.contains(event.relatedTarget)) closeMenu();
  });
  desktop.addEventListener('change', () => {
    if (!desktop.matches && menu.contains(document.activeElement)) menuButton.focus();
    closeMenu();
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.getElementById(link.getAttribute('href').slice(1));
      if (!target) return;
      event.preventDefault();
      closeMenu();
      target.focus({ preventScroll: true });
      target.scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'start' });
      // replaceState는 페이지 이동 없이 현재 섹션을 주소에 반영합니다.
      window.history.replaceState(null, '', link.getAttribute('href'));
    });
  });
  topButton.addEventListener('click', () => {
    select('#home').focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
  });
  let scrollScheduled = false;
  const renderScroll = () => {
    if (window.scrollY >= 60) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
    topButton.hidden = window.scrollY < 300;
    scrollScheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scrollScheduled) { scrollScheduled = true; window.requestAnimationFrame(renderScroll); }
  }, { passive: true });
  renderScroll();

  let observer = null;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.2) {
          if (!reducedMotion.matches) entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
  }

  const getReadmeUrl = (repo) => {
    const record = github.readmes[repo.name];
    // 검증 당시 이후 커밋/기본 브랜치가 바뀌면 불확실한 링크는 표시하지 않습니다.
    if (!record || record.status !== 200 || record.branch !== repo.default_branch || record.pushedAt !== repo.pushed_at) return null;
    const url = safeHttpsUrl(record.url);
    const prefix = `/${github.username}/${repo.name}/blob/`;
    return url && url.hostname === 'github.com' && !url.port && url.pathname.startsWith(prefix) ? url.href : null;
  };
  const languageOf = (repo) => typeof repo.language === 'string' && repo.language.trim() ? repo.language : '언어 미지정';
  const makeProjectCard = (repo, featured = false, index = 0) => {
    const article = document.createElement('article');
    article.className = 'project-card reveal';
    // 템플릿 리터럴의 동적 HTML: 신뢰 가능한 고정 태그와 내부 숫자만 삽입합니다.
    // 외부 API 문자열은 이 HTML에 보간하지 않고 아래에서 textContent로 넣습니다.
    article.innerHTML = `${featured ? `<span class="project-index">CODYSSEY / ${String(index + 1).padStart(2, '0')}</span>` : ''}
      <h4></h4><p class="project-description"></p>
      <div class="project-meta"><span class="project-language"></span><span class="project-stars"></span></div>
      <div class="project-links"></div>`;
    const { name, description, stargazers_count: stars, html_url: htmlUrl } = repo;
    article.querySelector('h4').textContent = typeof name === 'string' && name.trim() ? name : '저장소 이름 정보 없음';
    article.querySelector('.project-description').textContent = typeof description === 'string' && description.trim() ? description : '등록된 설명이 없습니다.';
    article.querySelector('.project-language').textContent = languageOf(repo);
    article.querySelector('.project-stars').textContent = Number.isInteger(stars) && stars >= 0 ? `★ ${stars} Stars` : 'Star 정보 없음';
    const url = safeHttpsUrl(htmlUrl);
    const links = article.querySelector('.project-links');
    if (url && url.hostname === 'github.com' && !url.port && url.pathname.startsWith(`/${github.username}/`)) links.append(externalLink('GitHub ↗', url.href));
    else links.textContent = '저장소 링크 정보 없음';
    const readmeUrl = getReadmeUrl(repo);
    if (readmeUrl) links.append(externalLink('README ↗', readmeUrl));
    return article;
  };
  const observeCards = (cards) => cards.forEach((card) => { if (observer) observer.observe(card); });
  const renderFilters = () => {
    const languages = [...new Set(state.projects.items.map(languageOf))].sort((a, b) => a.localeCompare(b));
    const options = [{ value: 'all', label: '전체' }, ...languages.map((language) => ({ value: language, label: language }))];
    filters.replaceChildren(...options.map(({ value, label }) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'button filter-button';
      button.dataset.language = value;
      button.textContent = label;
      button.setAttribute('aria-pressed', String(state.projects.language === value));
      return button;
    }));
  };
  const renderRepositoryList = () => {
    const { items, language } = state.projects;
    const visible = items.filter((repo) => language === 'all' || languageOf(repo) === language);
    const sorted = [...visible].sort((a, b) => String(a.name || '').localeCompare(String(b.name || '')));
    if (observer) projectGrid.querySelectorAll('.project-card').forEach((card) => observer.unobserve(card));
    const cards = sorted.map((repo) => makeProjectCard(repo));
    projectGrid.replaceChildren(...cards);
    observeCards(cards);
    select('#filter-status').textContent = `${language === 'all' ? '전체' : language} · ${visible.length} / ${items.length}개${visible.length ? '' : ' · 이 조건에 맞는 저장소가 없습니다.'}`;
    filters.querySelectorAll('button').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
  };
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-language]');
    if (!button || !filters.contains(button) || state.projects.status !== 'success') return;
    state.projects.language = button.dataset.language;
    renderRepositoryList();
  });
  const renderProjects = () => {
    const { status, items, error } = state.projects;
    if (observer) document.querySelectorAll('.project-card').forEach((card) => observer.unobserve(card));
    projectGrid.replaceChildren();
    featuredGrid.replaceChildren();
    filters.replaceChildren();
    select('#filter-status').textContent = '';
    select('#featured-status').textContent = '';
    [projectGrid, featuredGrid].forEach((grid) => grid.setAttribute('aria-busy', String(status === 'loading')));
    retryButton.hidden = status !== 'error';
    retryButton.disabled = status === 'loading';
    if (status === 'loading') projectStatus.textContent = '프로젝트를 불러오는 중입니다…';
    if (status === 'empty') projectStatus.textContent = '표시할 프로젝트가 없습니다.';
    if (status === 'error') projectStatus.textContent = `프로젝트를 불러올 수 없습니다. ${error}`;
    if (status === 'success') {
      projectStatus.textContent = `공개 저장소 ${items.length}개 · All은 이름 오름차순`;
      const featured = github.featured.map((name) => items.find((repo) => repo.name === name)).filter(Boolean);
      const cards = featured.map((repo, index) => makeProjectCard(repo, true, index));
      featuredGrid.replaceChildren(...cards);
      observeCards(cards);
      select('#featured-status').textContent = featured.length ? `코디세이 학습 과제 ${featured.length}개` : '현재 공개 목록에 지정된 Featured 저장소가 없습니다.';
      renderFilters();
      renderRepositoryList();
    }
  };
  const fetchProjects = async () => {
    if (state.projects.status === 'loading') return;
    state.projects = { status: 'loading', items: [], error: '', language: state.projects.language };
    renderProjects();
    try {
      const repositories = [];
      let page = 1;
      let hasNextPage = true;
      while (hasNextPage) {
        const controller = new AbortController();
        const timeout = window.setTimeout(() => controller.abort(), 15000);
        try {
          const response = await fetch(`${github.endpoint}?per_page=100&page=${page}`, {
            headers: { Accept: 'application/vnd.github+json' }, signal: controller.signal
          });
          if (!response.ok) {
            if (response.status === 403 || response.status === 429 || response.headers.get('x-ratelimit-remaining') === '0') {
              throw new Error('GitHub 요청 한도 또는 접근 제한입니다. 잠시 후 다시 시도해 주세요.');
            }
            throw new Error(`GitHub 응답 오류 (${response.status})입니다.`);
          }
          const data = await response.json();
          if (!Array.isArray(data) || data.some((repo) => !repo || typeof repo !== 'object' || Array.isArray(repo))) {
            throw new Error('예상하지 못한 응답 형식입니다.');
          }
          repositories.push(...data);
          // GitHub Link 헤더는 다음 페이지 유무만 확인합니다. 요청 주소는 고정 엔드포인트로 구성합니다.
          hasNextPage = /rel="next"/.test(response.headers.get('link') || '');
          if (hasNextPage && data.length === 0) throw new Error('페이지 응답 형식이 올바르지 않습니다.');
          page += 1;
        } finally { window.clearTimeout(timeout); }
      }
      state.projects = { status: repositories.length ? 'success' : 'empty', items: repositories, error: '', language: state.projects.language };
    } catch (error) {
      const message = error.name === 'AbortError' ? '요청 시간이 초과되었습니다. 다시 시도해 주세요.'
        : error instanceof TypeError ? '네트워크 연결을 확인하고 다시 시도해 주세요.'
        : error instanceof SyntaxError ? '예상하지 못한 응답 형식입니다.' : error.message;
      state.projects = { status: 'error', items: [], error: message, language: state.projects.language };
    }
    renderProjects();
  };
  retryButton.addEventListener('click', () => { void fetchProjects(); });

  const validateField = (name, value) => {
    const trimmed = value.trim();
    const labels = { name: '이름', email: '이메일', message: '메시지' };
    if (!trimmed) return `${labels[name]} 항목을 입력해 주세요.`;
    if (name === 'email' && (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed) || fields.email.validity.typeMismatch)) return '올바른 이메일 주소를 입력해 주세요.';
    if (value.length > fields[name].maxLength) return `${fields[name].maxLength}자 이하로 입력해 주세요.`;
    return '';
  };
  const canSendEmail = () => email.enabled === true && typeof email.formId === 'string' && /^[a-zA-Z0-9]{6,64}$/.test(email.formId);
  const renderFormState = () => {
    fieldNames.forEach((name) => {
      const error = state.form.errors[name] || '';
      select(`#${name}-error`).textContent = error;
      fields[name].setAttribute('aria-invalid', String(Boolean(error)));
    });
    const submitting = state.form.status === 'submitting';
    select('#contact-fields').disabled = submitting;
    select('#contact-submit').disabled = submitting;
    form.setAttribute('aria-busy', String(submitting));
    formStatus.dataset.state = state.form.status;
    formStatus.classList.toggle('success', state.form.status === 'success');
    formStatus.textContent = state.form.message;
    select('#contact-submit').textContent = submitting ? '전송 중…' : canSendEmail() ? '메시지 보내기 ↗' : '입력 확인 · 전송 비활성';
    if (canSendEmail()) {
      select('#contact-intro').textContent = '아래 폼으로 문의를 남길 수 있습니다. 개인 이메일 주소는 공개하지 않습니다.';
      select('#form-notice').textContent = '제출하면 이름·이메일·메시지가 문의 처리를 위해 Formspree와 수신자에게 전달됩니다. 민감한 정보는 입력하지 마세요.';
    }
  };
  fieldNames.forEach((name) => {
    fields[name].addEventListener('input', () => {
      state.form.values[name] = fields[name].value;
      state.form.errors[name] = validateField(name, fields[name].value);
      state.form.status = Object.values(state.form.errors).some(Boolean) ? 'invalid' : 'idle';
      state.form.message = '';
      renderFormState();
    });
  });
  const submitContact = async (event) => {
    event.preventDefault();
    if (state.form.status === 'submitting') return;
    fieldNames.forEach((name) => {
      state.form.values[name] = fields[name].value.trim();
      state.form.errors[name] = validateField(name, fields[name].value);
    });
    const invalidName = fieldNames.find((name) => state.form.errors[name]);
    if (invalidName) {
      state.form.status = 'invalid';
      state.form.message = '입력 오류를 확인해 주세요.';
      renderFormState();
      fields[invalidName].focus();
      return;
    }
    if (!canSendEmail()) {
      state.form.status = 'error';
      state.form.message = '입력 검증이 완료되었습니다. 서비스 연동 전이므로 메시지는 전송되지 않았습니다.';
      renderFormState();
      return;
    }
    if (form.elements.namedItem('_gotcha').value) {
      state.form.status = 'error';
      state.form.message = '자동 입력 방지 확인에 실패했습니다. 입력 내용을 확인해 주세요.';
      renderFormState();
      return;
    }
    const body = new FormData();
    fieldNames.forEach((name) => body.append(name, state.form.values[name]));
    body.append('_gotcha', '');
    state.form.status = 'submitting';
    state.form.message = '메시지를 전송하고 있습니다…';
    renderFormState();
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), email.timeoutMs);
    try {
      const response = await fetch(`https://formspree.io/f/${email.formId}`, {
        method: 'POST', body, headers: { Accept: 'application/json' }, signal: controller.signal
      });
      if (!response.ok) throw new Error(response.status === 429 ? '요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.' : `전송 서비스 오류 (${response.status})입니다. 입력 내용은 유지됩니다.`);
      const data = await response.json();
      if (!data || typeof data !== 'object' || Array.isArray(data) || data.ok === false || data.errors || data.error) throw new Error('전송 서비스가 접수를 확인하지 못했습니다.');
      state.form.status = 'success';
      state.form.message = '전송 서비스가 메시지를 접수했습니다. 수신함 도착 여부는 별도로 확인해야 합니다.';
      form.reset();
      state.form.values = { name: '', email: '', message: '' };
      state.form.errors = {};
    } catch (error) {
      state.form.status = 'error';
      state.form.message = error.name === 'AbortError' ? '응답 시간이 초과되었습니다. 중복 전송을 피하려면 접수 여부를 확인한 뒤 다시 시도해 주세요.'
        : error instanceof TypeError ? '네트워크 오류로 접수를 확인하지 못했습니다. 연결과 접수 여부를 확인해 주세요.'
        : error instanceof SyntaxError ? '전송 서비스 응답을 확인하지 못했습니다.' : error.message;
    } finally {
      window.clearTimeout(timeout);
      renderFormState();
    }
  };
  form.addEventListener('submit', submitContact);
  renderPersonalContent();
  renderFormState();
  setupTyping();
  void fetchProjects();
})();
