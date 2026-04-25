#!/usr/bin/env python3
"""Detecta candidatos a verbo dominante em um SKILL.md.

Heuristica:
1. Carrega palavras-chave de config/palavras-chave-verbo-dominante.yaml.
2. Conta ocorrencias por familia verbal no SKILL.md.
3. Aponta familias com mais de um Procedimento operacional, mais de
   cinco modos, ou outputs primarios distintos.
4. Indica se a skill e candidata a divisao.

Auditoria substantiva nao e feita aqui. O script apenas levanta
sintomas estruturais.

Uso:
    python detectar_verbo_multiplo.py <caminho_skill_md>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "palavras-chave-verbo-dominante.yaml"
)


def carregar_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def carregar_skill(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def contar_familias(texto: str, mapa: dict) -> dict[str, int]:
    contagens: dict[str, int] = {}
    texto_lower = texto.lower()
    for familia, palavras in mapa.items():
        total = 0
        for p in palavras:
            total += len(re.findall(rf"\b{re.escape(p.lower())}\b", texto_lower))
        contagens[familia] = total
    return contagens


def contar_procedimentos(texto: str) -> int:
    return len(re.findall(r"^#+\s*Procedimento operacional", texto, flags=re.MULTILINE | re.IGNORECASE))


def contar_modos(texto: str) -> int:
    return len(re.findall(r"^##\s+Modo\b", texto, flags=re.MULTILINE | re.IGNORECASE))


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: detectar_verbo_multiplo.py <SKILL.md>", file=sys.stderr)
        return 2
    caminho = Path(sys.argv[1])
    if not caminho.is_file():
        print(f"Arquivo nao encontrado: {caminho}", file=sys.stderr)
        return 2

    config = carregar_config()
    mapa = config.get("verbos_dominantes", {})

    texto = carregar_skill(caminho)
    contagens = contar_familias(texto, mapa)
    n_proc = contar_procedimentos(texto)
    n_modos = contar_modos(texto)

    relevantes = {f: n for f, n in contagens.items() if n > 0}
    sintomas: list[str] = []

    if len(relevantes) > 1:
        top = sorted(relevantes.items(), key=lambda x: -x[1])[:3]
        sintomas.append(
            "Mais de uma familia verbal detectada: "
            + ", ".join(f"{f}({n})" for f, n in top)
        )
    if n_proc > 1:
        sintomas.append(f"{n_proc} secoes 'Procedimento operacional' detectadas.")
    if n_modos > 5:
        sintomas.append(f"{n_modos} modos internos detectados (limite recomendado: 5).")

    print(f"Skill auditada: {caminho.name}")
    print(f"Familias verbais detectadas: {relevantes}")
    print(f"Procedimentos: {n_proc}; Modos: {n_modos}")
    if sintomas:
        print("\nSintomas estruturais:")
        for s in sintomas:
            print(f"  - {s}")
        print("\nStatus: DIVISAO_RECOMENDADA")
        print("Proxima skill: governanca-skills modo `divisao`.")
        return 0
    print("\nNenhum sintoma estrutural de inchaco detectado.")
    print("Status: AUDITORIA_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
