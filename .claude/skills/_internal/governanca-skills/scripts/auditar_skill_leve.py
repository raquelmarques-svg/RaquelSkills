#!/usr/bin/env python3
"""Auditoria leve de skill. Confere apenas presenca de campos minimos.

Auditoria substantiva pertence a healthcheck-biblioteca.

Uso:
    python auditar_skill_leve.py <caminho_pasta_skill>

A pasta deve conter SKILL.md e as sete subpastas obrigatorias (assets,
templates, schemas, scripts, references, examples, config).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "criterios-auditoria-leve.yaml"
)

PASTAS = ["assets", "templates", "schemas", "scripts", "references", "examples", "config"]
SECOES_OBRIGATORIAS = [
    ("Finalidade", r"^#\s+Finalidade"),
    ("Transformacao", r"^#\s+Transforma[cç][aã]o"),
    ("Gatilhos", r"^#\s+Gatilhos"),
    ("Bloqueios", r"^#\s+Bloqueios"),
    ("Entrada minima", r"^#\s+Entrada\s+m[ií]nima"),
    ("Procedimento operacional obrigatorio", r"Procedimento operacional"),
    ("Outputs", r"^#\s+Outputs"),
    ("Limites", r"^#\s+Limites"),
]
FRONTMATTER_CAMPOS = ["name", "description", "version", "layer", "activation"]


def carregar_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extrair_frontmatter(texto: str) -> dict:
    if not texto.startswith("---"):
        return {}
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}
    bloco = texto[3:fim].strip()
    try:
        return yaml.safe_load(bloco) or {}
    except yaml.YAMLError:
        return {}


def auditar(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    resultado = {
        "skill_id": skill_dir.resolve().name,
        "audit_level": "leve",
        "campos_obrigatorios": {},
        "pastas_obrigatorias": {},
        "skill_md_linhas": 0,
        "alertas": [],
        "status": "AUDITORIA_OK",
    }

    if not skill_md.is_file():
        resultado["status"] = "AUDITORIA_REPROVADA"
        resultado["alertas"].append("SKILL.md ausente.")
        return resultado

    texto = skill_md.read_text(encoding="utf-8")
    resultado["skill_md_linhas"] = texto.count("\n") + 1

    fm = extrair_frontmatter(texto)
    for campo in FRONTMATTER_CAMPOS:
        presente = campo in fm and fm[campo] not in (None, "")
        resultado["campos_obrigatorios"][f"frontmatter_{campo}"] = {"presente": presente}
        if not presente:
            resultado["status"] = "AUDITORIA_REPROVADA"

    for nome, regex in SECOES_OBRIGATORIAS:
        presente = bool(re.search(regex, texto, flags=re.MULTILINE | re.IGNORECASE))
        chave = nome.lower().replace(" ", "_")
        resultado["campos_obrigatorios"][chave] = {"presente": presente}
        if not presente:
            resultado["status"] = "AUDITORIA_REPROVADA"

    for pasta in PASTAS:
        p = skill_dir / pasta
        existe = p.is_dir()
        vazia = existe and not any(p.iterdir())
        resultado["pastas_obrigatorias"][pasta] = {"presente": existe, "vazia": vazia}
        if not existe:
            resultado["status"] = "AUDITORIA_REPROVADA"
            resultado["alertas"].append(f"Pasta ausente: {pasta}")

    if resultado["skill_md_linhas"] > 500:
        resultado["alertas"].append(
            f"SKILL.md tem {resultado['skill_md_linhas']} linhas (limite 500)."
        )
        if resultado["status"] == "AUDITORIA_OK":
            resultado["status"] = "AUDITORIA_COM_ALERTAS"
    if resultado["skill_md_linhas"] < 30:
        resultado["alertas"].append(
            f"SKILL.md tem {resultado['skill_md_linhas']} linhas (minimo 30)."
        )
        if resultado["status"] == "AUDITORIA_OK":
            resultado["status"] = "AUDITORIA_COM_ALERTAS"

    if resultado["status"] == "AUDITORIA_OK" and any(
        p["vazia"] for p in resultado["pastas_obrigatorias"].values()
    ):
        resultado["status"] = "AUDITORIA_COM_ALERTAS"
        for nome, info in resultado["pastas_obrigatorias"].items():
            if info["vazia"]:
                resultado["alertas"].append(f"Pasta vazia: {nome}.")

    resultado["proxima_skill_recomendada"] = "healthcheck-biblioteca"
    return resultado


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: auditar_skill_leve.py <pasta_skill>", file=sys.stderr)
        return 2
    skill_dir = Path(sys.argv[1])
    if not skill_dir.is_dir():
        print(f"Pasta nao encontrada: {skill_dir}", file=sys.stderr)
        return 2
    resultado = auditar(skill_dir)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado["status"] != "AUDITORIA_REPROVADA" else 1


if __name__ == "__main__":
    sys.exit(main())
