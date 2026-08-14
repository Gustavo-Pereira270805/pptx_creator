# PPTX Motion — Coreografia de animação para o entregável `.pptx`

> Complemento do html-ppt para a **camada de entrega nativa** (PowerPoint).
> As animações CSS/FX do html-ppt só existem no deck HTML. Para o `.pptx`
> final, este guia + `scripts/pptx_motion.py` injetam **entrance animations**
> e **transições** (incluindo **Morph**) diretamente no XML do slide.

## Filosofia (regra de ouro)

**Motion transmite significado, não decora.** Use movimento para mostrar
hierarquia (o que entra primeiro), sequência (o que vem depois) e ênfase
(o que é o número-chave). Se a animação não ajuda a contar a história, remova.

## Choreografia por tipo de slide

| Tipo de slide | Padrão de motion |
|---|---|
| **Capa** | Título `fade` (0.5s) → subtítulo `fade` com 150ms de delay. Nada chamativo. |
| **Agenda / Sumário** | Itens em **stagger**: 1º `fade`, depois cada item `fade` com `after_previous` + 150–200ms. Total < 2s. |
| **Seção / divisor** | Elemento único `zoom` (0.5s) ou `fade`. Transição de entrada: `fade`. |
| **Conteúdo / bullets** | Bullets em stagger (mesmo padrão da agenda). Título `appear` ou `fade` antes. |
| **Dados / KPI** | Número-chave `zoom` (0.6s) + legenda `fade` com 200ms. **Nunca** animar gráfico inteiro; destaque um dado. |
| **Comparação** | Duas colunas `fade` com 150ms de delay entre elas (mostra contraste). |
| **Citação** | Citação `fade` + leve `zoom` (1.02) no elemento. Sem stagger. |
| **Encerramento / CTA** | CTA `fade` (0.5s). Se houver múltiplos passos, stagger curto. |

## Timing, easing, duração

- **Duração**: entrance 400–600ms (fade 500ms; zoom 600ms). Mais que 700ms = lento.
- **Stagger**: 150–250ms entre elementos da mesma sequência.
- **Total do slide**: a coreografia completa deve terminar em ≤ 3s. Se passar, corte efeitos.
- **Trigger por padrão**: `after_previous` (a apresentação flui sozinha). Use `on_click` só quando o conteúdo precisa ser revelado passo a passo pelo apresentador.
- **Reduzido-motion**: para público que pedir, usar `appear`/`none` em tudo.

## Transições entre slides

| Transição | Uso |
|---|---|
| **Morph** | Mesma ideia evoluindo (ex.: passo 1 → passo 2 de um processo; mapa → detalhe). O efeito mais "wow" e profissional. |
| **Fade** | Continuidade (seções de conteúdo sequencial). Padrão seguro. |
| **Push** | Mudança de capítulo/seção (sensação de avanço). |
| **Wipe** | Timeline/progressão (raro; usar com parcimônia). |
| **None** | Conteúdo denso (tabelas, código) — movimento distrai. |

## Anti-padrões (nunca)

- ❌ Animar **tudo** (bolas, spinners, bounce, spin) — parece template amador.
- ❌ Animação por **palavra** em parágrafos longos.
- ❌ `zoom` em slides de conteúdo denso (causa enjoo).
- ❌ Stagger > 8 elementos (ninguém espera).
- ❌ Mixar 5 tipos de transição no mesmo deck (escolha 1–2).
- ❌ Motion sem propósito em deck executivo/corporativo (Sebrae, governo, conselho).

## Uso do script (`scripts/pptx_motion.py`)

```bash
# Animação individual
python3 scripts/pptx_motion.py deck.pptx --entrance 3 fade after_previous --out deck_motion.pptx

# Transição
python3 scripts/pptx_motion.py deck.pptx --transition fade --slide 2 --out deck_motion.pptx

# Spec de motion (recomendado — coreografia declarativa em JSON)
python3 scripts/pptx_motion.py deck.pptx --spec motion-spec.json --out deck_motion.pptx
```

Spec JSON (mesma filosofia do design-spec — o pptx-builder declara e o script aplica):

```json
{
  "transitions": { "default": "fade", "2": "none", "5": "push" },
  "morph_pairs": [["6", "7"]],
  "slides": {
    "1": [
      {"shape": "Título", "effect": "fade", "trigger": "after_previous"},
      {"shape": "Subtítulo", "effect": "fade", "trigger": "after_previous", "delay_ms": 150}
    ],
    "2": {"stagger": {"shapes": ["item1", "item2", "item3"], "effect": "fade", "gap_ms": 180}}
  }
}
```

O script casa shapes por **nome** (ou índice), injeta `<p:timing>` e `<p:transition>`
no XML e salva um `.pptx` válido. Depois valide com `./render_pptx.sh` — se o XML
estiver malformado, o LibreOffice quebra o render.

## Checklist do pptx-builder

- [ ] Spec de motion declarada no `design/design-spec.md` (seção "Motion").
- [ ] Transições: no máximo 2 tipos; Morph só para "mesma ideia evoluindo".
- [ ] Nenhum slide com coreografia > 3s.
- [ ] Renders validados com visão após aplicar motion (nada quebrou, layout intacto).
- [ ] Deck abre no PowerPoint (valide abrindo manualmente ou com `p:timing` bem-formado).
