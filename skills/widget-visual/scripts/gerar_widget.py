#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_widget.py — Gera blocos PNG para petições jurídicas.

Uso:
    python3 gerar_widget.py --tipo composicao-renda --titulo "Renda Familiar" \
        --dados '[{"membro":"Maria","parentesco":"Requerente","renda":0,"obs":""}]' \
        --output /path/saida --prefixo silva-joao

Tipos: composicao-renda | vinculos | linha-do-tempo | comparativo | tabela
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib import rcParams
except ImportError:
    print("ERRO: matplotlib não instalado. Execute: pip install matplotlib --break-system-packages")
    sys.exit(1)

# ── Paleta Almeida Marques ────────────────────────────────────────────────────
NAVY   = "#1B3A6B"
CREME  = "#F5F0E8"
CINZA  = "#E8E4DC"
TEXTO  = "#1A1A1A"
BRANCO = "#FFFFFF"
VERMELHO = "#C0392B"

rcParams["font.family"] = "DejaVu Sans"
rcParams["font.size"]   = 10


def titulo_png(ax_titulo, titulo: str):
    """Desenha barra de título navy com texto creme."""
    ax_titulo.set_facecolor(NAVY)
    ax_titulo.text(0.5, 0.5, titulo, ha="center", va="center",
                   fontsize=13, fontweight="bold", color=CREME,
                   transform=ax_titulo.transAxes)
    ax_titulo.axis("off")


def tabela_generica(ax, cabecalho: list, linhas: list):
    """Renderiza tabela N×M com cabeçalho navy."""
    n_cols = len(cabecalho)
    n_rows = len(linhas)
    total_rows = n_rows + 1

    for c, col in enumerate(cabecalho):
        ax.add_patch(mpatches.FancyBboxPatch(
            (c / n_cols, n_rows / total_rows), 1 / n_cols, 1 / total_rows,
            boxstyle="square,pad=0", linewidth=0.5,
            edgecolor=BRANCO, facecolor=NAVY, transform=ax.transAxes, clip_on=False
        ))
        ax.text((c + 0.5) / n_cols, (n_rows + 0.5) / total_rows, col,
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=CREME, transform=ax.transAxes)

    for r, linha in enumerate(linhas):
        bg = CREME if r % 2 == 0 else CINZA
        inv_r = n_rows - 1 - r
        for c, val in enumerate(linha):
            ax.add_patch(mpatches.FancyBboxPatch(
                (c / n_cols, inv_r / total_rows), 1 / n_cols, 1 / total_rows,
                boxstyle="square,pad=0", linewidth=0.3,
                edgecolor="#CCCCCC", facecolor=bg,
                transform=ax.transAxes, clip_on=False
            ))
            ax.text((c + 0.5) / n_cols, (inv_r + 0.5) / total_rows, str(val),
                    ha="center", va="center", fontsize=9,
                    color=TEXTO, transform=ax.transAxes)
    ax.axis("off")


def widget_composicao_renda(dados: list, titulo: str, output: Path, prefixo: str):
    membros = dados
    n = len(membros)
    total_renda = sum(float(m.get("renda", 0)) for m in membros)
    renda_pc = total_renda / (n if n > 0 else 1)
    sm_2026 = 1621.00
    limite_bpc = sm_2026 / 4

    cab = ["Membro", "Parentesco", "Renda Bruta (R$)", "Observação"]
    linhas = [[m["membro"], m["parentesco"],
               f"R$ {float(m.get('renda',0)):,.2f}".replace(",","X").replace(".",",").replace("X","."),
               m.get("obs", "")] for m in membros]
    linhas.append(["TOTAL", f"{n} membro(s)",
                   f"R$ {total_renda:,.2f}".replace(",","X").replace(".",",").replace("X","."), ""])
    linhas.append(["Renda per capita", "",
                   f"R$ {renda_pc:,.2f}".replace(",","X").replace(".",",").replace("X","."),
                   f"{'≤ ¼ SM ✓' if renda_pc <= limite_bpc else '> ¼ SM ✗'}"])

    altura = max(3.0, 0.6 * (n + 3))
    fig = plt.figure(figsize=(10, 0.8 + altura))
    ax_t = fig.add_axes([0, 0.88, 1, 0.12])
    ax_b = fig.add_axes([0.02, 0, 0.96, 0.86])
    titulo_png(ax_t, titulo)
    tabela_generica(ax_b, cab, linhas)

    nome = f"{prefixo}-composicao-renda-{date.today().strftime('%Y%m%d')}.png"
    dest = output / nome
    fig.savefig(str(dest), dpi=150, bbox_inches="tight", facecolor=BRANCO)
    plt.close(fig)
    return dest


