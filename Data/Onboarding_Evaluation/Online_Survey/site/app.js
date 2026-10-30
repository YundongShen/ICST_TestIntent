
const BG01 = [
  "Software developer / engineer",
  "Software test / QA engineer",
  "Researcher / academic",
  "Other"
];
const BG02 = [
  "I am still learning about testing as part of my education",
  "Less than 1 year",
  "1 to less than 3 years",
  "3 to less than 6 years",
  "6 to less than 9 years",
  "9 years or more"
];
const BG03 = [
  [
    "language",
    "JavaScript / TypeScript"
  ],
  [
    "playwright",
    "Playwright tests and assertions"
  ],
  [
    "dom",
    "HTML elements and DOM attributes"
  ],
  [
    "css",
    "CSS styling and Bootstrap"
  ]
];
const FAMILIAR = [
  "Not familiar at all",
  "Slightly familiar",
  "Somewhat familiar",
  "Moderately familiar",
  "Very familiar"
];
const AGREEMENT = [
  "Strongly disagree",
  "Disagree",
  "Neither agree nor disagree",
  "Agree",
  "Strongly agree"
];
const GROUPS = [
  {
    "key": "g1",
    "title": "Part 2 of 3 · Understanding the suite",
    "main": "The material helps me understand this test suite.",
    "itemsQ": "More specifically, the material makes clear...",
    "items": [
      "...what behavior the test suite checks.",
      "...what each test case is meant to check.",
      "...how each test's steps and assertions check the intended behavior.",
      "...how the test cases relate to each other."
    ],
    "why": "Which part of the material helped you most to understand the test suite, and why?",
    "why2": "What is still unclear about the test suite, and why?",
    "context": "Base your answers on the material: the test code and the supporting material shown above.",
    "cannotJudge": "Cannot judge from the material",
    "reasonPlaceholder": "Why can't you judge this from the material?"
  },
  {
    "key": "g2",
    "title": "Part 3 of 3 · Planning a new test case",
    "main": "The material would help me plan a new test case for this suite.",
    "itemsQ": "More specifically, the material would help me...",
    "items": [
      "...check whether a new test case would duplicate an existing one.",
      "...find an existing test case to build on.",
      "...decide which behavior or condition to test next.",
      "...choose inputs and expected results for a new test case."
    ],
    "why": "What in the material would you use to design a new test case, and why?",
    "why2": "What information is missing that you would need to design a new test case?",
    "context": "Base your answers on the material: the test code and the supporting material shown above.",
    "cannotJudge": "Cannot judge from the material",
    "reasonPlaceholder": "Why can't you judge this from the material?"
  }
];
function feedbackGroup(key,condition=COND) {
    const group={...GROUPS.find(g=>g.key===key),scale:AGREEMENT};
    if(condition==='A')group.context='Base your answers on the material: the test code shown above.';
    return group;
  }
const COMPREHENSION_TITLE = "Part 1 of 3 · Test Suite Comprehension";
const COMPREHENSION_INTRO = "These three questions evaluate the material, not you. We want to see how well it helps you understand what the test suite is meant to check. If the material does not tell you, choose \u201cCan't tell from the material\u201d. That is a useful answer too.";
const COMPREHENSION = [
  {
    "key": "cq1",
    "text": "How many test cases does this test suite contain?",
    "options": [
      "2",
      "5",
      "6",
      "7",
      "Can't tell from the material"
    ],
    "why": ""
  },
  {
    "key": "cq2",
    "text": "According to this test suite, what should happen to the page content (the body element) after the page loads?",
    "options": [
      "It is visible immediately and stays visible",
      "It is hidden at first and then becomes visible",
      "It is visible at first and then becomes hidden",
      "Can't tell from the material"
    ],
    "why": ""
  },
  {
    "key": "cq3",
    "text": "Suppose clicking the \"Launch demo modal\" button stopped opening the modal. Would this test suite detect it?",
    "options": [
      "Yes, at least one test would fail",
      "No, all tests would still pass",
      "Can't tell from the material"
    ],
    "why": "Briefly, what made you choose this answer?"
  }
];
const STEPS = ["Background","Instructions","Comprehension","Part 2","Part 3","Finish"];

