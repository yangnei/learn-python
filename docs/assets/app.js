/* Learn Python — interactive site runtime.
   - Renders embedded markdown (marked) + syntax highlight (highlight.js)
   - Turns playground snippets into editable, runnable editors via Pyodide (Python in the browser)
   - Tracks per-page completion in localStorage and reflects it in the nav. */

const PYODIDE_VERSION = "0.26.4";
const STORE_KEY = "pyresearch.progress.v1";

/* ---------- progress (localStorage) ---------- */
function getProgress(){ try{ return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }catch{ return {}; } }
function setDone(id, done){ const p=getProgress(); if(done)p[id]=true; else delete p[id]; localStorage.setItem(STORE_KEY, JSON.stringify(p)); }
function isDone(id){ return !!getProgress()[id]; }

/* ---------- markdown rendering ---------- */
function slugify(text){
  return text.toLowerCase().trim()
    .replace(/[^\w\s-]/g, "")   // drop punctuation
    .replace(/\s+/g, "-")       // spaces -> hyphens
    .replace(/-+/g, "-");       // collapse repeats
}
function renderMarkdownInto(scriptId, targetId){
  const src = document.getElementById(scriptId);
  const target = document.getElementById(targetId);
  if(!src || !target) return;
  target.innerHTML = marked.parse(src.textContent);
  // give headings stable IDs (marked v12 doesn't add them) so #anchors work
  const seen = {};
  target.querySelectorAll("h1,h2,h3,h4").forEach(h=>{
    if(!h.id){ let id = slugify(h.textContent) || "section";
      if(seen[id]){ id += "-" + (++seen[id]); } else { seen[id] = 1; }
      h.id = id; }
  });
  // syntax-highlight read-only python blocks
  target.querySelectorAll("pre code").forEach(block=>{
    if(window.hljs){ try{ hljs.highlightElement(block); }catch{} }
  });
}

