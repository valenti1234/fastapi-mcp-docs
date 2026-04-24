from __future__ import annotations

from html import escape


def render_index_html(*, docs_url: str) -> str:
    base = docs_url.rstrip("/")
    schema_url = f"{base}/schema"
    call_url = f"{base}/call"
    config_url = f"{base}/config"

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MCP Docs</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #0b0f16;
        --panel: #0f1623;
        --muted: #93a4bf;
        --text: #e7eefc;
        --border: #1f2a3d;
        --accent: #7aa2ff;
        --danger: #ff6b6b;
        --ok: #49d49d;
        --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
        --radius: 14px;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: var(--sans);
        background: radial-gradient(1000px 700px at 10% 10%, rgba(122,162,255,0.08), transparent 50%),
                    radial-gradient(900px 600px at 90% 0%, rgba(73,212,157,0.06), transparent 55%),
                    var(--bg);
        color: var(--text);
      }}
      a {{ color: var(--accent); text-decoration: none; }}
      header {{
        position: sticky;
        top: 0;
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 18px;
        border-bottom: 1px solid var(--border);
        background: rgba(11,15,22,0.85);
        backdrop-filter: blur(10px);
      }}
      header .title {{
        display: flex;
        gap: 10px;
        align-items: baseline;
      }}
      header h1 {{
        font-size: 16px;
        letter-spacing: 0.6px;
        margin: 0;
      }}
      header .meta {{
        font-size: 12px;
        color: var(--muted);
      }}
      .wrap {{
        display: grid;
        grid-template-columns: 340px 1fr;
        min-height: calc(100vh - 56px);
      }}
      aside {{
        border-right: 1px solid var(--border);
        background: rgba(15,22,35,0.6);
      }}
      main {{
        padding: 18px;
      }}
      .panel {{
        background: rgba(15,22,35,0.7);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
      }}
      .panel .hd {{
        padding: 12px 14px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }}
      .panel .bd {{
        padding: 12px 14px;
      }}
      .btn {{
        border: 1px solid var(--border);
        background: rgba(122,162,255,0.08);
        color: var(--text);
        padding: 8px 10px;
        border-radius: 10px;
        font-size: 12px;
        cursor: pointer;
      }}
      .btn:hover {{ border-color: rgba(122,162,255,0.6); }}
      .btn:active {{ transform: translateY(1px); }}
      .btn.secondary {{
        background: rgba(147,164,191,0.07);
      }}
      .search {{
        width: 100%;
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: rgba(11,15,22,0.6);
        color: var(--text);
        outline: none;
      }}
      .tools {{
        display: flex;
        flex-direction: column;
        gap: 8px;
      }}
      .tool-item {{
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: rgba(11,15,22,0.35);
        cursor: pointer;
      }}
      .tool-item:hover {{ border-color: rgba(122,162,255,0.45); }}
      .tool-item.active {{ border-color: rgba(122,162,255,0.85); background: rgba(122,162,255,0.09); }}
      .tool-item .name {{ font-family: var(--mono); font-size: 13px; }}
      .tool-item .desc {{ color: var(--muted); font-size: 12px; margin-top: 4px; line-height: 1.25; }}
      .grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }}
      .kv {{
        display: grid;
        grid-template-columns: 120px 1fr;
        gap: 10px;
        font-size: 13px;
        align-items: start;
      }}
      .kv .k {{ color: var(--muted); }}
      pre {{
        margin: 0;
        font-family: var(--mono);
        font-size: 12px;
        line-height: 1.35;
        white-space: pre-wrap;
        word-break: break-word;
      }}
      textarea {{
        width: 100%;
        min-height: 120px;
        border-radius: 12px;
        border: 1px solid var(--border);
        padding: 10px 12px;
        background: rgba(11,15,22,0.6);
        color: var(--text);
        font-family: var(--mono);
        font-size: 12px;
        outline: none;
      }}
      .status {{
        font-size: 12px;
        color: var(--muted);
        display: flex;
        gap: 10px;
        align-items: center;
      }}
      .dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--muted);
      }}
      .dot.ok {{ background: var(--ok); }}
      .dot.bad {{ background: var(--danger); }}
      @media (max-width: 980px) {{
        .wrap {{ grid-template-columns: 1fr; }}
        aside {{ border-right: none; border-bottom: 1px solid var(--border); }}
      }}
    </style>
  </head>
  <body>
    <header>
      <div class="title">
        <h1>MCP Docs</h1>
        <div class="meta">Embedded MCP documentation UI</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <button class="btn secondary" id="btnExport">Export mcp.json</button>
        <button class="btn" id="btnReload">Reload schema</button>
      </div>
    </header>

    <div class="wrap">
      <aside>
        <div style="padding:14px;">
          <input class="search" id="search" placeholder="Search tools…" />
        </div>
        <div style="padding:0 14px 14px 14px;">
          <div class="status" id="status"><span class="dot" id="statusDot"></span><span id="statusText">Loading…</span></div>
        </div>
        <div style="padding:0 14px 18px 14px;">
          <div class="tools" id="tools"></div>
        </div>
      </aside>

      <main>
        <div class="panel" style="margin-bottom:12px;">
          <div class="hd">
            <div style="display:flex;flex-direction:column;gap:3px">
              <div style="font-family:var(--mono);font-size:13px" id="toolName">Select a tool</div>
              <div style="color:var(--muted);font-size:12px" id="toolDesc"></div>
            </div>
            <div style="display:flex;gap:8px;">
              <button class="btn secondary" id="btnCopyReq">Copy request</button>
              <button class="btn secondary" id="btnCopyResp">Copy response</button>
              <button class="btn" id="btnCall">Call tool</button>
            </div>
          </div>
          <div class="bd">
            <div class="grid">
              <div class="panel">
                <div class="hd"><div>Input schema</div></div>
                <div class="bd"><pre id="inputSchema"></pre></div>
              </div>
              <div class="panel">
                <div class="hd"><div>Output schema</div></div>
                <div class="bd"><pre id="outputSchema"></pre></div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid">
          <div class="panel">
            <div class="hd"><div>JSON request</div></div>
            <div class="bd">
              <textarea id="req"></textarea>
            </div>
          </div>
          <div class="panel">
            <div class="hd"><div>JSON response</div></div>
            <div class="bd">
              <textarea id="resp" readonly></textarea>
            </div>
          </div>
        </div>
      </main>
    </div>

    <script>
      const schemaUrl = {escape(schema_url)!r};
      const callUrl = {escape(call_url)!r};
      const configUrl = {escape(config_url)!r};

      const els = {{
        tools: document.getElementById("tools"),
        search: document.getElementById("search"),
        toolName: document.getElementById("toolName"),
        toolDesc: document.getElementById("toolDesc"),
        inputSchema: document.getElementById("inputSchema"),
        outputSchema: document.getElementById("outputSchema"),
        req: document.getElementById("req"),
        resp: document.getElementById("resp"),
        statusText: document.getElementById("statusText"),
        statusDot: document.getElementById("statusDot"),
        btnReload: document.getElementById("btnReload"),
        btnCall: document.getElementById("btnCall"),
        btnCopyReq: document.getElementById("btnCopyReq"),
        btnCopyResp: document.getElementById("btnCopyResp"),
        btnExport: document.getElementById("btnExport"),
      }};

      let schema = null;
      let activeTool = null;

      function setStatus(kind, text) {{
        els.statusText.textContent = text;
        els.statusDot.className = "dot" + (kind === "ok" ? " ok" : kind === "bad" ? " bad" : "");
      }}

      function pretty(x) {{
        try {{
          return JSON.stringify(x ?? null, null, 2);
        }} catch (e) {{
          return String(x);
        }}
      }}

      function safeParse(text) {{
        try {{
          return [true, JSON.parse(text)];
        }} catch (e) {{
          return [false, e?.message || String(e)];
        }}
      }}

      function renderTools() {{
        const q = (els.search.value || "").trim().toLowerCase();
        const tools = (schema?.tools || []).filter(t => !q || (t.name || "").toLowerCase().includes(q));
        els.tools.innerHTML = "";
        for (const t of tools) {{
          const div = document.createElement("div");
          div.className = "tool-item" + (activeTool?.name === t.name ? " active" : "");
          div.innerHTML = `<div class="name">${{escapeHtml(t.name)}}</div><div class="desc">${{escapeHtml(t.description || "")}}</div>`;
          div.onclick = () => selectTool(t.name);
          els.tools.appendChild(div);
        }}
      }}

      function escapeHtml(s) {{
        return String(s)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }}

      function selectTool(name) {{
        activeTool = (schema?.tools || []).find(t => t.name === name) || null;
        renderTools();
        els.toolName.textContent = activeTool?.name || "Select a tool";
        els.toolDesc.textContent = activeTool?.description || "";
        els.inputSchema.textContent = pretty(activeTool?.input_schema || {{}});
        els.outputSchema.textContent = pretty(activeTool?.output_schema || {{}});
        els.req.value = pretty({{ tool: activeTool?.name || "", arguments: {{}} }});
        els.resp.value = "";
      }}

      async function loadSchema() {{
        setStatus("loading", "Loading schema…");
        try {{
          const r = await fetch(schemaUrl, {{ headers: {{ "accept": "application/json" }} }});
          if (!r.ok) throw new Error(`schema: HTTP ${{r.status}}`);
          schema = await r.json();
          setStatus("ok", `Loaded ${{(schema?.tools || []).length}} tools`);
          renderTools();
          if (!activeTool && (schema?.tools || []).length) {{
            selectTool(schema.tools[0].name);
          }}
        }} catch (e) {{
          setStatus("bad", e?.message || String(e));
        }}
      }}

      async function callTool() {{
        const [ok, parsed] = safeParse(els.req.value);
        if (!ok) {{
          els.resp.value = pretty({{ ok: false, error: `Invalid JSON: ${{parsed}}` }});
          return;
        }}
        try {{
          els.resp.value = "Calling…";
          const r = await fetch(callUrl, {{
            method: "POST",
            headers: {{ "content-type": "application/json", "accept": "application/json" }},
            body: JSON.stringify(parsed),
          }});
          const out = await r.json().catch(() => ({{ ok: false, error: `HTTP ${{r.status}}` }}));
          els.resp.value = pretty(out);
        }} catch (e) {{
          els.resp.value = pretty({{ ok: false, error: e?.message || String(e) }});
        }}
      }}

      async function exportConfig() {{
        try {{
          const r = await fetch(configUrl, {{ headers: {{ "accept": "application/json" }} }});
          const cfg = await r.json();
          const text = pretty(cfg);
          await navigator.clipboard.writeText(text);
          setStatus("ok", "Copied mcp.json to clipboard");
        }} catch (e) {{
          setStatus("bad", e?.message || String(e));
        }}
      }}

      async function copyTextFrom(el) {{
        try {{
          await navigator.clipboard.writeText(el.value || "");
          setStatus("ok", "Copied to clipboard");
        }} catch (e) {{
          setStatus("bad", e?.message || String(e));
        }}
      }}

      els.search.addEventListener("input", () => renderTools());
      els.btnReload.onclick = () => loadSchema();
      els.btnCall.onclick = () => callTool();
      els.btnExport.onclick = () => exportConfig();
      els.btnCopyReq.onclick = () => copyTextFrom(els.req);
      els.btnCopyResp.onclick = () => copyTextFrom(els.resp);

      loadSchema();
    </script>
  </body>
</html>
"""

