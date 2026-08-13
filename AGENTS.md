# AGENTS.md

## Ambiente de criação de apresentações PPTX

### Ferramentas instaladas
- **python-pptx 1.0.2** — biblioteca núcleo para gerar/editar `.pptx` (Python 3.13, instalada no sistema).
- **office-powerpoint-mcp-server 2.0.7** — MCP server de PowerPoint (37 ferramentas: create_presentation, add_slide, add_table, add_chart, apply_professional_design, auto_generate_presentation, etc.).
  - Instalado em venv isolado: `/workspace/project/.venv-mcp/`
  - Executar via: `/workspace/project/.venv-mcp/bin/ppt_mcp_server` (stdio, protocolo MCP JSON-RPC)
  - **Importante**: o venv usa `mcp<2` pois o pacote exige `mcp.server.fastmcp` (removido no mcp 2.0).

### Skills relevantes
- **theme-factory** — 10 temas prontos com cores/fontes para slides. Showcase em `theme-showcase.pdf` (cópia no workspace). Temas em `/home/openhands/.openhands/cache/skills/public-skills/skills/theme-factory/themes/`.
- **frontend-design** — princípios de design visual de alta qualidade (evitar estética genérica de IA).
- **technical-writing** / **plain-english-content** — qualidade de texto e conteúdo.

### Skills de design de apresentações importadas (`.agents/skills/`)
| Skill | Origem (⭐) | Uso |
|---|---|---|
| `frontend-slides` | zarazhangrui/frontend-slides (~27k) | Apresentações HTML 16:9 com animações; converte PPTX→web |
| `guizang-ppt-skill` | op7418/guizang-ppt-skill (~24k) | Web PPT de alto nível: estilo "revista × e-ink" e "Swiss Style" |
| `design-taste-frontend` | leonxlnx/taste-skill (~76k) | Anti-"AI slop": direciona o design para algo não-templated |
| `corporate` | bergside/awesome-design-skills | Estética corporativa: grids, layouts minimalistas, padrões enterprise |
| `premium` | bergside/awesome-design-skills | Estética premium estilo Apple: espaçamento preciso, tipografia refinada |

Fluxo recomendado: definir a estética com `corporate`/`premium`/`design-taste-frontend` → cores/fontes via `theme-factory` → gerar HTML de preview com `frontend-slides`/`guizang-ppt-skill` → validar por imagem → converter para `.pptx` final.

### MCPs
- **Tavily** — MCP de pesquisa web (já conectado na sessão): `tavily_tavily_search`, `tavily_tavily_extract`, `tavily_tavily_research`, etc. Útil para levantar conteúdo/dados para a apresentação.
- **Office-PowerPoint-MCP-Server** — MCP local de manipulação de PPTX (via venv acima).
- **Figma MCP** — inspirações de design diretamente do Figma (arquivos, componentes, estilos).
  - Servidor: `figma-developer-mcp` v0.13.2 (npm, instalado globalmente) — modo StreamableHTTP em `http://127.0.0.1:3333/mcp`.
  - Iniciar: `./start_figma_mcp.sh` (background, log em `/tmp/figma-mcp.log`; aceita `FIGMA_API_KEY` env ou flag `--figma-api-key`).
  - Cliente CLI: `python3 figma_mcp.py get --file-key <KEY> [--node-id <ID>] [--depth N] [--token figd_...]` / `images ...` / `tools`.
  - **Auth**: Personal Access Token do Figma via header `X-Figma-Token` (por request) ou `--figma-api-key` no servidor. Sem token → `403 Invalid token`.
  - Ferramentas: `get_figma_data` (fileKey obrigatório; nodeId/depth opcionais) e `download_figma_images` (nodes + localPath).
  - O token NÃO deve ser commitado (fica em `.env`/variável de ambiente ou passado por request).
  - **Limitações**: arquivos da **Comunidade** e **Figma Slides** (`/slides/`) não são acessíveis via REST API (comunidade exige OAuth; slides retorna `400 File type not supported`). Para acessá-los, o usuário deve duplicar para Rascunhos (o link muda para `/design/<key>/`).