/* ---------- Pyodide (lazy, shared) ---------- */
let _pyodidePromise = null;
function loadPyodideOnce(statusEl){
  if(_pyodidePromise) return _pyodidePromise;
  if(statusEl) statusEl.textContent = "loading Python… (first run downloads ~10 MB, ~10–20 s)";
  _pyodidePromise = new Promise((resolve, reject)=>{
    const s = document.createElement("script");
    s.src = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`;
    s.onload = async ()=>{ try{ resolve(await loadPyodide()); }catch(e){ reject(e); } };
    s.onerror = ()=> reject(new Error("Could not load Pyodide (are you online?)"));
    document.head.appendChild(s);
  });
  return _pyodidePromise;
}

async function runPython(code, outEl, statusEl){
  outEl.innerHTML = '<pre class="muted">Running…</pre>';
  let py;
  try{ py = await loadPyodideOnce(statusEl); }
  catch(e){ outEl.innerHTML = `<pre class="err">${escapeHtml(e.message)}</pre>`; return; }
  if(statusEl) statusEl.textContent = "";
  const buf = [];
  py.setStdout({ batched:(s)=>buf.push(s) });
  py.setStderr({ batched:(s)=>buf.push(s) });
  try{
    await py.runPythonAsync(code);
    const text = buf.join("\n");
    outEl.innerHTML = `<pre>${escapeHtml(text || "(no output — add a print() to see results)")}</pre>`;
  }catch(err){
    const text = buf.join("\n");
    outEl.innerHTML = `<pre>${escapeHtml(text)}${text? "\n":""}<span class="err">${escapeHtml(cleanTrace(err.message))}</span></pre>`;
  }
}
function cleanTrace(msg){
  // show the friendly tail of a Python traceback
  const lines = String(msg).split("\n").filter(Boolean);
  const i = lines.findIndex(l=>l.includes('File "<exec>"') || l.startsWith("Traceback"));
  return i>=0 ? lines.slice(i).join("\n") : msg;
}
function escapeHtml(s){ return String(s).replace(/[&<>]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }

/* ---------- build playground editors ---------- */
function buildPlaygrounds(){
  const host = document.getElementById("playgrounds");
  const dataEl = document.getElementById("playgrounds-data");
  if(!host || !dataEl) return;
  let snippets;
  try{ snippets = JSON.parse(dataEl.textContent); }catch{ snippets = []; }
  if(!snippets.length){ host.remove(); return; }

  const label = document.createElement("div");
  label.className = "section-label";
  label.innerHTML = '<span class="pill">Run it</span><h2>Try it yourself — live Python</h2>';
  host.appendChild(label);

  const note = document.createElement("div");
  note.className = "note";
  note.innerHTML = "Edit the code, then press <strong>Run ▶</strong>. Predict the output first!";
  host.appendChild(note);

  snippets.forEach((snip, idx)=>{
    const original = snip.code;
    const wrap = document.createElement("div");
    wrap.className = "playground";
    wrap.innerHTML = `
      <div class="pg-bar"><span class="dot"></span><span class="name">${escapeHtml(snip.title||("snippet "+(idx+1)))}</span>
        <span class="actions">
          <button class="btn reset" type="button">Reset</button>
          <button class="btn run" type="button">Run ▶</button>
        </span></div>`;
    const ta = document.createElement("textarea");
    ta.className = "code"; ta.spellcheck = false; ta.value = original;
    ta.rows = Math.min(22, original.split("\n").length + 1);
    const out = document.createElement("div"); out.className = "pg-out";
    wrap.appendChild(ta); wrap.appendChild(out);
    host.appendChild(wrap);

    const status = document.createElement("span"); status.className="pyodide-status";
    wrap.querySelector(".pg-bar").appendChild(status);

    const runBtn = wrap.querySelector(".btn.run");
    const resetBtn = wrap.querySelector(".btn.reset");
    runBtn.addEventListener("click", async ()=>{
      runBtn.disabled = true; runBtn.textContent = "Running…";
      await runPython(ta.value, out, status);
      runBtn.disabled = false; runBtn.textContent = "Run ▶";
    });
    resetBtn.addEventListener("click", ()=>{ ta.value = original; out.innerHTML=""; status.textContent=""; });
    // Ctrl/Cmd+Enter to run; Tab inserts spaces
    ta.addEventListener("keydown", (e)=>{
      if((e.ctrlKey||e.metaKey) && e.key==="Enter"){ e.preventDefault(); runBtn.click(); }
      if(e.key==="Tab"){ e.preventDefault(); const s=ta.selectionStart,en=ta.selectionEnd;
        ta.value=ta.value.slice(0,s)+"    "+ta.value.slice(en); ta.selectionStart=ta.selectionEnd=s+4; }
    });
  });
}


/* ---------- language toggle (EN / 中文): UI chrome only ---------- */
const LANG_KEY = "lp.lang";
function getLang(){
  try{
    const q = new URLSearchParams(location.search).get("lang");
    if(q === "zh" || q === "en"){ localStorage.setItem(LANG_KEY, q); return q; }
    return localStorage.getItem(LANG_KEY) === "zh" ? "zh" : "en";
  }catch{ return "en"; }
}
/* Chinese strings for chrome elements; English is recovered from the markup itself. */
const I18N_ZH = {
  "nav.home": "首页", "nav.cheats": "速查表", "check": "自我检测",
  "hero.note": "—— 全部课程、练习与速查表，可离线阅读。",
  "idx.sessions": "课程列表", "idx.keep": "常备资源",
  "dl.full": "&#8595; 下载完整课程（PDF）",
  "nb.download": "&#8595; 下载本课（.ipynb）",
  "nb.blank": "在 Colab 中打开空白笔记本 &#8599;",
  "slot.colab": "在 Colab 中打开 &#8599;",
  "card.open": '打开 <span aria-hidden="true">&rarr;</span>',
  "foot.prev": "&larr; 上一课", "foot.next": "下一课 &rarr;",
  "foot.home": "&larr; 首页", "foot.cheats": "速查表 &rarr;",
  "res.setup": '<strong>第一次用 Python？</strong> <a href="cheatsheets.html#setup">先配置电脑与学习工具</a> —— 各系统安装指南（或直接在浏览器运行、免安装），还有 Python&nbsp;Tutor、regex101，以及如何用 AI 辅助学习。',
  "res.traps": '<a href="cheatsheets.html">陷阱与坑速查表</a> —— 每个怪癖的错误写法 vs 正确写法（第 2 课起常备）。',
  "res.quick": '<a href="cheatsheets.html#quick-reference">语法速查</a>和<a href="cheatsheets.html#glossary">通俗术语表</a>。',
  "res.nb": '<strong>偏好笔记本？</strong> <a href="jupyter/lab/index.html" target="_blank" rel="noopener">在浏览器中以 Jupyter 笔记本打开全部课程</a> —— 完整 Jupyter、免安装。每课页面也有 Colab 链接和 <code>.ipynb</code> 下载。',
  "res.pdf": '<a href="learn-python-student.pdf" download>整套课程 PDF</a> —— 离线阅读或打印。',
};
/* generated-inside-markdown strings, translated after render (both directions) */
const CONTENT_I18N = [
  ["Quiz", "测验"], ["Show answers", "查看答案"],
  ["Traps — predict, then reveal", "陷阱 —— 先预测，再揭晓"],
  ["Reveal the result", "查看结果"],
];
function translateRendered(){
  const zh = getLang() === "zh";
  document.querySelectorAll(".md h1, .md h2, .md h3, .md summary").forEach(el=>{
    const txt = el.textContent.trim();
    for(const [en, zhs] of CONTENT_I18N){
      if(zh && txt === en){ el.textContent = zhs; return; }
      if(!zh && txt === zhs){ el.textContent = en; return; }
    }
    let m;
    if(zh && (m = txt.match(/^Session (\d+)$/))) el.textContent = `第 ${+m[1]} 课`;
    else if(!zh && (m = txt.match(/^第 (\d+) 课$/))) el.textContent = `Session ${m[1]}`;
  });
}
function applyLang(){
  const zh = getLang() === "zh";
  document.documentElement.lang = zh ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    if(!("orig" in el.dataset)) el.dataset.orig = el.textContent;
    const z = I18N_ZH[el.dataset.i18n];
    el.textContent = (zh && z) ? z : el.dataset.orig;
  });
  document.querySelectorAll("[data-i18n-html]").forEach(el=>{
    if(!("orig" in el.dataset)) el.dataset.orig = el.innerHTML;
    const z = I18N_ZH[el.dataset.i18nHtml];
    el.innerHTML = (zh && z) ? z : el.dataset.orig;
  });
  document.querySelectorAll("[data-en][data-zh]").forEach(el=>{
    el.textContent = zh ? el.dataset.zh : el.dataset.en;
  });
  document.querySelectorAll("[data-sess-n]").forEach(el=>{
    const n = +el.dataset.sessN;
    el.textContent = zh ? `第 ${n} 课` : `Session ${String(n).padStart(2, "0")}`;
  });
  document.querySelectorAll("[data-title-en][data-title-zh]").forEach(el=>{
    el.title = zh ? el.dataset.titleZh : el.dataset.titleEn;
  });
  document.querySelectorAll("[data-nb-embed]").forEach(btn=>{
    const open = btn.getAttribute("aria-expanded") === "true";
    btn.textContent = open ? (zh ? "▾ 收起笔记本" : "▾ Hide notebook")
                           : (zh ? btn.dataset.labelZh : btn.dataset.labelEn);
  });
  const lt = document.querySelector(".lang-toggle");
  if(lt) lt.textContent = zh ? "EN" : "中文";
  if(window._completeRefresh) window._completeRefresh();
  translateRendered();
}
function setupLang(){
  const btn = document.querySelector(".lang-toggle");
  if(btn) btn.addEventListener("click", ()=>{
    try{ localStorage.setItem(LANG_KEY, getLang() === "zh" ? "en" : "zh"); }catch{}
    applyLang();
  });
  applyLang();
}

/* ---------- completion button + nav checks ---------- */
function setupCompletion(){
  const btn = document.getElementById("complete-btn");
  const pageId = document.body.dataset.page;
  if(btn && pageId){
    const refresh = ()=>{ const d=isDone(pageId), zh=getLang()==="zh";
      btn.classList.toggle("is-done", d);
      btn.textContent = d ? (zh ? "✓ 已完成 —— 点击取消" : "✓ Completed — click to unmark")
                          : (zh ? "标记本课完成" : "Mark this session complete"); };
    window._completeRefresh = refresh;
    refresh();
    btn.addEventListener("click", ()=>{ setDone(pageId, !isDone(pageId)); refresh(); markNav(); });
  }
  markNav();
}
function markNav(){
  document.querySelectorAll(".nav-links a[data-page]").forEach(a=>{
    const done = isDone(a.dataset.page);
    let chk = a.querySelector(".chk");
    if(done && !chk){ chk=document.createElement("span"); chk.className="chk"; chk.textContent=" ✓"; a.appendChild(chk); }
    if(!done && chk) chk.remove();
  });
  // index cards
  document.querySelectorAll(".card[data-page]").forEach(c=>{
    c.classList.toggle("done", isDone(c.dataset.page));
  });
}

/* ---------- dark / light theme toggle ---------- */
function setupTheme(){
  const btn = document.querySelector(".theme-toggle");
  if(!btn) return;
  btn.addEventListener("click", ()=>{
    const next = document.documentElement.getAttribute("data-theme")==="dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try{ localStorage.setItem("lp.theme", next); }catch{}
  });
}

/* ---------- boot ---------- */
/* ---------- embedded JupyterLite notebook (lazy) ---------- */
function setupNotebookEmbed(){
  document.querySelectorAll("[data-nb-embed]").forEach(btn=>{
    const slot = btn.closest("[data-nb-src]");
    const holder = slot && slot.querySelector(".nb-embed");
    if(!slot || !holder) return;
    const src = slot.getAttribute("data-nb-src");
    btn.addEventListener("click", ()=>{
      const opening = holder.hasAttribute("hidden");
      if(opening){
        if(!holder.querySelector("iframe")){
          const f = document.createElement("iframe");
          f.src = src; f.loading = "lazy"; f.title = "Notebook (runs in your browser)";
          holder.appendChild(f);
        }
        holder.removeAttribute("hidden");
        btn.setAttribute("aria-expanded","true");
        btn.textContent = getLang() === "zh" ? "▾ 收起笔记本" : "▾ Hide notebook";
      } else {
        holder.setAttribute("hidden","");
        btn.setAttribute("aria-expanded","false");
        btn.textContent = getLang() === "zh" ? btn.dataset.labelZh : btn.dataset.labelEn;
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", ()=>{
  // Render every embedded markdown block into the div whose id is the script id
  // minus "-md" (e.g. lesson-a-md -> #lesson-a, practice-b-md -> #practice-b).
  document.querySelectorAll('script[type="text/markdown"]').forEach(s=>{
    if(s.id && s.id.endsWith("-md")) renderMarkdownInto(s.id, s.id.slice(0, -3));
  });
  buildPlaygrounds();
  setupNotebookEmbed();
  setupCompletion();
  setupTheme();
  setupLang();
});
