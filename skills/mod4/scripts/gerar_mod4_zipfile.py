#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_mod4_zipfile.py — Gerador canônico de DOCX para o escritório Almeida Marques
Versão: 4.3.0 | Data: 2026-05-14
Método: zipfile direto sobre template_mod4.docx (LD5, L22)

USO BÁSICO
----------
from gerar_mod4_zipfile import gerar_docx, substituir_xml

# Mapa de substituições no formato {">placeholder<": ">valor_final<"}
subs = {
    ">CLIENTE_NOME<":  ">Maria da Silva<",
    ">PROCESSO_NUM<":  ">1050182-30.2024.8.26.0002<",
    ">DATA_ASSIN<":    ">14 de maio de 2026<",
}
gerar_docx(
    template_path="/caminho/para/template_mod4.docx",
    substituicoes=subs,
    dest_path="/tmp/peticao.docx"
)

REGRAS APLICADAS
----------------
LD5: zipfile direto — nunca python-docx ou gerar_mod4.py
LD6: placeholders intermediários para cadeias de substituição
LD7: padrão >texto< em vez de tag completa <w:t>texto</w:t>
L22: método padrão permanente; gerar_mod4.py descontinuado
L23: str.replace reprocessa o próprio output — usar tokens
L24: Word gera <w:t xml:space="preserve"> que quebra busca por tag completa
"""

import argparse
import io
import json
import os
import shutil
import zipfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------

def ler_template(template_path: str) -> dict:
    """Lê todos os membros do ZIP em memória como {nome: bytes}."""
    with zipfile.ZipFile(template_path, "r") as zin:
        return {name: zin.read(name) for name in zin.namelist()}


def substituir_xml(doc: str, substituicoes: dict) -> str:
    """
    Aplica substituições em word/document.xml.

    Regra LD7: as chaves do dict devem estar no formato ">texto<",
    não como tags completas. Isso garante compatibilidade com ambas as
    formas que o Word gera: <w:t>X</w:t> e <w:t xml:space="preserve">X</w:t>.

    Regra LD6: o chamador deve usar tokens intermediários quando as
    substituições formam cadeia (A->B, B->C, C->D). Ver docstring abaixo.

    Exemplo correto:
        substituicoes = {
            ">PLACEHOLDER_NOME<": ">João Silva<",
            ">PLACEHOLDER_DATA<": ">14 de maio de 2026<",
        }

    Exemplo de cadeia com tokens (LD6):
        substituicoes = {
            ">Fevereiro/2026<": ">__MESA__<",     # passo 1: proteger
            ">Marco/2026<":     ">__MESB__<",
            ">Abril/2026<":     ">Maio/2026<",    # passo 1: ultimo elo ok
            ">__MESB__<":       ">Abril/2026<",   # passo 2: resolver
            ">__MESA__<":       ">Marco/2026<",
        }
        # ATENÇÃO: dicts preservam ordem de inserção desde Python 3.7+.
        # A ordem das entradas no dict é a ordem de aplicação.
    """
    for old, new in substituicoes.items():
        doc = doc.replace(old, new)
    return doc


def montar_zip(all_files: dict, doc_xml: str) -> bytes:
    """
    Remonta o ZIP substituindo apenas word/document.xml.
    Todos os demais arquivos (VML, media, styles, numbering, etc.)
    são preservados byte a byte do template original.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for fname, data in all_files.items():
            if fname == "word/document.xml":
                zout.writestr(fname, doc_xml.encode("utf-8"))
            else:
                zout.writestr(fname, data)
    return buf.getvalue()


def gerar_docx(template_path: str, substituicoes: dict, dest_path: str) -> None:
    """
    Pipeline completo: lê template → aplica substituições → grava DOCX.

    Parâmetros
    ----------
    template_path : str
        Caminho para ASSETS/template_mod4.docx
    substituicoes : dict
        Mapa {">placeholder<": ">valor<"} conforme LD7.
        Para cadeias, incluir tokens intermediários conforme LD6.
    dest_path : str
        Caminho de destino do DOCX gerado.

    Após a geração, verificar o checklist do §7 do SKILL.md (12 pontos).
    """
    all_files = ler_template(template_path)
    doc = all_files["word/document.xml"].decode("utf-8")
    doc = substituir_xml(doc, substituicoes)
    docx_bytes = montar_zip(all_files, doc)

    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(docx_bytes)

    size_kb = os.path.getsize(dest_path) // 1024
    print(f"[mod4] DOCX gerado: {dest_path} ({size_kb} KB)")

    if size_kb < 100:
        print(f"[mod4] AVISO: tamanho {size_kb}KB abaixo de 100KB — verificar VML e imagens")


# ---------------------------------------------------------------------------
# Helpers de substituição — uso direto no pipeline mod4
# ---------------------------------------------------------------------------

def subs_simples(placeholder: str, valor: str) -> dict:
    """Atalho para substituição de campo único."""
    return {f">{placeholder}<": f">{valor}<"}


def subs_cadeia_meses(meses_origem: list, meses_destino: list) -> dict:
    """
    Gera mapa de substituição para rotação de meses com tokens (LD6 + LD7).

    meses_origem  = ["Fevereiro/2026", "Marco/2026", "Abril/2026"]
    meses_destino = ["Marco/2026",     "Abril/2026", "Maio/2026"]

    Retorna dict com a sequência correta: tokens na primeira metade,
    resolução na segunda.
    """
    assert len(meses_origem) == len(meses_destino), "listas devem ter o mesmo tamanho"
    tokens = [f"__MES{i}__" for i in range(len(meses_origem))]
    subs = {}
    # Passo 1: proteger origens — exceto o último elemento se não há conflito
    for i, (orig, dest) in enumerate(zip(meses_origem, meses_destino)):
        if dest not in meses_origem:
            # destino seguro — aplicar diretamente
            subs[f">{orig}<"] = f">{dest}<"
        else:
            # destino pode ser origem de outro — usar token
            subs[f">{orig}<"] = f">{tokens[i]}<"
    # Passo 2: resolver tokens
    for i, (orig, dest) in enumerate(zip(meses_origem, meses_destino)):
        if f">{tokens[i]}<" in subs.values():
            subs[f">{tokens[i]}<"] = f">{dest}<"
    return subs


# ---------------------------------------------------------------------------
# CLI — uso direto via linha de comando
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Gera DOCX mod4 via zipfile direto sobre template"
    )
    parser.add_argument(
        "--template", required=True,
        help="Caminho para template_mod4.docx"
    )
    parser.add_argument(
        "--subs", required=True,
        help=(
            "JSON com mapa de substituições no formato "
            '\{"\">placeholder<\": \">valor<\"}\'. '
            "Pode ser um arquivo .json ou uma string JSON inline."
        )
    )
    parser.add_argument(
        "--output", required=True,
        help="Caminho de destino do DOCX gerado"
    )
    args = parser.parse_args()

    # Carregar substituições
    if os.path.isfile(args.subs):
        with open(args.subs, encoding="utf-8") as f:
            substituicoes = json.load(f)
    else:
        substituicoes = json.loads(args.subs)

    gerar_docx(args.template, substituicoes, args.output)


if __name__ == "__main__":
    main()