/* Connection and local recovery. No service-role key is used in the browser. */
const CONFIG = window.SURVEY_CONFIG;
const BANK = JSON.parse(document.getElementById('material-bank').textContent);
const MODE = new URLSearchParams(location.search).get('mode') || CONFIG.mode;
const LS_KEY = 'online-onboarding-' + CONFIG.study + '-' + MODE;
let DATA = BANK.A, COND = '', HAS_DOC = false;
const $ = id => document.getElementById(id);
const blank = () => ({
  pid: '', step: 0, maxStep: 0, started: new Date().toISOString(), finished: '',
  bg01: [], bg01_other: '', bg02: '', bg03: {},
  g1: { main: '', reason: '', items: {}, why: '', why2: '' },
  g2: { main: '', reason: '', items: {}, why: '', why2: '' },
  cq: {}, secs: [0,0,0,0,0,0], scrollCode: 0, scrollDoc: 0, linkClicks: 0,
});
let session, S = blank(), revision = 0, acknowledged = 0;
let shownAt = Date.now(), serverReady = false, busy = false, connecting = false;
let submittedAt = null, syncPromise = null, saveTimer;
let onlineStatus = 'Connecting…';

function setOnlineStatus(text) {
  onlineStatus = text;
  $('save-status').textContent = text;
  if (!$('status').classList.contains('err')) $('status').textContent = text;
}
function persist() {
  localStorage.setItem(LS_KEY, JSON.stringify({session, state: S, revision}));
}
function saveDraft() {
  if (submittedAt || !session) return;
  revision = Math.max(Date.now(), revision + 1);
  try { persist(); } catch {
    setOnlineStatus('Browser storage failed. Keep this page open until submission.');
  }
  setOnlineStatus('Saving…');
  clearTimeout(saveTimer);
  if (!busy && serverReady) saveTimer = setTimeout(() => flushDraft().catch(() => {}), 900);
}
function answerParams() {
  return {p_id: session.id, p_token: session.token, p_revision: revision,
    p_state: JSON.parse(JSON.stringify(S))};
}
async function rpc(name, args) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(CONFIG.url + '/rest/v1/rpc/' + name, {
      method: 'POST', signal: controller.signal,
      headers: {'Content-Type': 'application/json', apikey: CONFIG.publishableKey},
      body: JSON.stringify(args)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || 'The server could not save your answers.');
    return result;
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('The server did not respond. Your draft is kept in this browser. Please try again.');
    throw error;
  } finally { clearTimeout(timeout); }
}
async function flushDraft() {
  clearTimeout(saveTimer);
  if (!serverReady || submittedAt || revision <= acknowledged) return;
  if (syncPromise) {
    await syncPromise;
    if (!submittedAt && revision > acknowledged) return flushDraft();
    return;
  }
  const args = answerParams();
  syncPromise = (async () => {
    try {
      const result = await rpc('survey_save', args);
      if (result.submitted_at) { applyReceipt(result); return; }
      if (result.revision > args.p_revision) throw new Error('A newer draft exists. Close other survey tabs and reload this page.');
      acknowledged = Math.max(acknowledged, result.revision);
      setOnlineStatus(revision <= acknowledged ? 'Saved online' : 'Saving…');
    } catch (error) {
      setOnlineStatus('Not saved online. Draft kept in this browser.');
      throw error;
    }
  })();
  try { await syncPromise; } finally { syncPromise = null; }
}
function applyAssignment(result) {
  if (!['A','B','C'].includes(result.condition) || result.study !== CONFIG.study || result.suite !== BANK.A.suite)
    throw new Error('The assigned material does not match this survey.');
  COND = result.condition; HAS_DOC = COND !== 'A'; DATA = BANK[COND];
  $('doccol').hidden = !HAS_DOC;
  $('work').classList.toggle('single', !HAS_DOC);
  $('g-task').textContent = HAS_DOC
    ? 'Your material includes the test suite code on the left and supporting material on the right. Read it as if you were a new tester getting to know the suite.'
    : 'Your material is the test suite code. Read it as if you were a new tester getting to know the suite.';
  $('suitename').textContent = $('codetitle').textContent = DATA.codeName;
  $('suitesub').textContent = HAS_DOC ? 'Test code + supporting material' : 'Test code';
  $('cannot-guide').textContent = feedbackGroup('g1').cannotJudge;
  renderCode(); if (HAS_DOC) renderDoc();
  acknowledged = Math.max(acknowledged, result.revision);
}
function applyReceipt(result) {
  submittedAt = result.submitted_at;
  if (result.state) S = result.state;
  S.finished = submittedAt; S.step = 5; S.maxStep = 5;
  revision = acknowledged = result.revision;
  try { persist(); } catch {}
  setOnlineStatus('Submitted');
  $('receipt').textContent = 'Receipt: ' + session.id + ' · ' + new Date(submittedAt).toLocaleString() + '. Include this receipt ID if you request data removal.';
  render();
}
function setBusy(value) {
  busy = value;
  document.body.classList.toggle('busy', value);
  for (const id of ['bgnext','ready','prev','next']) $(id).disabled = value;
}
async function transition(action, errorId) {
  if (busy) return;
  setBusy(true); $(errorId).textContent = '';
  try { await action(); }
  catch (error) { $(errorId).textContent = error.message; $(errorId).classList.add('err'); }
  finally {
    setBusy(false);
    if (serverReady && !submittedAt && revision > acknowledged) saveTimer = setTimeout(() => flushDraft().catch(() => {}), 1500);
  }
}
async function connect() {
  if (connecting || serverReady) return;
  connecting = true; $('bgnext').disabled = true;
  $('session-retry').hidden = true;
  try {
    if (!['test','live'].includes(MODE)) throw new Error('Invalid survey mode. Use the link provided by the researcher.');
    if (!session) {
      const stored = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
      if (stored) {
        session = stored.session;
        S = Object.assign(blank(), stored.state);
        revision = Number(stored.revision) || 0;
      } else {
        const bytes = crypto.getRandomValues(new Uint8Array(32));
        session = {id: crypto.randomUUID(), token: Array.from(bytes, x => x.toString(16).padStart(2,'0')).join('')};
      }
      S.pid = session.id;
      persist(); // Refuse to start if a stable recovery token cannot be kept.
    }
    const result = await rpc('survey_open', {p_id: session.id, p_token: session.token, p_mode: MODE});
    if (result.study !== CONFIG.study || result.suite !== BANK.A.suite) throw new Error('Survey version mismatch. Contact the researcher.');
    acknowledged = result.revision;
    if (result.state && result.revision >= revision) { S = result.state; revision = result.revision; }
    serverReady = true;
    if (result.condition) {
      applyAssignment(result);
      S.maxStep = Math.max(1, Math.min(4, S.maxStep)); S.step = Math.min(4, S.step);
    } else { S.step = S.maxStep = 0; }
    $('session-notice').classList.remove('error');
    $('session-message').textContent = MODE === 'test'
      ? 'Pilot mode. These answers are stored as test data, separate from the study.'
      : 'Your answers are saved online. Please use one browser tab.';
    $('session-notice').hidden = false;
    persist(); renderBg(); render();
    setOnlineStatus('Connected');
    if (result.submitted_at) applyReceipt(result);
    else if (revision > acknowledged) flushDraft().catch(() => {});
  } catch (error) {
    serverReady = false;
    $('session-notice').classList.add('error');
    $('session-message').textContent = 'Could not connect: ' + error.message;
    $('session-retry').hidden = false;
    setOnlineStatus('Not connected');
  } finally {
    connecting = false; $('bgnext').disabled = !serverReady;
  }
}

