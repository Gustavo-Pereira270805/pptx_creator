#!/usr/bin/env python3
"""Cliente do Figma MCP (StreamableHTTP) para buscar inspirações de design.

Uso:
    python3 figma_mcp.py get --file-key <KEY> [--node-id <ID>] [--depth N] [--token figd_...]
    python3 figma_mcp.py images --file-key <KEY> --nodes <ID1,ID2> --local-path <dir> [--token figd_...]
    python3 figma_mcp.py tools [--token figd_...]

O token também pode vir de FIGMA_API_KEY (env) ou da flag --token.
O servidor MCP deve estar rodando em http://127.0.0.1:3333/mcp
(use ./start_figma_mcp.sh para iniciá-lo).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:3333/mcp"
_SID = None


def call(obj, token=None):
    global _SID
    body = json.dumps(obj).encode()
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if token:
        req.add_header("X-Figma-Token", token)
    if _SID:
        req.add_header("Mcp-Session-Id", _SID)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            if "Mcp-Session-Id" in resp.headers:
                _SID = resp.headers["Mcp-Session-Id"]
            raw = resp.read().decode()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:400]}")
    except urllib.error.URLError:
        raise SystemExit("Figma MCP indisponível. Rode ./start_figma_mcp.sh primeiro.")
    for line in raw.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(raw) if raw.strip() else {}


def tool_text(result):
    out = []
    for c in result.get("content", []):
        if c.get("type") == "text":
            out.append(c["text"])
        elif c.get("type") == "image":
            out.append(f"[imagem em {c.get('data', '?')[:30]}...]")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get")
    g.add_argument("--file-key", required=True)
    g.add_argument("--node-id", default=None)
    g.add_argument("--depth", type=int, default=None)
    g.add_argument("--token", default=None)

    i = sub.add_parser("images")
    i.add_argument("--file-key", required=True)
    i.add_argument("--nodes", required=True)
    i.add_argument("--local-path", required=True)
    i.add_argument("--token", default=None)

    t = sub.add_parser("tools")
    t.add_argument("--token", default=None)

    a = p.parse_args()
    token = a.token or os.environ.get("FIGMA_API_KEY")

    call({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "openhands", "version": "1.0"}}})
    call({"jsonrpc": "2.0", "method": "notifications/initialized"})

    if a.cmd == "tools":
        r = call({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        for t_ in r["result"]["tools"]:
            print(f"● {t_['name']}: {t_['description'][:100]}")
        return

    if a.cmd == "get":
        args = {"fileKey": a.file_key}
        if a.node_id:
            args["nodeId"] = a.node_id
        if a.depth is not None:
            args["depth"] = a.depth
        r = call({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                  "params": {"name": "get_figma_data", "arguments": args}}, token=token)
        text = tool_text(r.get("result", {}))
        if not text:
            print(json.dumps(r, indent=2)[:500])
            return
        # tenta parsear o texto como JSON de dados do Figma
        try:
            data = json.loads(text)
            out = a.file_key + ("-" + a.node_id if a.node_id else "") + ".json"
            with open(out, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Salvo em {out} ({len(text)} bytes)")
        except json.JSONDecodeError:
            print(text[:4000])

    if a.cmd == "images":
        r = call({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                  "params": {"name": "download_figma_images",
                             "arguments": {"fileKey": a.file_key,
                                           "nodes": a.nodes.split(","),
                                           "localPath": a.local_path}}}, token=token)
        print(tool_text(r.get("result", {}))[:2000])


if __name__ == "__main__":
    main()
