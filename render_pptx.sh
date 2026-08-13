#!/usr/bin/env bash
# Renderiza um .pptx em imagens PNG (um por slide) usando LibreOffice + poppler.
# Uso: ./render_pptx.sh <arquivo.pptx> <dir_saida> [dpi]
set -euo pipefail

INPUT="${1:?uso: render_pptx.sh <arquivo.pptx> <dir_saida> [dpi]}"
OUTDIR="${2:?uso: render_pptx.sh <arquivo.pptx> <dir_saida> [dpi]}"
DPI="${3:-80}"

mkdir -p "$OUTDIR"
BASE="$(basename "$INPUT" .pptx)"
echo "==> Convertendo para PDF..."
LD_LIBRARY_PATH=/usr/lib/libreoffice/program soffice --headless \
    --convert-to pdf --outdir "$OUTDIR" "$INPUT" >/dev/null
echo "==> Convertendo PDF para PNG..."
pdftoppm -png -r "$DPI" "$OUTDIR/$BASE.pdf" "$OUTDIR/$BASE"
echo "==> Pronto: $OUTDIR/$BASE-*.png"