function bankTime() {
  S.secs[S.step] = (S.secs[S.step] || 0) + (Date.now() - shownAt) / 1000;
  shownAt = Date.now();
}
function fmt(s) { s = Math.round(s); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }

/* ---------- small builders ---------- */
function el(tag, attrs = {}, text) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v; else if (k.startsWith("on")) n[k] = v; else n.setAttribute(k, v);
  }
  if (text != null) n.textContent = text;
  return n;
}
// A Likert matrix: one column header per scale point, one row per item.
function likert(box, rows, labels, get, set) {
  box.textContent = "";
  box.appendChild(el("div", { class: "corner" }));
  labels.forEach((t, i) => {
    const h = el("div", { class: "lh" });
    h.append(el("b", {}, String(i + 1)), el("span", {}, t));
    box.appendChild(h);
  });
  rows.forEach(([key, text]) => {
    box.appendChild(el("div", { class: "lt" }, text));
    const btns = [];
    labels.forEach((t, i) => {
      const v = i + 1;
      const b = el("button", { class: "lbtn", type: "button", "aria-pressed": String(get(key) === v), "aria-label": text + ": " + v + " – " + t, title: t }, String(v));
      b.onclick = () => { set(key, v); btns.forEach((x, j) => x.setAttribute("aria-pressed", String(j + 1 === v))); save(); };
      btns.push(b);
      const c = el("div", { class: "lc" }); c.appendChild(b);
      box.appendChild(c);
    });
  });
}

