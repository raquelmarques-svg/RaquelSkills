#!/usr/bin/env python3
"""
undo_operacao.py — Reverte operacao do log de auditoria.

Uso:
    python3 undo_operacao.py listar [<skill>]
    python3 undo_operacao.py mostrar <timestamp>
    python3 undo_operacao.py reverter <timestamp> [--confirmar]

Comportamento:
    - Localiza entrada no log de auditoria por timestamp
    - Verifica reversibilidade (<= 30 dias)
    - Localiza arquivo de backup correspondente
    - Mostra diff entre versao atual e backup
    - Apos --confirmar, faz backup da versao atual e restaura

Conforme arquitetura V4:
    - Modo Undo do skill-creator-am
    - Janela 30 dias
    - Auto-protecao: backup da versao atual antes de reverter
"""

import sys
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))


def localizar_log() -> Path:
    """Resolve caminho do log de auditoria."""
    import os
    drive = os.environ.get('RAQUEL_DRIVE_ROOT')
    if drive:
        return Path(drive) / 'Claude' / 'governanca' / '_log-auditoria.md'
    raiz = Path(os.environ.get('RAQUEL_SKILLS_ROOT', Path.cwd()))
    candidatos = [
        raiz.parent / 'Drive' / 'Claude' / 'governanca' / '_log-auditoria.md',
        raiz / 'governanca' / '_log-auditoria.md',
        Path.cwd() / 'governanca' / '_log-auditoria.md',
    ]
    for c in candidatos:
        if c.exists():
            return c
    return candidatos[1]


def parse_entrada(bloco_texto: str) -> dict:
    """Parse de uma entrada do log."""
    entrada = {}
    for linha in bloco_texto.split('\n'):
        m = re.match(r'^\s*-?\s*([a-z_]+):\s*(.*)$', linha)
        if m:
            k, v = m.group(1), m.group(2).strip()
            # remover aspas externas
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            entrada[k] = v
    return entrada


def listar_entradas(skill_filtro: str = None) -> list:
    """Lista todas as entradas do log."""
    log_path = localizar_log()
    if not log_path.exists():
        return []
    texto = log_path.read_text(encoding='utf-8')
    blocos = re.findall(r'(- timestamp: .+?)(?=\n- timestamp:|\Z)', texto, re.DOTALL)
    entradas = [parse_entrada(b) for b in blocos]
    if skill_filtro:
        entradas = [e for e in entradas if e.get('skill') == skill_filtro]
    return entradas


def buscar_por_timestamp(timestamp: str) -> dict:
    """Busca entrada exata por timestamp (prefix-match)."""
    entradas = listar_entradas()
    for e in entradas:
        if e.get('timestamp', '').startswith(timestamp):
            return e
    return {}


def calcular_reversibilidade(entrada: dict) -> tuple:
    """Retorna (reversivel, dias_restantes)."""
    try:
        ts = datetime.fromisoformat(entrada['timestamp'])
        agora = datetime.now()
        dias = 30 - (agora - ts).days
        return (dias > 0, dias)
    except Exception:
        return (False, -1)


def backup_r3(arquivo: Path) -> Path:
    """Backup R3."""
    import os
    raiz = os.environ.get('RAQUEL_SKILLS_ROOT', '')
    backup_root = (Path(raiz) / '_backups' if raiz else arquivo.parent / '_backups') / arquivo.name
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = backup_root / f"{arquivo.stem}-{timestamp}-pre-undo{arquivo.suffix}"
    shutil.copy2(arquivo, dest)
    return dest


def mostrar_diff(atual: Path, backup: Path):
    """Mostra diff entre versao atual e backup."""
    import difflib
    a = atual.read_text(encoding='utf-8').splitlines(keepends=True)
    b = backup.read_text(encoding='utf-8').splitlines(keepends=True)
    diff = list(difflib.unified_diff(a, b, fromfile=str(atual), tofile=str(backup), n=3))
    if not diff:
        print("(arquivos identicos)")
        return
    for linha in diff[:200]:
        print(linha, end='')
    if len(diff) > 200:
        print(f"\n... ({len(diff) - 200} linhas adicionais omitidas)")


