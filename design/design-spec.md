# Design Spec — Redesign Capacitação SIME (Sebrae/PB)

Fonte de inspiração: Figma **Pitch Deck** (`Adncq73gHMxPwOoBihEZ26`) — renders em
`figma-inspirations/`. Canvas: 13.333 × 7.5 in (16:9, 1920×1080 pt).

## Design System

| Token | Valor | Uso |
|---|---|---|
| `paper` | `#F2F3F2` | Fundo do slide |
| `white` | `#FFFFFF` | Cards, painéis |
| `navy` | `#0E2756` | Títulos, texto primário, geometric accents |
| `slate` | `#304258` | Subtítulos |
| `blue` | `#2353E9` | Acento assinatura: KPIs, chips, eyebrow, VS, destaques |
| `bright` | `#559AFF` | Acento secundário |
| `royal` | `#193BA7` | Footer / ênfase profunda |
| `steel` | `#6E7885` | Corpo de texto, metadados |
| `tint` | `#EAF1FF` | Fundo de callouts / dicas / alertas |
| `amber` | `#B4540A` | Texto de aviso (⚠️) sobre fundo tint |

Tipografia: **Poppins** — Bold 700 p/ títulos/eyebrow/números; Regular 400 p/ corpo.

| Papel | Tamanho |
|---|---|
| Hero (capa) | 40–48pt Bold navy |
| Título de seção | 24pt Bold navy |
| Eyebrow | 10.5pt Bold caps, blue, com quadrado-accento 9px stroke |
| Card title | 13pt Bold navy |
| Corpo | 10–11pt Regular steel/slate |
| KPI número | 60pt Bold blue |
| Footer | 8pt steel |

## Regras aplicadas (power-design)

- Safe-zone ≥0.5" nas 4 bordas; margens internas de card ≥0.3".
- Acento único: blue `#2353E9` (nunca >2 cores vibrantes por card).
- Contraste: navy sobre white/paper e white sobre navy ≥ WCAG AA.
- ≤7 chunks por slide; grids de 2/3/6 colunas com gap 0.25–0.35".
- Repetição: header (eyebrow + título + "Sebrae/PB" à direita) e footer (linha + metadado + número) em TODOS os slides.

## Arquétipos de layout (17 slides)

1. **Capa** — bg full-bleed (image1) + overlay navy à esquerda; eyebrow + hero 2-linha + subtítulo + objetivo.
2. **Conceitos (Atendimento ≠ Cliente Atendido)** — 2 cards imagem (Quem é contado / O que é contado) + painel "Exemplo Prático".
3. **Contraste de painéis** — 2 painéis (Foco na Operação / Foco no Território) + selo "VS".
4. **Matriz de Contabilização** — tabela 4×3 + chips ✔SIM/✘NÃO (colunas: Clientes Atendidos / Metas Mobilizadoras).
5. **As 6 Metas** — grid 3×2 de cards ícone + título + descrição.
6–11. **Metas 01–06 (template)** — coluna esquerda: blocos Q&A (O que medir / Quem entra / Como calcular / Desdobramento) + callout ⚠️; coluna direita: card KPI (número grande + nota) + imagem.
12. **Navegação (divisor)** — bg full-bleed; hero "Agora vamos para o SIME!" + citação + passos + chip "Acesso ao Sistema".
13. **Interface & Navegação** — card "Estrutura do Painel" (filtros) + card "Inteligência de Gestão" (4 perguntas) + dica rodapé.
14. **Acompanhamento** — card "Visualização Estratégica" (componentes) + card "Pergunta de Gestão" (citação) + lembrete.
15. **Desafio Prático** — card "Situação-Problema" + card "Plano de Trabalho" (6 passos ✔) + citação "proposta de gestão".
16. **Plano de Ação** — tabela 8 colunas (2 exemplos) + nota 📌 + estrutura 5 passos da DIREX.
17. **Conclusão** — card "Regras e Conceitos" + card "Gestão Orientada a Dados" + citação final + tagline "SIME ➔ Análise ➔ Decisão ➔ Ação ➔ Resultado".

## Motion (via `html-ppt/scripts/pptx_motion.py`)

- Entradas: eyebrow `appear`; título `fade` (+100ms); conteúdo em stagger `fade` (gap 150–180ms).
- KPI (slides 6–11): número `zoom` (after_previous).
- Transições: `fade` entre conteúdo; `push` nas viradas de capítulo (12); `morph` 6→7 (NPS→ME+EPP, mesma ideia evoluindo).
- Nenhum slide com coreografia >3s. Card denso (4, 16): sem animação interna.

## Entregáveis

- `build_deck.py` → `<deck>.pptx` + `motion-spec.json` → deck com animação.
- Renders: `renders/after/*.png` (comparar com `figma-inspirations/` e renders originais).
- Auditoria visual: subagente designer-vision (baseline = renders do deck ORIGINAL).
