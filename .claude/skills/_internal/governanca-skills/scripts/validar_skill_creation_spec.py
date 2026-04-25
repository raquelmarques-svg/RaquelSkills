#!/usr/bin/env python3
"""Valida uma SkillCreationSpec contra o schema da skill governanca-skills.

Uso:
    python validar_skill_creation_spec.py <caminho_para_spec.yaml>

Retorna codigo 0 se valido, 1 se invalido. Imprime violacoes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "skill-creation-spec.schema.json"


def carregar_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def carregar_spec(caminho: Path) -> dict:
    with caminho.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validar(spec: dict, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema)
    erros = sorted(validator.iter_errors(spec), key=lambda e: list(e.path))
    return [
        f"{'.'.join(str(p) for p in e.path) or '<raiz>'}: {e.message}"
        for e in erros
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: validar_skill_creation_spec.py <spec.yaml>", file=sys.stderr)
        return 2
    caminho = Path(sys.argv[1])
    if not caminho.is_file():
        print(f"Arquivo nao encontrado: {caminho}", file=sys.stderr)
        return 2
    schema = carregar_schema()
    spec = carregar_spec(caminho)
    erros = validar(spec, schema)
    if not erros:
        print("OK: SkillCreationSpec valida.")
        return 0
    print(f"ERRO: {len(erros)} violacao(oes):")
    for msg in erros:
        print(f"  - {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
