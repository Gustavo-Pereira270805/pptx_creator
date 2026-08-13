# pptx_creator

Pipeline de criação de apresentações PPTX com um time de subagentes OpenHands especializados.

## Subagentes ('.agents/agents/')
- **slide-researcher** — pesquisa conteúdo/dados com fontes verificadas
- **slide-writer** — roteiro: narrativa, mensagem-chave e bullets por slide
- **slide-designer** — design visual validado por imagem (MiMo-V2.5 com visão, perfil `designer-vision`)
- **pptx-builder** — gera o `.pptx` final com python-pptx

## Ferramentas
- `render_pptx.sh` — renderização PPTX → PDF → PNG (LibreOffice + poppler-utils) para validação visual
- `AGENTS.md` — setup completo (skills, MCP server, pipeline)

## Requisitos
- Python 3 + python-pptx
- LibreOffice + poppler-utils