### Inspiração de design capturada (Figma)
- **Pitch Deck template** (pyrstudio/omar.vaceem): file key `Adncq73gHMxPwOoBihEZ26`.
  - Dados brutos: `Adncq73gHMxPwOoBihEZ26.json` (476 KB)
  - Renders dos 11 slides: `figma-inspirations/*.png` + `contact-sheet.png`
  - Design system: `figma-inspirations/design-system.md`
  - Tema gerado: `figma-pitch-deck` no theme-factory (Paper White `#F2F3F2`, Navy `#0E2756`, Vibrant Blue `#2353E9`, Steel Gray `#6E7885`; Poppins Bold 700 / Regular 400).
  - Uso: `render_pptx.sh` + build_deck.py com tema figma-pitch-deck.

### Pipeline de renderização (validação visual dos slides)
- **LibreOffice** (`/usr/bin/soffice`) + **poppler-utils** (`pdftoppm`) instalados via apt.
- **IMPORTANTE**: o `LD_LIBRARY_PATH` do ambiente quebra o soffice. Sempre prefixar:
  `LD_LIBRARY_PATH=/usr/lib/libreoffice/program soffice --headless --convert-to pdf --outdir <dir> <arquivo.pptx>`
- Script pronto: `./render_pptx.sh <arquivo.pptx> <dir_saida> [dpi]` (gera um PNG por slide).
- **Atenção Python**: o `/usr/local/bin/python3` só lê `/usr/local/lib/python3.13/dist-packages`.
  - `python-pptx 1.0.2` instalado em `dist-packages` (via `pip --target`). Funciona com `python3`.
  - O MCP server de PowerPoint continua no venv: `/workspace/project/.venv-mcp/` (com python-pptx próprio).
  - Se `import pptx` falhar, reinstalar: `sudo /usr/local/bin/python3 -m pip install --target /usr/local/lib/python3.13/dist-packages python-pptx`

### Uso típico
1. Escolher tema via theme-factory (ou criar tema customizado).
2. Gerar conteúdo (tavily para pesquisa, se necessário).
3. Criar o `.pptx` com python-pptx diretamente OU através do MCP server (`ppt_mcp_server`) via stdio JSON-RPC.
4. Validar visualmente: `./render_pptx.sh deck.pptx renders/` e inspecionar os PNGs (modelo com visão).

## Time de subagentes (`.agents/agents/`)

Pipeline de criação de apresentação — orquestrar em ordem:

| Subagente | Função | Tools | Modelo |
|---|---|---|---|
| `slide-researcher` | Pesquisa conteúdo/dados com fontes | `browser_tool_set`, `file_editor` | inherit |
| `slide-writer` | Roteiro: narrativa, mensagem e bullets por slide | — | inherit |
| `slide-designer` | Design visual + validação por imagem (preview HTML + screenshot) | `browser_tool_set`, `terminal`, `file_editor` | `designer-vision` (MiMo-V2.5) |
| `pptx-builder` | Gera o `.pptx` com python-pptx e valida com render | `terminal`, `file_editor` | inherit |

Artefatos: `research/research-notes.md` → `outline/slides-outline.md` → `design/design-spec.md` (+ `design/preview.html/png`) → `<deck>.pptx` (+ `renders/`).

### Perfil LLM `designer-vision` (MiMo-V2.5 via OpenCode Go)
- Arquivo: `.openhands/profiles/designer-vision.json` (referenciado por `model: designer-vision` + `profile_store_dir` no subagente).
- Endpoint: `https://opencode.ai/zen/go/v1` (OpenAI-compatible) — model id `mimo-v2.5` (sem prefixo `xiaomi/`).
- Chave: do OpenCode Go do usuário (mesma chave serve para Zen e Go).
- **IMPORTANTE**: o Cloudflare do opencode.ai bloqueia User-Agents de Python padrão (403 error 1010). O perfil já inclui `extra_headers.User-Agent` de navegador.
- MiMo é reasoning model: responde em `message.reasoning` + `message.content`; precisa de `max_tokens` alto (perfil usa 8192).
- Modelos alternativos no Go: `mimo-v2.5-pro`, `mimo-v2-pro`, `mimo-v2-omni`. No Zen (pay-per-use): `mimo-v2.5-free`.
