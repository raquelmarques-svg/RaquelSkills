#!/usr/bin/env python3
"""Auto-auditoria leve da governanca-skills.

Confere apenas presenca estrutural minima da propria skill. Auditoria
de integridade da biblioteca (coerencia com _manifest, ausencia de
orfaos, politica de arquivos) pertence a healthcheck-biblioteca, e nao
deve ser duplicada aqui.

Uso:
    python self_audit.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent

ARQUIVOS_MINIMOS = [
    "SKILL.md",
    "README.md",
    "SKILL_CREATION_SPEC.yaml",
]
PASTAS = ["assets", "templates", "schemas", "scripts", "references", "examples", "config"]
MODOS_OBRIGATORIOS = ["criacao", "auditoria", "classificacao", "divisao", "fusao", "auditar-self"]
TEMPLATES_OBRIGATORIOS = [
    "skill-creation-spec.yaml",
    "relatorio-auditoria-skill.md",
    "ficha-classificacao.md",
    "plano-divisao-skill.md",
    "plano-fusao-skills.md",
    "relatorio-self-audit.md",
]
SCHEMAS_OBRIGATORIOS = [
    "skill-creation-spec.schema.json",
    "skill-audit-leve.schema.json",
    "ficha-classificacao.schema.json",
]
SCRIPTS_OBRIGATORIOS = [
    "validar_skill_creation_spec.py",
    "detectar_verbo_multiplo.py",
    "auditar_skill_leve.py",
    "classificar_conteudo.py",
    "self_audit.py",
]


def main() -> int:
    resultado = {
        "skill_id": "governanca-skills",
        "audit_level": "leve",
        "scope": "self",
        "delegacao_externa": "healthcheck-biblioteca",
        "arquivos_minimos": {},
        "pastas_obrigatorias": {},
        "modos_em_skill_md": {},
        "templates_presentes": {},
        "schemas_presentes": {},
        "scripts_presentes": {},
        "alertas": [],
        "status": "SELF_AUDIT_OK",
    }

    for nome in ARQUIVOS_MINIMOS:
        existe = (SKILL_DIR / nome).is_file()
        resultado["arquivos_minimos"][nome] = existe
        if not existe:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Ausente: {nome}")

    for pasta in PASTAS:
        p = SKILL_DIR / pasta
        existe = p.is_dir()
        resultado["pastas_obrigatorias"][pasta] = existe
        if not existe:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Pasta ausente: {pasta}")

    skill_md = SKILL_DIR / "SKILL.md"
    texto = skill_md.read_text(encoding="utf-8") if skill_md.is_file() else ""
    for modo in MODOS_OBRIGATORIOS:
        # busca tolerante: presenca do nome do modo em qualquer secao.
        presente = modo.lower() in texto.lower()
        resultado["modos_em_skill_md"][modo] = presente
        if not presente:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Modo nao declarado em SKILL.md: {modo}")

    for nome in TEMPLATES_OBRIGATORIOS:
        existe = (SKILL_DIR / "templates" / nome).is_file()
        resultado["templates_presentes"][nome] = existe
        if not existe:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Template ausente: {nome}")

    for nome in SCHEMAS_OBRIGATORIOS:
        existe = (SKILL_DIR / "schemas" / nome).is_file()
        resultado["schemas_presentes"][nome] = existe
        if not existe:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Schema ausente: {nome}")

    for nome in SCRIPTS_OBRIGATORIOS:
        existe = (SKILL_DIR / "scripts" / nome).is_file()
        resultado["scripts_presentes"][nome] = existe
        if not existe:
            resultado["status"] = "SELF_AUDIT_COM_ALERTAS"
            resultado["alertas"].append(f"Script ausente: {nome}")

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
