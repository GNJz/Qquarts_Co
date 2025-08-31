# -*- coding: utf-8 -*-
# cookiiePHAM_web.py — 로컬 3대장(쿠키팜) 웹 UI (한 파일)
# 필요: Ollama 실행 + 모델( llama3.1 / mistral-nemo / qwen2.5 )
# pip: python3 -m pip install fastapi uvicorn httpx sentence-transformers

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import httpx, asyncio, re
from sentence_transformers import SentenceTransformer, util
from collections import Counter

# ===== 임베딩 모델 로드 =====
_embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

app = FastAPI(title="cookiiePHAM · 3대장")

OLLAMA = "http://127.0.0.1:11434"
MODELS = {
    "GPT": ("llama3.1", "llama3.1"),
    "제미나이": ("mistral", "mistral-nemo"),
    "그록": ("qwen", "qwen2.5"),
}

# --------- Ollama 호출 ---------
async def ask_ollama(model: str, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120) as cli:
        r = await cli.post(
            f"{OLLAMA}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()

# --------- 종합 로직 (의미 기반) ---------
def synth(answers: dict) -> dict:
    try:
        texts = [answers.get("GPT", ""), answers.get("제미나이", ""), answers.get("그록", "")]
        if not any(texts):
            return {"final": "요약 불가", "agree": 0}

        # 의미 임베딩
        embs = _embed_model.encode(texts, convert_to_tensor=True)
        s01 = util.pytorch_cos_sim(embs[0], embs[1]).item()
        s02 = util.pytorch_cos_sim(embs[0], embs[2]).item()
        s12 = util.pytorch_cos_sim(embs[1], embs[2]).item()
        agree = round(((s01 + s02 + s12) / 3.0) * 100)

        # 공통 키워드
        def toks(t):
            return [w.lower() for w in re.findall(r"[A-Za-z가-힣0-9]{2,}", t)]
        bags = [set(toks(t)) for t in texts]
        freq = Counter()
        for bag in bags:
            freq.update(bag)
        commons = [w for w, c in freq.most_common() if c >= 2]
        common_top = ", ".join(commons[:8]) if commons else "없음"

        final = f"공통핵심: {common_top} · 동의도 ≈ {agree}%"
        return {"final": final, "agree": agree}

    except Exception:
        return {"final": "요약 중 오류 발생", "agree": 0}

# --------- API ---------
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    q = (data.get("question") or "").strip()
    if not q:
        return JSONResponse({"error": "질문이 비었습니다."}, status_code=400)

    # 3모델 병렬 호출
    tasks = [ask_ollama(m[1], q) for m in MODELS.values()]
    r = await asyncio.gather(*tasks, return_exceptions=True)

    keys = list(MODELS.keys())
    answers = {}
    for i, res in enumerate(r):
        label = keys[i]
        if isinstance(res, Exception):
            answers[label] = f"[오류] {type(res).__name__}: {res}"
        else:
            answers[label] = res

    return {"answers": answers, "synthesis": synth(answers)}

# --------- UI ---------
@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse("""
<!doctype html><html lang="ko"><meta charset="utf-8">
<title>cookiiePHAM · 3대장</title>
<style>
  *{box-sizing:border-box} body{font-family:system-ui,Apple SD Gothic Neo,sans-serif;margin:0;background:#0b0c10}
  .wrap{max-width:1100px;margin:28px auto;padding:16px}
  h1{color:#e9eef5;margin:0 0 12px;font-size:22px}
  .bar{display:flex;gap:8px}
  textarea{flex:1;padding:12px;border-radius:12px;border:1px solid #2b2f3a;background:#12141a;color:#e9eef5;height:90px}
  button{padding:12px 16px;border-radius:12px;border:0;background:#4f8cff;color:white;cursor:pointer}
  .grid{margin-top:12px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
  .card{background:#11141b;border:1px solid #262a36;border-radius:14px;padding:12px;min-height:240px;color:#dfe6f3}
  .ttl{font-weight:700;margin-bottom:6px;color:#9fb5ff}
  .meta{margin-top:10px;color:#b5bfd0}
  .gauge{height:8px;background:#22283a;border-radius:6px;overflow:hidden}
  .fill{height:100%;background:#6dd36d;width:0%}
  pre{white-space:pre-wrap;margin:0;font-family:ui-monospace,Menlo,monospace}
</style>
<div class="wrap">
  <h1>🍪 cookiiePHAM — 3대장 교차검증</h1>
  <div class="bar">
    <textarea id="q" placeholder="여기에 질문을 입력하세요. 예) K-pop 팬덤 경제의 핵심 수익원 3가지는?"></textarea>
    <button id="go">질문하기</button>
  </div>

  <div class="grid">
    <div class="card"><div class="ttl">GPT</div><pre id="a1">-</pre></div>
    <div class="card"><div class="ttl">제미나이</div><pre id="a2">-</pre></div>
    <div class="card"><div class="ttl">그록</div><pre id="a3">-</pre></div>
    <div class="card">
      <div class="ttl">쿠키팜 종합</div>
      <pre id="syn">-</pre>
      <div class="meta">동의도</div>
      <div class="gauge"><div id="gfill" class="fill"></div></div>
    </div>
  </div>
</div>
<script>
const qs = (s)=>document.querySelector(s);
qs('#go').onclick = async ()=>{
  const q = qs('#q').value.trim();
  if(!q){ alert('질문을 입력하세요'); return; }
  qs('#a1').textContent = qs('#a2').textContent = qs('#a3').textContent = '생성 중…';
  qs('#syn').textContent = '요약 중…';
  qs('#gfill').style.width = '0%';
  try{
    const r = await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({question:q})});
    const j = await r.json();
    if(j.error){ alert(j.error); return; }
    qs('#a1').textContent = j.answers["GPT"] || '-';
    qs('#a2').textContent = j.answers["제미나이"] || '-';
    qs('#a3').textContent = j.answers["그록"] || '-';
    qs('#syn').textContent = j.synthesis.final;
    qs('#gfill').style.width = (j.synthesis.agree||0) + '%';
  }catch(e){ alert('오류: '+e); }
};
</script>
</html>
""")