/* ---------- step 1: background ---------- */
const other = el("input", { type: "text", "aria-label": "Other role", placeholder: "Please specify" });
other.oninput = () => { S.bg01_other = other.value; save(); };

function radioList(box, name, options, get, set) {
  box.textContent = "";
  options.forEach((t) => {
    const lab = el("label", { class: "opt" });
    const r = el("input", { type: "radio", name, value: t });
    r.checked = get() === t;
    r.onchange = () => set(t);
    lab.append(r, el("span", {}, t === "Other" ? "Other:" : t));
    if (t === "Other") lab.appendChild(other);
    box.appendChild(lab);
  });
}
function renderBg() {
  other.value=S.bg01_other;other.disabled=!S.bg01.includes('Other');
  const box=$('bg01');box.textContent='';
  BG01.forEach(text=>{
    const label=el('label',{class:'opt'}),input=el('input',{type:'checkbox',name:'bg01',value:text});
    input.checked=S.bg01.includes(text);
    input.onchange=()=>{
      S.bg01=BG01.filter(value=>value===text?input.checked:S.bg01.includes(value));
      other.disabled=!S.bg01.includes('Other');if(text==='Other'&&input.checked)other.focus();save();
    };
    label.append(input,el('span',{},text==='Other'?'Other:':text));if(text==='Other')label.appendChild(other);box.appendChild(label);
  });
  radioList($('bg02'),'bg02',BG02,()=>S.bg02,text=>{S.bg02=text;save();});
  likert($('bg03'),BG03,FAMILIAR,key=>S.bg03[key],(key,value)=>{S.bg03[key]=value;});
}
function bgMissing() {
  const missing=[];
  if(!S.bg01.length)missing.push('at least one role in question 1');
  if(S.bg01.includes('Other')&&!S.bg01_other.trim())missing.push('your role in question 1');
  if(!S.bg02)missing.push('question 2');
  if(BG03.some(([key])=>!S.bg03[key]))missing.push('every row of question 3');
  return missing;
}

