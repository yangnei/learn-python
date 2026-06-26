/* Python for Researchers — interactive site runtime.
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
  note.innerHTML = "These editors run real Python <strong>in your browser</strong> (via Pyodide) — nothing is installed and nothing leaves your machine. Edit the code, then press <strong>Run ▶</strong>. Predict the output first!";
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

/* ---------- completion button + nav checks ---------- */
function setupCompletion(){
  const btn = document.getElementById("complete-btn");
  const pageId = document.body.dataset.page;
  if(btn && pageId){
    const refresh = ()=>{ const d=isDone(pageId);
      btn.classList.toggle("is-done", d);
      btn.textContent = d ? "✓ Completed — click to unmark" : "Mark this session complete"; };
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

/* ---------- boot ---------- */
document.addEventListener("DOMContentLoaded", ()=>{
  renderMarkdownInto("lesson-md","lesson");
  renderMarkdownInto("practice-md","practice");
  renderMarkdownInto("quiz-md","quiz");
  renderMarkdownInto("cheats-md","cheats");
  buildPlaygrounds();
  setupCompletion();
});