def widget_vinculos(dados: list, titulo: str, output: Path, prefixo: str):
    cab = ["Empresa", "Função", "CNAE", "Admissão", "Rescisão", "Remuneração"]
    linhas = [[v.get("empresa",""), v.get("funcao",""), v.get("cnae",""),
               v.get("admissao",""), v.get("rescisao",""), v.get("remuneracao","")]
              for v in dados]

    altura = max(2.5, 0.5 * len(dados) + 1.5)
    fig = plt.figure(figsize=(12, 0.8 + altura))
    ax_t = fig.add_axes([0, 0.88, 1, 0.12])
    ax_b = fig.add_axes([0.01, 0, 0.98, 0.86])
    titulo_png(ax_t, titulo)
    tabela_generica(ax_b, cab, linhas)

    nome = f"{prefixo}-vinculos-{date.today().strftime('%Y%m%d')}.png"
    dest = output / nome
    fig.savefig(str(dest), dpi=150, bbox_inches="tight", facecolor=BRANCO)
    plt.close(fig)
    return dest


def widget_linha_do_tempo(dados: list, titulo: str, output: Path, prefixo: str):
    dados_s = sorted(dados, key=lambda x: x.get("data", ""))
    cab = ["Data", "Evento", "Dimensão"]
    linhas = [[d.get("data",""), d.get("evento",""), d.get("dimensao","")]
              for d in dados_s]

    altura = max(2.5, 0.45 * len(dados) + 1.5)
    fig = plt.figure(figsize=(10, 0.8 + altura))
    ax_t = fig.add_axes([0, 0.88, 1, 0.12])
    ax_b = fig.add_axes([0.02, 0, 0.96, 0.86])
    titulo_png(ax_t, titulo)
    tabela_generica(ax_b, cab, linhas)

    nome = f"{prefixo}-linha-do-tempo-{date.today().strftime('%Y%m%d')}.png"
    dest = output / nome
    fig.savefig(str(dest), dpi=150, bbox_inches="tight", facecolor=BRANCO)
    plt.close(fig)
    return dest


def widget_comparativo(dados: dict, titulo: str, output: Path, prefixo: str):
    cab = dados.get("cabecalho", ["Item", "Coluna A", "Coluna B"])
    linhas = dados.get("linhas", [])

    altura = max(2.5, 0.5 * len(linhas) + 1.5)
    fig = plt.figure(figsize=(10, 0.8 + altura))
    ax_t = fig.add_axes([0, 0.88, 1, 0.12])
    ax_b = fig.add_axes([0.02, 0, 0.96, 0.86])
    titulo_png(ax_t, titulo)
    tabela_generica(ax_b, cab, linhas)

    nome = f"{prefixo}-comparativo-{date.today().strftime('%Y%m%d')}.png"
    dest = output / nome
    fig.savefig(str(dest), dpi=150, bbox_inches="tight", facecolor=BRANCO)
    plt.close(fig)
    return dest


def widget_tabela(dados: dict, titulo: str, output: Path, prefixo: str):
    cab = dados.get("cabecalho", [])
    linhas = dados.get("linhas", [])
    if not cab:
        raise ValueError("'tabela' requer campo 'cabecalho' em dados")

    altura = max(2.5, 0.5 * len(linhas) + 1.5)
    n_cols = len(cab)
    fig = plt.figure(figsize=(max(8, n_cols * 2), 0.8 + altura))
    ax_t = fig.add_axes([0, 0.88, 1, 0.12])
    ax_b = fig.add_axes([0.02, 0, 0.96, 0.86])
    titulo_png(ax_t, titulo)
    tabela_generica(ax_b, cab, linhas)

    nome = f"{prefixo}-tabela-{date.today().strftime('%Y%m%d')}.png"
    dest = output / nome
    fig.savefig(str(dest), dpi=150, bbox_inches="tight", facecolor=BRANCO)
    plt.close(fig)
    return dest


GERADORES = {
    "composicao-renda": widget_composicao_renda,
    "vinculos":         widget_vinculos,
    "linha-do-tempo":   widget_linha_do_tempo,
    "comparativo":      widget_comparativo,
    "tabela":           widget_tabela,
}


def main():
    parser = argparse.ArgumentParser(description="Gera blocos PNG para petições jurídicas")
    parser.add_argument("--tipo",    required=True, choices=list(GERADORES.keys()))
    parser.add_argument("--titulo",  required=True)
    parser.add_argument("--dados",   required=True, help="JSON string com os dados")
    parser.add_argument("--output",  default=".")
    parser.add_argument("--prefixo", default="caso")
    args = parser.parse_args()

    try:
        dados = json.loads(args.dados)
    except json.JSONDecodeError as e:
        print(f"ERRO: JSON inválido em --dados: {e}")
        sys.exit(1)

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    gerador = GERADORES[args.tipo]
    try:
        dest = gerador(dados, args.titulo, output, args.prefixo)
        size = dest.stat().st_size
        print(f"OK  {dest}  ({size} bytes)")
    except Exception as e:
        print(f"ERRO ao gerar widget '{args.tipo}': {e}")
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
