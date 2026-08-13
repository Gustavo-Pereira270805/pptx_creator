#!/usr/bin/env bash
# Inicia o Figma MCP Server (StreamableHTTP) em background na porta 3333.
# O token pode ser informado via variável FIGMA_API_KEY ou flag --figma-api-key.
set -euo pipefail

PORT="${FIGMA_MCP_PORT:-3333}"
LOG=/tmp/figma-mcp.log
KEYFLAG=()
if [ -n "${FIGMA_API_KEY:-}" ]; then
  KEYFLAG=(--figma-api-key "$FIGMA_API_KEY")
fi

if pgrep -f "figma-developer-mcp" > /dev/null; then
  echo "Figma MCP já está rodando (porta $PORT). Log: $LOG"
  exit 0
fi

cd "$(dirname "$0")"
mkdir -p .figma-assets
setsid figma-developer-mcp --format json --port "$PORT" \
  --image-dir "$(pwd)/.figma-assets" --no-telemetry "${KEYFLAG[@]}" \
  > "$LOG" 2>&1 < /dev/null &

sleep 2
if pgrep -f "figma-developer-mcp" > /dev/null; then
  echo "✅ Figma MCP Server rodando em http://127.0.0.1:$PORT/mcp (log: $LOG)"
else
  echo "❌ Falha ao iniciar. Veja $LOG"
  exit 1
fi
