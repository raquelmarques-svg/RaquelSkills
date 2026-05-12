#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar_tamanho.py — Auditoria 1 (tamanho dos arquivos).

Uso:
    python3 auditar_tamanho.py <skill-path>
    python3 auditar_tamanho.py --todas

Comportamento:
    - Conta linhas de SKILL.md, references, scripts
    - Compara com limites canônicos da arquitetura V4
    - Retorna semáforo (verde/amarelo/laranja/vermelho)

Limites V4:
    SKILL.md core:    ideal ≤ 300, máximo ≤ 500
    Reference:        ideal ≤ 200, máximo ≤ 400
    Script:           ideal ≤ 200, máximo ≤ 500
"""

import sys
from pathlib import Path

try:
    from resolver_output_root import resolver_skills_root
except ImportError:
    def resolver_skills_root():
        import os
        return Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))


LIMITES = {
    'SKILL.md':   {'ideal': 300, 'max': 500},
    'reference':  {'ideal': 200, 'max': 400},
    'script':     {'ideal': 200, 'max': 500},
}


def cor_status(linhas: int, limite: dict) -> str:
    """Retorna cor de status conforme limite."""
    if linhas <= limite['ideal']:
        return 'verde'
    elif linhas <= limite['ideal'] * 1.5:
        return 'amarelo'
    elif linhas <= limite['max']:
        return 'laranja'
    else:
        return 'vermelho'


def contar_linhas(arquivo: Path) -> int:
    """Conta linhas (não vazias)."""
    if not arquivo.exists():
        return 0
    try:
        texto = arquivo.read_text(encoding='utf-8', errors='ignore')
        return len(texto.split('\n'))
    except Exception:
        return 0


def auditar_skill(skill_dir: Path) -> dict:
    """Audita tamanho de todos os componentes de uma skill."""
    resultado = {
        'skill': skill_dir.name,
        'SKILL.md': None,
        'references': {},
        'scripts': {},
        'examples': {},
        'total_linhas': 0,
        'status_geral': 'verde',
    }
    
    # SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    if skill_md.exists():
        linhas = contar_linhas(skill_md)
        status = cor_status(linhas, LIMITES['SKILL.md'])
        resultado['SKILL.md'] = {'linhas': linhas, 'status': status}
        resultado['total_linhas'] += linhas
    
    # References
    ref_dir = skill_dir / 'references'
    if ref_dir.exists():
        for ref in ref_dir.iterdir():
            if ref.suffix == '.md':
                linhas = contar_linhas(ref)
                status = cor_status(linhas, LIMITES['reference'])
                resultado['references'][ref.name] = {'linhas': linhas, 'status': status}
                resultado['total_linhas'] += linhas
    
    # Scripts
    scr_dir = skill_dir / 'scripts'
    if scr_dir.exists():
        for scr in scr_dir.iterdir():
            if scr.suffix == '.py':
                linhas = contar_linhas(scr)
                status = cor_status(linhas, LIMITES['script'])
                resultado['scripts'][scr.name] = {'linhas': linhas, 'status': status}
                resultado['total_linhas'] += linhas
    
    # Examples (info, sem auditoria de tamanho)
    ex_dir = skill_dir / 'examples'
    if ex_dir.exists():
        for ex in ex_dir.iterdir():
            if ex.suffix == '.md':
                resultado['examples'][ex.name] = {'linhas': contar_linhas(ex)}
    
    # Status geral
    statuses = []
    if resultado['SKILL.md']:
        statuses.append(resultado['SKILL.md']['status'])
    for d in resultado['references'].values():
        statuses.append(d['status'])
    for d in resultado['scripts'].values():
        statuses.append(d['status'])
    
    if 'vermelho' in statuses:
        resultado['status_geral'] = 'vermelho'
    elif 'laranja' in statuses:
        resultado['status_geral'] = 'laranja'
    elif 'amarelo' in statuses:
        resultado['status_geral'] = 'amarelo'
    
    return resultado


def imprimir_relatorio(resultado: dict):
    cor_map = {'verde': '✅', 'amarelo': '🟡', 'laranja': '🟠', 'vermelho': '🔴'}
    print(f"\nAuditoria de tamanho: {resultado['skill']}")
    print("=" * 60)
    
    if resultado['SKILL.md']:
        m = resultado['SKILL.md']
        print(f"  {cor_map[m['status']]} SKILL.md: {m['linhas']} linhas ({m['status']})")
    
    if resultado['references']:
        print("\n  References:")
        for nome, d in sorted(resultado['references'].items()):
            print(f"    {cor_map[d['status']]} {nome}: {d['linhas']} linhas")
    
    if resultado['scripts']:
        print("\n  Scripts:")
        for nome, d in sorted(resultado['scripts'].items()):
            print(f"    {cor_map[d['status']]} {nome}: {d['linhas']} linhas")
    
    if resultado['examples']:
        print(f"\n  Examples: {len(resultado['examples'])} arquivos")
    
    print(f"\n  Total: {resultado['total_linhas']} linhas")
    print(f"  Status geral: {cor_map[resultado['status_geral']]} {resultado['status_geral']}")


def main():
    if len(sys.argv) < 2:
        print("Uso: auditar_tamanho.py <skill-path> | --todas", file=sys.stderr)
        sys.exit(1)
    
    biblioteca = resolver_skills_root()
    
    if sys.argv[1] == '--todas':
        for skill in biblioteca.iterdir():
            if skill.is_dir() and (skill / 'SKILL.md').exists():
                resultado = auditar_skill(skill)
                imprimir_relatorio(resultado)
    else:
        skill = Path(sys.argv[1])
        if not skill.is_absolute():
            skill = biblioteca / skill.name
        if not skill.exists():
            print(f"ERRO — skill não encontrada: {skill}", file=sys.stderr)
            sys.exit(1)
        resultado = auditar_skill(skill)
        imprimir_relatorio(resultado)


if __name__ == '__main__':
    main()
