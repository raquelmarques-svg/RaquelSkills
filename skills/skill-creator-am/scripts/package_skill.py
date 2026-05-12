#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_skill.py — Empacota skill em arquivo .skill (zip).

Uso:
    python3 package_skill.py <skill-path> [output-dir]

Comportamento:
    - Cria zip da skill com estrutura canônica
    - Nome: [nome-skill].skill
    - Destino: output-dir (default: resolver_output_root)
    - Exclui __pycache__, .pyc, .DS_Store, Thumbs.db
"""

import sys
import zipfile
from pathlib import Path

try:
    from resolver_output_root import resolver
except ImportError:
    def resolver():
        return Path.cwd()


EXCLUIR = {'__pycache__', '.pyc', '.DS_Store', 'Thumbs.db', '.git'}


def deve_excluir(path: Path) -> bool:
    for parte in path.parts:
        if parte in EXCLUIR:
            return True
        if any(parte.endswith(suf) for suf in ('.pyc', '.swp', '.tmp')):
            return True
    return False


def empacotar(skill_dir: Path, output_dir: Path) -> Path:
    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill não encontrada: {skill_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_name = skill_dir.name
    zip_path = output_dir / f"{skill_name}.skill"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in skill_dir.rglob('*'):
            if item.is_file() and not deve_excluir(item):
                arcname = item.relative_to(skill_dir.parent)
                zf.write(item, arcname)
    
    return zip_path


def main():
    if len(sys.argv) < 2:
        print("Uso: package_skill.py <skill-path> [output-dir]", file=sys.stderr)
        sys.exit(1)
    
    skill = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else resolver()
    
    try:
        zip_path = empacotar(skill, output)
        size_kb = zip_path.stat().st_size / 1024
        print(f"OK — empacotado em: {zip_path}")
        print(f"     Tamanho: {size_kb:.1f} KB")
        sys.exit(0)
    except Exception as e:
        print(f"ERRO — empacotamento falhou: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
