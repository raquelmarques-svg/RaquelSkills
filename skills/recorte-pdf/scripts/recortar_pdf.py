#!/usr/bin/env python3
"""
recortar_pdf.py — Recorta páginas ou regiões de um PDF como PNG.

Uso:
    python3 recortar_pdf.py --pdf CAMINHO --pages 3 --output PASTA
    python3 recortar_pdf.py --pdf CAMINHO --pages 3-7 --region superior --dpi 300
    python3 recortar_pdf.py --pdf CAMINHO --pages 3,7,12 --output PASTA

Regiões disponíveis: inteira | superior | inferior | central
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERRO: PyMuPDF não instalado. Execute: pip install pymupdf --break-system-packages")
    sys.exit(1)


def parse_pages(pages_str: str, total: int) -> list[int]:
    """Parseia '3', '3-7', '3,7,12' → lista de índices 0-based."""
    result = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            result.extend(range(int(start) - 1, int(end)))
        else:
            result.append(int(part) - 1)
    # Filtrar inválidos
    return [p for p in result if 0 <= p < total]


def get_clip(page, region: str):
    """Retorna rect de crop baseado na região solicitada."""
    r = page.rect
    margin = 10  # pixels de margem
    regions = {
        "inteira":   fitz.Rect(r.x0 + margin, r.y0 + margin, r.x1 - margin, r.y1 - margin),
        "superior":  fitz.Rect(r.x0 + margin, r.y0 + margin, r.x1 - margin, r.y1 * 0.5),
        "inferior":  fitz.Rect(r.x0 + margin, r.y1 * 0.5,   r.x1 - margin, r.y1 - margin),
        "central":   fitz.Rect(r.x0 + margin, r.y1 * 0.2,   r.x1 - margin, r.y1 * 0.8),
    }
    return regions.get(region, regions["inteira"])


def main():
    parser = argparse.ArgumentParser(description="Recorta páginas de PDF como PNG")
    parser.add_argument("--pdf",    required=True, help="Caminho do arquivo PDF")
    parser.add_argument("--pages",  required=True, help="Páginas: '3', '3-7' ou '3,7,12'")
    parser.add_argument("--region", default="inteira",
                        choices=["inteira", "superior", "inferior", "central"])
    parser.add_argument("--dpi",    type=int, default=150)
    parser.add_argument("--output", default=".", help="Diretório de saída")
    parser.add_argument("--prefix", default="recorte", help="Prefixo do nome do arquivo")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"ERRO: arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total = len(doc)
    page_indices = parse_pages(args.pages, total)

    if not page_indices:
        print(f"ERRO: nenhuma página válida no intervalo '{args.pages}' (total: {total})")
        sys.exit(1)

    zoom = args.dpi / 72  # fitz usa 72 DPI como base
    mat = fitz.Matrix(zoom, zoom)
    gerados = []

    for idx in page_indices:
        page = doc[idx]
        clip = get_clip(page, args.region)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        nome = f"{args.prefix}-p{idx+1:03d}-{args.region}.png"
        destino = out_dir / nome
        pix.save(str(destino))
        gerados.append(str(destino))
        print(f"  OK  p{idx+1:03d} → {destino}  ({pix.width}×{pix.height}px)")

    doc.close()
    print(f"\nTotal: {len(gerados)} arquivo(s) gerado(s) em {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
