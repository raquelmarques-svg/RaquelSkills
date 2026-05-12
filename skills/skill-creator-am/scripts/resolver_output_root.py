#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resolver_output_root.py — Implementação L8 (skill ambiente-consciente).

Uso:
    from resolver_output_root import resolver
    output_root = resolver()

Comportamento:
    - Detecta o ambiente de execução:
      * Sandbox Claude.ai: /mnt/user-data/outputs/
      * Cowork local Windows: C:\\RaquelSkills\\outputs ou cwd
      * Variável de ambiente RAQUEL_OUTPUT_ROOT (override)
    - Retorna Path do diretório de saída apropriado

Conforme arquitetura V4:
    - Lição L8 (ambiente-consciente)
    - Usado por toda skill que escreve arquivos
"""

import os
import sys
from pathlib import Path


def detectar_ambiente() -> str:
    """Retorna o nome do ambiente: 'sandbox', 'cowork', 'unknown'."""
    if Path('/mnt/user-data/outputs').exists():
        return 'sandbox'
    if Path('C:\\RaquelSkills').exists() or Path('C:/RaquelSkills').exists():
        return 'cowork'
    return 'unknown'


def resolver() -> Path:
    """
    Resolve o diretório de output canônico para o ambiente atual.
    Cria o diretório se não existir.
    """
    # Override por variável de ambiente
    override = os.environ.get('RAQUEL_OUTPUT_ROOT')
    if override:
        path = Path(override)
        path.mkdir(parents=True, exist_ok=True)
        return path

    ambiente = detectar_ambiente()
    
    if ambiente == 'sandbox':
        path = Path('/mnt/user-data/outputs')
    elif ambiente == 'cowork':
        # Tenta C:\RaquelSkills\outputs primeiro
        cand1 = Path('C:/RaquelSkills/outputs')
        if Path('C:/RaquelSkills').exists():
            path = cand1
        else:
            path = Path.cwd() / 'outputs'
    else:
        # Fallback: cwd/outputs
        path = Path.cwd() / 'outputs'
    
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolver_skills_root() -> Path:
    """
    Resolve a raiz da biblioteca de skills.
    Útil para listar skills existentes (verificação de duplicidade).
    """
    override = os.environ.get('RAQUEL_SKILLS_ROOT')
    if override:
        return Path(override)
    
    ambiente = detectar_ambiente()
    if ambiente == 'sandbox':
        # Em sandbox, skills oficiais ficam aqui
        return Path('/mnt/skills/user')
    elif ambiente == 'cowork':
        return Path('C:/RaquelSkills/skills')
    else:
        return Path.cwd() / 'skills'


def resolver_compartilhados_root() -> Path:
    """Resolve raiz de _compartilhados/."""
    override = os.environ.get('RAQUEL_COMPARTILHADOS_ROOT')
    if override:
        return Path(override)
    
    ambiente = detectar_ambiente()
    if ambiente == 'sandbox':
        return Path('/mnt/user-data/outputs/_compartilhados')
    elif ambiente == 'cowork':
        return Path('C:/RaquelSkills/_compartilhados')
    else:
        return Path.cwd() / '_compartilhados'


def main():
    """Modo CLI: imprime caminhos resolvidos."""
    ambiente = detectar_ambiente()
    print(f"Ambiente detectado: {ambiente}")
    print(f"Output root: {resolver()}")
    print(f"Skills root: {resolver_skills_root()}")
    print(f"Compartilhados root: {resolver_compartilhados_root()}")


if __name__ == '__main__':
    main()
