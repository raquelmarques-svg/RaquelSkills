#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_duplicacao.py — Detecta duplicação entre skills.

Uso:
    python3 verificar_duplicacao.py <skill-nova>
    python3 verificar_duplicacao.py --todas

Comportamento:
    - Compara SKILL.md da skill nova (ou todas) com biblioteca existente
    - Identifica blocos de 10+ linhas duplicados
    - Reporta pares (skill A, skill B, trecho)
    - Sugere migração para _compartilhados/

Conforme arquitetura V4:
    - Auditoria 10 do pós-criação
    - Modo Extract do skill-creator-am
    - Threshold: 10 linhas (alerta), 20 linhas (bloqueio)
"""

import sys
import re
from pathlib import Path
from difflib import SequenceMatcher

try:
    from resolver_output_root import resolver_skills_root
except ImportError:
    # Fallback se rodar isolado
    def resolver_skills_root():
        import os
        return Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))


THRESHOLD_ALERTA = 10
THRESHOLD_BLOQUEIO = 20
SIMILARIDADE_MIN = 0.85


def ler_skill_md(caminho_skill: Path) -> str:
    """Lê SKILL.md de uma skill."""
    skill_md = caminho_skill / 'SKILL.md'
    if not skill_md.exists():
        return ''
    return skill_md.read_text(encoding='utf-8', errors='ignore')


def extrair_blocos(texto: str, min_linhas: int = THRESHOLD_ALERTA) -> list:
    """Extrai blocos de N+ linhas contíguas (não-vazias)."""
    linhas = texto.split('\n')
    blocos = []
    bloco_atual = []
    
    for linha in linhas:
        if linha.strip():
            bloco_atual.append(linha)
        else:
            if len(bloco_atual) >= min_linhas:
                blocos.append('\n'.join(bloco_atual))
            bloco_atual = []
    
    if len(bloco_atual) >= min_linhas:
        blocos.append('\n'.join(bloco_atual))
    
    return blocos


def comparar_blocos(blocos_a: list, blocos_b: list) -> list:
    """Compara blocos par a par; retorna duplicações."""
    duplicacoes = []
    for ba in blocos_a:
        for bb in blocos_b:
            sim = SequenceMatcher(None, ba, bb).ratio()
            if sim >= SIMILARIDADE_MIN:
                linhas_ba = len(ba.split('\n'))
                duplicacoes.append({
                    'linhas': linhas_ba,
                    'similaridade': sim,
                    'trecho_a': ba[:200] + '...' if len(ba) > 200 else ba,
                    'severidade': 'bloqueio' if linhas_ba >= THRESHOLD_BLOQUEIO else 'alerta',
                })
    return duplicacoes


def verificar_skill_unica(skill_alvo: Path, biblioteca: Path) -> dict:
    """Verifica uma skill contra toda a biblioteca."""
    texto_alvo = ler_skill_md(skill_alvo)
    blocos_alvo = extrair_blocos(texto_alvo)
    
    resultado = {
        'skill': skill_alvo.name,
        'duplicacoes': {},
        'total_bloqueio': 0,
        'total_alerta': 0,
    }
    
    for skill_dir in biblioteca.iterdir():
        if not skill_dir.is_dir() or skill_dir.name == skill_alvo.name:
            continue
        texto_outra = ler_skill_md(skill_dir)
        if not texto_outra:
            continue
        blocos_outra = extrair_blocos(texto_outra)
        dups = comparar_blocos(blocos_alvo, blocos_outra)
        if dups:
            resultado['duplicacoes'][skill_dir.name] = dups
            for d in dups:
                if d['severidade'] == 'bloqueio':
                    resultado['total_bloqueio'] += 1
                else:
                    resultado['total_alerta'] += 1
    
    return resultado


def verificar_todas(biblioteca: Path) -> dict:
    """Verifica todos os pares na biblioteca."""
    resultados = {}
    skills = [s for s in biblioteca.iterdir() if s.is_dir()]
    for skill in skills:
        resultados[skill.name] = verificar_skill_unica(skill, biblioteca)
    return resultados


def imprimir_relatorio(resultado: dict):
    """Imprime relatório legível."""
    print(f"\nDuplicação para: {resultado['skill']}")
    print("=" * 60)
    
    if not resultado['duplicacoes']:
        print("  ✓ Nenhuma duplicação detectada (≥ 10 linhas).")
        return
    
    for outra_skill, dups in resultado['duplicacoes'].items():
        print(f"\n  vs {outra_skill}:")
        for d in dups:
            cor = '🔴' if d['severidade'] == 'bloqueio' else '🟡'
            print(f"    {cor} {d['linhas']} linhas, similaridade {d['similaridade']:.2%}")
            print(f"       Trecho: {d['trecho_a'][:100]}...")
    
    print(f"\n  Total: {resultado['total_bloqueio']} bloqueio, {resultado['total_alerta']} alerta")
    
    if resultado['total_bloqueio'] > 0:
        print("\n  ⚠️ AÇÃO: usar Modo Extract para migrar para _compartilhados/")


def main():
    if len(sys.argv) < 2:
        print("Uso: verificar_duplicacao.py <skill-nova-path> | --todas", file=sys.stderr)
        sys.exit(1)
    
    biblioteca = resolver_skills_root()
    if not biblioteca.exists():
        print(f"ERRO — biblioteca não encontrada: {biblioteca}", file=sys.stderr)
        sys.exit(1)
    
    if sys.argv[1] == '--todas':
        resultados = verificar_todas(biblioteca)
        for nome, res in resultados.items():
            imprimir_relatorio(res)
    else:
        skill = Path(sys.argv[1])
        if not skill.is_absolute():
            skill = biblioteca / skill.name
        resultado = verificar_skill_unica(skill, biblioteca)
        imprimir_relatorio(resultado)


if __name__ == '__main__':
    main()
