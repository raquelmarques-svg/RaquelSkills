#!/usr/bin/env python3
"""Classifica um conteudo recebido entre skill autonoma, modo interno e
sete tipos de recurso (asset, template, schema, script, reference,
example, config), aplicando a regra hierarquica fixada no projeto.

Heuristica simplificada. Decisao final pertence a usuaria, especialmente
em casos cinza. Em duvida, devolve com matriz de criterios.

Uso:
    python classificar_conteudo.py <arquivo_descricao.txt>

O arquivo deve conter, em texto livre, descricao do conteudo a
classificar. O script imprime a ficha-classificacao em JSON.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "palavras-chave-verbo-dominante.yaml"
)

# Skills nucleares e suas familias verbais predominantes (conforme manual).
# Esta tabela e auxiliar; classificacao final exige aplicacao do asset
# regra-hierarquica-casos-cinza.md por humano ou por governanca-skills.
SKILLS_PAI = {
    "redigir": "peticao-processual",
    "revisar": "revisao-juridica",
    "validar": "revisao-preprotocolo",
    "formatar": "mod4",
    "protocolar": "peticionamento-eletronico",
    "extrair": "levanta-fatos",
    "calcular": "honorarios",
    "sintetizar": "dossie-caso",
    "monitorar": "monitor-publicacoes",
    "comunicar": "comunicacao-cliente",
    "organizar": "organizar-pasta-cliente",
    "governar": "governanca-skills",
    "classificar": "governanca-skills",
}

PALAVRAS_TIPO_RECURSO = {
    "asset": ["criterio", "criterios", "padrao", "diretriz", "como decidir", "como distinguir"],
    "template": ["modelo", "molde", "forma de saida", "preencher", "esqueleto"],
    "schema": ["campos obrigatorios", "validar campos", "tipo de dado", "enumeracao"],
    "script": ["calcular", "validar arquivo", "extrair texto", "normalizar", "gerar arquivo", "converter"],
    "reference": ["documentacao longa", "metodologia", "tratado", "manual completo"],
    "example": ["exemplo bom", "exemplo ruim", "calibrar", "comparacao para ajustar"],
    "config": ["parametro", "caminho", "limite", "permissao", "constante"],
}


def carregar_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detectar_familia_verbal(texto: str, mapa: dict) -> tuple[str, int]:
    melhor = ("nenhuma", 0)
    t = texto.lower()
    for familia, palavras in mapa.items():
        score = 0
        for p in palavras:
            score += len(re.findall(rf"\b{re.escape(p.lower())}\b", t))
        if score > melhor[1]:
            melhor = (familia, score)
    return melhor


def detectar_tipo_recurso(texto: str) -> str | None:
    t = texto.lower()
    for tipo, marcadores in PALAVRAS_TIPO_RECURSO.items():
        for m in marcadores:
            if m in t:
                return tipo
    return None


def classificar(descricao: str) -> dict:
    config = carregar_config()
    mapa = config.get("verbos_dominantes", {})

    familia, score = detectar_familia_verbal(descricao, mapa)
    skill_pai = SKILLS_PAI.get(familia)
    tipo_recurso = detectar_tipo_recurso(descricao)

    ficha = {
        "conteudo_avaliado": descricao[:200],
        "verbo_dominante_detectado": familia if score > 0 else "indefinido",
        "skill_pai_existente": {
            "existe": skill_pai is not None,
            "skill_id": skill_pai or "",
            "compatibilidade_verbal": "alta" if score >= 2 else ("media" if score == 1 else "nenhuma"),
        },
        "regra_aplicada": "regra_hierarquica_skill_pai",
        "destino_recomendado": "",
        "justificativa": "",
        "caminho_destino_sugerido": "",
        "status": "",
        "proxima_skill": "",
    }

    if tipo_recurso:
        ficha["destino_recomendado"] = tipo_recurso
        if skill_pai:
            ficha["caminho_destino_sugerido"] = f"{skill_pai}/{tipo_recurso}s/"
            ficha["status"] = "VIRAR_RECURSO_LOCAL"
        else:
            ficha["caminho_destino_sugerido"] = f"_shared/{tipo_recurso}s/"
            ficha["status"] = "VIRAR_RECURSO_SHARED"
        ficha["justificativa"] = (
            f"Marcadores de tipo '{tipo_recurso}' detectados no texto."
        )
        ficha["proxima_skill"] = "resource-registry"
        return ficha

    if skill_pai and score >= 2:
        ficha["destino_recomendado"] = "modo_interno"
        ficha["caminho_destino_sugerido"] = (
            f"{skill_pai}/SKILL.md (adicionar modo interno)"
        )
        ficha["justificativa"] = (
            f"Skill-pai '{skill_pai}' existe com verbo compativel. Regra "
            "hierarquica determina virar modo interno."
        )
        ficha["status"] = "VIRAR_MODO_INTERNO"
        ficha["proxima_skill"] = "governanca-skills modo `criacao` para spec do modo"
        return ficha

    if score > 0 and not skill_pai:
        ficha["destino_recomendado"] = "skill_autonoma"
        ficha["caminho_destino_sugerido"] = "_internal/ ou skills/"
        ficha["justificativa"] = (
            "Verbo dominante detectado sem skill-pai compativel."
        )
        ficha["status"] = "VIRAR_SKILL_AUTONOMA"
        ficha["proxima_skill"] = "governanca-skills modo `criacao`"
        return ficha

    ficha["destino_recomendado"] = ""
    ficha["justificativa"] = (
        "Verbo dominante e tipo de recurso indeterminados. Devolucao a "
        "usuaria para decisao consciente, conforme postura para casos cinza."
    )
    ficha["status"] = "REJEITADA_DUPLICIDADE"
    ficha["proxima_skill"] = "usuaria"
    return ficha


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: classificar_conteudo.py <arquivo.txt>", file=sys.stderr)
        return 2
    caminho = Path(sys.argv[1])
    if not caminho.is_file():
        print(f"Arquivo nao encontrado: {caminho}", file=sys.stderr)
        return 2
    descricao = caminho.read_text(encoding="utf-8")
    ficha = classificar(descricao)
    print(json.dumps(ficha, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