/* ---------- material ---------- */
function splitHighlighted(html) {
  // Split highlighted HTML into lines, closing and reopening spans that cross a newline.
  const lines = []; const open = []; let cur = "";
  for (const tok of html.match(/<span[^>]*>|<\/span>|\n|[^<\n]+/g) || []) {
    if (tok === "\n") { cur += "</span>".repeat(open.length); lines.push(cur); cur = open.join(""); }
    else if (tok.startsWith("<span")) { open.push(tok); cur += tok; }
    else if (tok === "</span>") { open.pop(); cur += tok; }
    else cur += tok;
  }
  lines.push(cur);
  return lines;
}
function esc(t) { return t.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]); }
function renderCode() {
  const code = DATA.code.replace(/\r\n?/g, "\n").replace(/\n$/, "");
  let html;
  try { html = window.hljs ? hljs.highlight(code, { language: DATA.lang, ignoreIllegals: true }).value : esc(code); }
  catch { html = esc(code); }
  const pre = el("pre", { class: "codeview" });
  splitHighlighted(html).forEach((line, i) => {
    const row = el("div", { class: "ln", id: "L" + (i + 1) });
    const tx = el("span", { class: "tx" }); tx.innerHTML = line || " ";
    row.append(el("span", { class: "no" }, String(i + 1)), tx);
    pre.appendChild(row);
  });
  $("codebody").replaceChildren(pre);
}
function jumpTo(from, to) {
  const body = $("codebody");
  body.querySelectorAll(".ln.mark").forEach((n) => n.classList.remove("mark"));
  for (let n = from; n <= (to || from); n++) $("L" + n)?.classList.add("mark");
  const first = $("L" + from);
  if (first) body.scrollTop = first.offsetTop - body.clientHeight / 4;
  if (window.innerWidth <= 820) first?.scrollIntoView({ block: "center" });
}
function renderDoc() {
  const box = $("docbody");
  if (DATA.doc == null) { box.replaceChildren(el("div", { class: "placeholder" }, "Document not available yet.")); return; }
  let html = null;
  try {
    html = window.marked ? marked.parse(DATA.doc, { gfm: true }) : null;
    html = html && window.DOMPurify ? DOMPurify.sanitize(html) : null;
  } catch { html = null; }
  if (!html) { box.replaceChildren(el("pre", {}, DATA.doc)); return; }
  box.innerHTML = html;
  box.querySelectorAll("a").forEach((a) => {
    const href = a.getAttribute("href") || "";
    const m = href.match(/^([^#]*)#L(\d+)(?:-L(\d+))?$/);
    if (m && (!m[1] || m[1].split("/").pop() === DATA.codeName)) {
      a.href = "#L" + m[2];
      a.title = "Show these lines in the test code";
      a.onclick = (e) => { e.preventDefault(); S.linkClicks++; save(); jumpTo(+m[2], m[3] ? +m[3] : 0); };
    } else { a.target = "_blank"; a.rel = "noopener"; }
  });
}
function trackScroll(node, key) {
  node.addEventListener("scroll", () => {
    const pct = Math.min(100, Math.round(100 * (node.scrollTop + node.clientHeight) / node.scrollHeight));
    if (pct > S[key]) { S[key] = pct; save(); }
  }, { passive: true });
}

/* ---------- steps 4–5: question groups ---------- */
/* One matrix per group: the main statement is the first, emphasized row; the items follow. */
/* Main and supporting ratings share a single matrix on the left. */
function renderGroup(base) {
  const g=feedbackGroup(base.key,COND), a=S[g.key], box=$('qbox');
  box.textContent=''; $('qtitle').textContent=g.title;
  box.appendChild(el('p',{class:'question-context'},g.context));
  const columns=el('div',{class:'review-columns'});
  const closed=el('section',{class:'review-closed','aria-label':'Rating statements'});
  const open=el('aside',{class:'review-open','aria-label':'Optional comments'});
  open.appendChild(el('h4',{},'Optional comments · 2 questions'));
  columns.append(closed,open); box.appendChild(columns);
  const mx=el('div',{class:'mx'});
  mx.appendChild(el('div',{class:'mx-corner'}));
  g.scale.forEach((t,i)=>{
    const header=el('div',{class:'mx-h'});
    header.append(el('b',{},String(i+1)),el('span',{},t)); mx.appendChild(header);
  });
  mx.appendChild(el('div',{class:'mx-h mx-hcj'}));
  const reason=el('div',{class:'reason'});
  const reasonInput=el('textarea',{id:g.key+'-reason',rows:'2',placeholder:g.reasonPlaceholder});
  reasonInput.value=a.reason||'';
  reasonInput.oninput=()=>{a.reason=reasonInput.value;save();};
  reason.append(el('label',{for:reasonInput.id},'Please say why you cannot judge (required)'),reasonInput);
  reason.hidden=a.main!=='cj';
  mx.appendChild(el('div',{class:'mx-t mx-main'},g.main));
  const opts=g.scale.map((t,i)=>[String(i+1),t]).concat([['cj',g.cannotJudge]]), mainButtons=[];
  opts.forEach(([value,text])=>{
    const cj=value==='cj', cell=el('div',{class:'mx-c mx-main'+(cj?' mx-cj':'')});
    const button=el('button',{class:'lbtn'+(cj?' cjbtn':''),type:'button',
      'data-main-value':value,'aria-pressed':String(a.main===value),
      'aria-label':g.main+': '+text,title:text},cj?text:value);
    button.onclick=()=>{
      a.main=value;reason.hidden=!cj;
      mainButtons.forEach((b,i)=>b.setAttribute('aria-pressed',String(opts[i][0]===value)));
      if(cj) reasonInput.focus();save();
    };
    mainButtons.push(button);cell.appendChild(button);mx.appendChild(cell);
  });
  mx.appendChild(el('div',{class:'mx-sub'},g.itemsQ));
  g.items.forEach((text,i)=>{
    const key=String(i+1),buttons=[];
    mx.appendChild(el('div',{class:'mx-t'},text));
    g.scale.forEach((label,n)=>{
      const value=n+1,button=el('button',{class:'lbtn',type:'button',
        'data-item':key,'data-value':String(value),'aria-pressed':String(a.items[key]===value),
        'aria-label':text+': '+label,title:label},String(value));
      button.onclick=()=>{a.items[key]=value;buttons.forEach((b,j)=>b.setAttribute('aria-pressed',String(j+1===value)));save();};
      buttons.push(button);const cell=el('div',{class:'mx-c'});cell.appendChild(button);mx.appendChild(cell);
    });
    mx.appendChild(el('div',{class:'mx-c mx-empty'}));
  });
  closed.append(mx,reason);
  for(const field of ['why','why2']) appendOptional(open,g.key+'-'+field,g[field],
    a[field]||'',value=>{a[field]=value;save();});
  $('qbox').scrollTop=0;
}
function appendOptional(parent,id,text,value,onInput) {
  const section=el('div',{class:'why'}),label=el('label',{for:id},text+' ');
  label.appendChild(el('small',{},'(optional)'));
  const input=el('textarea',{id,rows:'3'});input.value=value;
  input.oninput=()=>onInput(input.value);section.append(label,input);parent.appendChild(section);
}
function renderCQ() {
  const box=$('qbox');box.textContent='';$('qtitle').textContent=COMPREHENSION_TITLE;
  const columns=el('div',{class:'review-columns'}),closed=el('section',{class:'review-closed'}),open=el('aside',{class:'review-open'});
  closed.appendChild(el('p',{class:'cq-intro'},COMPREHENSION_INTRO));
  const followUps=COMPREHENSION.map((question,n)=>question.why?n+1:0).filter(Boolean);
  open.appendChild(el('h4',{},followUps.length===1?'Optional comments · Question '+followUps[0]:'Optional comments'));
  const list=el('div',{class:'cq-list'});closed.appendChild(list);columns.append(closed,open);box.appendChild(columns);
  COMPREHENSION.forEach((question,n)=>{
    const block=el('fieldset',{class:'cq'});
    block.appendChild(el('legend',{class:'cq-q'},(n+1)+'. '+question.text));
    const options=el('div',{class:'cq-opts'});
    question.options.forEach(text=>{
      const label=el('label',{class:'opt'}),input=el('input',{type:'radio',name:'cq-'+question.key,value:text});
      input.checked=S.cq[question.key]===text;
      input.onchange=()=>{S.cq[question.key]=text;save();};label.append(input,el('span',{},text));options.appendChild(label);
    });
    block.appendChild(options);list.appendChild(block);
    if(question.why) appendOptional(open,'cq-'+question.key+'-why',question.why,S.cq[question.key+'_why']||'',
      value=>{S.cq[question.key+'_why']=value;save();});
  });
  $('qbox').scrollTop=0;
}

// Collapsing the panel gives the material the full height; each question group opens expanded.
let collapsed = false;
function setCollapsed(c) {
  collapsed = c;
  $("qpanel").classList.toggle("collapsed", c);
  $("resizer").hidden = c || !onMaterial(S.step);
  $("qtoggle").setAttribute("aria-expanded", String(!c));
  $("qtoggle").querySelector("span").textContent = c ? "Show questions" : "Hide questions";
}
function updateAnswered() {
  if (!onMaterial(S.step)) return;
  if (S.step === 2) {
    const n = COMPREHENSION.filter((q) => q.options.includes(S.cq[q.key])).length, total = COMPREHENSION.length;
    $("answered").textContent = (n === total ? "✓ " : "") + n + " / " + total + " answered";
    $("answered").classList.toggle("done", n === total);
    return;
  }
  const g = GROUPS[S.step - 3], a = S[g.key];
  const n = (a.main && (a.main !== "cj" || a.reason.trim()) ? 1 : 0) + g.items.filter((_, i) => a.items[String(i + 1)]).length;
  const total = g.items.length + 1;
  $("answered").textContent = (n === total ? "✓ " : "") + n + " / " + total + " answered";
  $("answered").classList.toggle("done", n === total);
}
function groupMissing(g) {
  const a = S[g.key]; const m = [];
  if (!a.main) m.push("the main question");
  else if (a.main === "cj" && !a.reason.trim()) m.push("the reason for “Cannot judge”");
  if (g.items.some((_, i) => !a.items[String(i + 1)])) m.push("all four items");
  return m;
}

/* ---------- step 3: Test Suite Comprehension ---------- */
function onMaterial(i) { return i >= 2 && i <= 4; }
function cqMissing() {
  const nums = COMPREHENSION.map((q, i) => q.options.includes(S.cq[q.key]) ? 0 : i + 1).filter(Boolean);
  if (!nums.length) return [];
  return [(nums.length > 1 ? 'questions ' : 'question ') + nums.join(', ')];
}

/* ---------- navigation ---------- */
function canEnter(i) { return !busy && (submittedAt ? i === 5 : i <= S.maxStep && i < 5); }
function go(i) {
  if (i < 0 || i >= STEPS.length || !canEnter(i)) return;
  bankTime();
  S.step = i;

  save(); render();
  window.scrollTo(0, 0);
}
function advance(from) {
  S.maxStep = Math.max(S.maxStep, from + 1);
  go(from + 1);
}
function render() {
  const i = S.step;
  $("s-bg").hidden = i !== 0;
  $("guide").hidden = i === 0 || i === 5;
  $("workhead").hidden = $("work").hidden = $("resizer").hidden = $("qpanel").hidden = !onMaterial(i);
  $("s-done").hidden = i !== 5;
  $("startrow").hidden = i !== 1;
  $("qfoot").hidden = !onMaterial(i);
  if (i === 1) $("guide").open = true;
  if (i === 2) { renderCQ(); setCollapsed(false); updateAnswered(); }
  if (i === 3 || i === 4) { renderGroup(GROUPS[i - 3]); setCollapsed(false); updateAnswered(); }
  $("next").textContent = i === 4 ? "Submit answers" : "Next →";
  $("status").textContent = "";
  $("status").classList.remove("err");
  const steps = $("steps"); steps.textContent = "";
  STEPS.forEach((name, k) => {
    if (k) steps.appendChild(el("span", { class: "sep", "aria-hidden": "true" }));
    const c = el("button", { class: "step", type: "button", "data-done": String(k < S.maxStep && k !== i) });
    if (k === i) c.setAttribute("aria-current", "step");
    c.append(el("span", { class: "num" }, k < S.maxStep && k !== i ? "✓" : String(k + 1)), el("span", { class: "lbl" }, name));
    c.disabled = !canEnter(k);
    c.onclick = () => go(k);
    steps.appendChild(c);
  });
}
function save() {
  saveDraft();
  updateAnswered();
  if ($("bgerr").textContent && !bgMissing().length) $("bgerr").textContent = "";
  if ($("status").classList.contains("err")) { $("status").textContent = ""; $("status").classList.remove("err"); }
}


$("bgnext").onclick = async () => {
  const missing = bgMissing();
  if (missing.length) { $("bgerr").textContent = "Please answer " + missing.join(", ") + "."; return; }
  if (!serverReady || busy) { $("bgerr").textContent = "Connect to the survey before continuing."; return; }
  await transition(async () => {
    bankTime(); saveDraft(); await flushDraft();
    const result = await rpc("survey_assign", answerParams());
    applyAssignment(result);
    S.maxStep = Math.max(1, S.maxStep); S.step = 1; save(); render();
  }, "bgerr");
};
$("ready").onclick = () => { if (busy || !COND) return; $("guide").open = false; advance(1); };
$("prev").onclick = () => go(S.step - 1);
$("next").onclick = async () => {
  if (busy || submittedAt) return;
  const missing = S.step === 2 ? cqMissing() : groupMissing(GROUPS[S.step - 3]);
  if (missing.length) { setCollapsed(false); $("qbox").scrollTop = $("qbox").scrollHeight; $("status").textContent = "Please answer " + missing.join(" and ") + "."; $("status").classList.add("err"); return; }
  if (S.step === 2 || S.step === 3) { advance(S.step); return; }
  await transition(async () => {
    const background = bgMissing();
    const earlier = cqMissing().concat(groupMissing(GROUPS[0]));
    if (background.length || earlier.length) throw new Error("Please complete the background questions, the comprehension questions and Part 1 before submitting.");
    bankTime(); saveDraft(); await flushDraft();
    const result = await rpc("survey_submit", answerParams());
    if (!result.submitted_at) throw new Error("Submission was not confirmed. Please try again.");
    applyReceipt(result);
  }, "status");
};
$("qtoggle").onclick = () => setCollapsed(!collapsed);
$("qtitle").onclick = () => { if (collapsed) setCollapsed(false); };

/* ---------- resizable question panel (a per-viewer convenience, kept in this browser) ---------- */
const PANEL_KEY = "online-onboarding-panel-height-v3";
function setPanelHeight(h) {
  const q = $("qpanel");
  if (h == null) { q.style.height = ""; q.style.maxHeight = ""; return; }
  h = Math.round(Math.max(140, Math.min(h, window.innerHeight * 0.8)));
  q.style.height = h + "px"; q.style.maxHeight = "none";
}
function rememberPanel() { try { localStorage.setItem(PANEL_KEY, String(parseInt($("qpanel").style.height) || "")); } catch {} }
try { const h = parseInt(localStorage.getItem(PANEL_KEY)); if (h) setPanelHeight(h); } catch {}
$("resizer").onpointerdown = (e) => {
  const r = $("resizer"); e.preventDefault();
  r.setPointerCapture(e.pointerId); r.classList.add("dragging"); document.body.classList.add("resizing");
  const move = (ev) => setPanelHeight(window.innerHeight - ev.clientY - $("qfoot").offsetHeight);
  const up = () => {
    r.removeEventListener("pointermove", move); r.removeEventListener("pointerup", up);
    r.classList.remove("dragging"); document.body.classList.remove("resizing"); rememberPanel();
  };
  r.addEventListener("pointermove", move); r.addEventListener("pointerup", up);
};
$("resizer").ondblclick = () => { setPanelHeight(null); try { localStorage.removeItem(PANEL_KEY); } catch {} };
$("resizer").onkeydown = (e) => {
  if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
  e.preventDefault();
  setPanelHeight($("qpanel").offsetHeight + (e.key === "ArrowUp" ? 40 : -40)); rememberPanel();
};


/* ---------- boot ---------- */
renderBg();
trackScroll($("codebody"), "scrollCode");
trackScroll($("docbody"), "scrollDoc");
$('session-retry').onclick = connect;
window.addEventListener('online', () => { if (!serverReady) connect(); else flushDraft().catch(() => {}); });
document.addEventListener("visibilitychange", () => {
  if (document.hidden) { bankTime(); save(); if (serverReady) flushDraft().catch(() => {}); }
  else shownAt = Date.now();
});
setInterval(() => {
  $("timer").textContent = fmt((S.secs[S.step] || 0) + (Date.now() - shownAt) / 1000);
}, 1000);
setInterval(() => { if (serverReady && !busy && !submittedAt && revision > acknowledged) flushDraft().catch(() => {}); }, 15000);
connect();

