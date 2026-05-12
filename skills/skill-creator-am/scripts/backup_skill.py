#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backup_skill.py — Implementação R3 (backup obrigatório antes de modificar).

Uso:
    python3 backup_skill.py <caminho-skill>
    python3 backup_skill.py <caminho-arquivo>

Comportamento:
    - Detecta se é diretório (skill completa) ou arquivo individual
    - Cria backup em _backups/[NOME]/[NOME]-YYYYMMDD-HHMMSS.[ext]
    - Retorna caminho do backup
    - Exit code 0 sucesso, 1 falha

Conforme arquitetura V4:
    - Cláusula universal R3
    - Localização: relativa à raiz RAQUEL_SKILLS_ROOT ou cwd
    - Preservação mínima 30 dias (janela do Undo)
"""

import sys
import os
import shutil
import datetime
from pathlib import Path


def detectar_raiz():
    """Detecta a raiz da biblioteca a partir de env var ou cwd."""
    raiz = os.environ.get('RAQUEL_SKILLS_ROOT')
    if raiz:
        return Path(raiz)
    cwd = Path.cwd()
    if (cwd / '_compartilhados').exists():
        return cwd
    return cwd


def backup(caminho_alvo: str) -> str:
    """
    Faz backup do alvo. Retorna caminho do backup.
    Lança exceção em caso de falha.
    """
    alvo = Path(caminho_alvo).resolve()
    if not alvo.exists():
        raise FileNotFoundError(f"Alvo não existe: {alvo}")

    raiz = detectar_raiz()
    backup_root = raiz / '_backups'
    backup_root.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    nome = alvo.name
    backup_dir = backup_root / nome
    backup_dir.mkdir(exist_ok=True)

    if alvo.is_dir():
        dest = backup_dir / f"{nome}-{timestamp}"
        shutil.copytree(alvo, dest)
    else:
        stem = alvo.stem
        ext = alvo.suffix
        dest = backup_dir / f"{stem}-{timestamp}{ext}"
        shutil.copy2(alvo, dest)

    if not dest.exists():
        raise RuntimeError(f"Backup falhou silenciosamente: {dest}")

    return str(dest)


def main():
    if len(sys.argv) < 2:
        print("Uso: backup_skill.py <caminho-skill-ou-arquivo>", file=sys.stderr)
        sys.exit(1)

    try:
        destino = backup(sys.argv[1])
        print(f"OK — backup em: {destino}")
        sys.exit(0)
    except Exception as e:
        print(f"ERRO — backup falhou: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