def comando_listar(args):
    entradas = listar_entradas(args.skill)
    if not entradas:
        print("Nenhuma entrada encontrada.")
        return
    print(f"Encontradas {len(entradas)} entradas:")
    print()
    for e in entradas[-20:]:  # ultimas 20
        rev, dias = calcular_reversibilidade(e)
        status = f"reversivel ({dias}d)" if rev else "expirado"
        print(f"  {e.get('timestamp', '?')}  {e.get('operacao', '?'):>10}  {e.get('skill', '?'):<30}  [{status}]")


def comando_mostrar(args):
    e = buscar_por_timestamp(args.timestamp)
    if not e:
        print(f"Entrada nao encontrada: {args.timestamp}", file=sys.stderr)
        sys.exit(1)
    print("Entrada encontrada:")
    for k, v in e.items():
        print(f"  {k}: {v}")
    rev, dias = calcular_reversibilidade(e)
    print(f"\nReversibilidade: {'sim' if rev else 'nao'} ({dias} dias restantes)")
    backup = e.get('backup', '')
    if backup and Path(backup).exists():
        print(f"Backup disponivel: {backup}")
    else:
        print(f"Backup: {backup or '(nao registrado)'} - {'ENCONTRADO' if backup and Path(backup).exists() else 'NAO ENCONTRADO'}")


def comando_reverter(args):
    e = buscar_por_timestamp(args.timestamp)
    if not e:
        print(f"Entrada nao encontrada: {args.timestamp}", file=sys.stderr)
        sys.exit(1)
    
    rev, dias = calcular_reversibilidade(e)
    if not rev:
        print(f"Operacao nao mais reversivel. Janela 30 dias expirada.", file=sys.stderr)
        sys.exit(1)
    
    backup_path = e.get('backup', '')
    if not backup_path or not Path(backup_path).exists():
        print(f"Backup nao encontrado: {backup_path}", file=sys.stderr)
        sys.exit(1)
    
    skill = e.get('skill', '')
    # Localizar arquivo alvo
    import os
    raiz = Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))
    arquivo_atual = raiz / 'skills' / skill / 'SKILL.md' if (raiz / 'skills').exists() else raiz / skill / 'SKILL.md'
    if not arquivo_atual.exists():
        print(f"Arquivo atual nao encontrado: {arquivo_atual}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Reverter operacao {e['operacao']} de {skill} em {e['timestamp']}")
    print(f"  Arquivo atual: {arquivo_atual}")
    print(f"  Backup origem: {backup_path}")
    print()
    print("=== DIFF (atual -> backup) ===")
    mostrar_diff(arquivo_atual, Path(backup_path))
    print("=== fim do diff ===")
    print()
    
    if not args.confirmar:
        print("Para aplicar a reversao, rode novamente com --confirmar")
        return
    
    # Auto-protecao: backup da versao atual ANTES de reverter
    auto_backup = backup_r3(arquivo_atual)
    print(f"+ Auto-protecao: versao atual em {auto_backup}")
    
    # Restaurar
    shutil.copy2(backup_path, arquivo_atual)
    print(f"+ Restaurado de: {backup_path}")
    print(f"  -> Aplicado em: {arquivo_atual}")
    
    # Sugerir registro no log
    print()
    print("Lembre de registrar no log:")
    print(f"  python3 log_auditoria.py registrar reverter {skill} \\")
    print(f"    --backup {auto_backup} \\")
    print(f"    --alteracoes 'undo de {e['timestamp']}'")


def main():
    parser = argparse.ArgumentParser(description='Undo - reverte operacao')
    sub = parser.add_subparsers(dest='cmd')
    
    p_list = sub.add_parser('listar')
    p_list.add_argument('skill', nargs='?', default=None)
    
    p_show = sub.add_parser('mostrar')
    p_show.add_argument('timestamp')
    
    p_rev = sub.add_parser('reverter')
    p_rev.add_argument('timestamp')
    p_rev.add_argument('--confirmar', action='store_true')
    
    args = parser.parse_args()
    
    if args.cmd == 'listar':
        comando_listar(args)
    elif args.cmd == 'mostrar':
        comando_mostrar(args)
    elif args.cmd == 'reverter':
        comando_reverter(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
