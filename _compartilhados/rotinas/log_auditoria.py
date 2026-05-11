#!/usr/bin/env python3
"""
log_auditoria.py — Registra operacoes em _log-auditoria.md.

Uso:
    python3 log_auditoria.py registrar <operacao> <skill> [opcoes]
    python3 log_auditoria.py listar [--ultimas N]
    python3 log_auditoria.py buscar <termo>

Operacoes registraveis:
    criar | editar | auditar | refatorar | extrair | reverter | bloquear

Opcoes (registrar):
    --versao-antes X.Y.Z
    --versao-depois X.Y.Z
    --backup CAMINHO
    --alteracoes "resumo"
    --alertas "A1,A2"
    --sugestoes "Refactor,Extract"
    --decisao "aguardando-usuaria"

Conforme arquitetura V4:
    - Entrada append-only no log
    - Imutavel por 12 meses
    - Reversibilidade calculada (30 dias para Undo)
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

try:
    from resolver_output_root import resolver_compartilhados_root
except ImportError:
    import os
    def resolver_compartilhados_root():
        return Path(os.environ.get('RAQUEL_COMPARTILHADOS_ROOT', 'C:/RaquelSkills/_compartilhados'))


OPERACOES_VALIDAS = {'criar', 'editar', 'auditar', 'refatorar', 'extrair', 'reverter', 'bloquear', 'diagnosticar'}


def localizar_log() -> Path:
    """Resolve caminho do log de auditoria."""
    import os
    drive = os.environ.get('RAQUEL_DRIVE_ROOT')
    if drive:
        return Path(drive) / 'Claude' / 'governanca' / '_log-auditoria.md'
    # fallback: cwd
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


def garantir_log_inicializado(log_path: Path):
    """Garante que o arquivo de log existe com cabecalho."""
    if log_path.exists():
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = """# Log de auditoria - biblioteca Almeida Marques

Registro imutavel de toda operacao executada por skills de governanca.
Periodo de retencao: 12 meses minimo.

## Entradas

"""
    log_path.write_text(cabecalho, encoding='utf-8')


def registrar(operacao: str, skill: str, **opcoes) -> dict:
    """Registra uma entrada no log. Retorna entrada criada."""
    if operacao not in OPERACOES_VALIDAS:
        raise ValueError(f"operacao invalida: {operacao}. Validas: {OPERACOES_VALIDAS}")
    
    log_path = localizar_log()
    garantir_log_inicializado(log_path)
    
    agora = datetime.now()
    reversivel_ate = agora + timedelta(days=30)
    
    entrada = {
        'timestamp': agora.isoformat(timespec='seconds'),
        'operacao': operacao,
        'skill': skill,
        'reversivel_ate': reversivel_ate.strftime('%Y-%m-%d'),
    }
    
    if opcoes.get('versao_antes'):
        entrada['versao_antes'] = opcoes['versao_antes']
    if opcoes.get('versao_depois'):
        entrada['versao_depois'] = opcoes['versao_depois']
    if opcoes.get('backup'):
        entrada['backup'] = opcoes['backup']
    if opcoes.get('alteracoes'):
        entrada['alteracoes'] = opcoes['alteracoes']
    if opcoes.get('alertas'):
        if isinstance(opcoes['alertas'], str):
            entrada['alertas'] = [a.strip() for a in opcoes['alertas'].split(',') if a.strip()]
        else:
            entrada['alertas'] = opcoes['alertas']
    if opcoes.get('sugestoes'):
        if isinstance(opcoes['sugestoes'], str):
            entrada['sugestoes'] = [s.strip() for s in opcoes['sugestoes'].split(',') if s.strip()]
        else:
            entrada['sugestoes'] = opcoes['sugestoes']
    if opcoes.get('decisao'):
        entrada['decisao_pendente'] = opcoes['decisao']
    
    bloco_yaml = "- " + "\n  ".join(_yaml_format(k, v) for k, v in entrada.items()) + "\n\n"
    
    with log_path.open('a', encoding='utf-8') as f:
        f.write(bloco_yaml)
    
    return entrada


def _yaml_format(k, v):
    """Formata par chave/valor para YAML simples."""
    if isinstance(v, list):
        return f"{k}: [{', '.join(repr(item) for item in v)}]"
    if isinstance(v, str) and (',' in v or ':' in v):
        return f'{k}: "{v}"'
    return f"{k}: {v}"


def listar(n: int = 10):
    """Lista as ultimas N entradas."""
    log_path = localizar_log()
    if not log_path.exists():
        print(f"Log nao existe ainda: {log_path}")
        return
    texto = log_path.read_text(encoding='utf-8')
    # Achar entradas (cada uma comeca com "- timestamp:")
    import re
    entradas = re.findall(r'(- timestamp: .+?)(?=\n- timestamp:|\Z)', texto, re.DOTALL)
    print(f"Total de entradas: {len(entradas)}")
    print(f"Ultimas {min(n, len(entradas))}:\n")
    for e in entradas[-n:]:
        print(e.strip())
        print()


def buscar(termo: str):
    """Busca entradas que contenham o termo."""
    log_path = localizar_log()
    if not log_path.exists():
        print(f"Log nao existe ainda: {log_path}")
        return
    texto = log_path.read_text(encoding='utf-8')
    import re
    entradas = re.findall(r'(- timestamp: .+?)(?=\n- timestamp:|\Z)', texto, re.DOTALL)
    encontradas = [e for e in entradas if termo.lower() in e.lower()]
    print(f"Encontradas {len(encontradas)} entradas com '{termo}':\n")
    for e in encontradas:
        print(e.strip())
        print()


def main():
    parser = argparse.ArgumentParser(description='Log de auditoria - skills V4')
    sub = parser.add_subparsers(dest='cmd')
    
    p_reg = sub.add_parser('registrar')
    p_reg.add_argument('operacao')
    p_reg.add_argument('skill')
    p_reg.add_argument('--versao-antes')
    p_reg.add_argument('--versao-depois')
    p_reg.add_argument('--backup')
    p_reg.add_argument('--alteracoes')
    p_reg.add_argument('--alertas')
    p_reg.add_argument('--sugestoes')
    p_reg.add_argument('--decisao')
    
    p_list = sub.add_parser('listar')
    p_list.add_argument('--ultimas', type=int, default=10)
    
    p_busc = sub.add_parser('buscar')
    p_busc.add_argument('termo')
    
    args = parser.parse_args()
    
    if args.cmd == 'registrar':
        opcoes = {
            'versao_antes': args.versao_antes,
            'versao_depois': args.versao_depois,
            'backup': args.backup,
            'alteracoes': args.alteracoes,
            'alertas': args.alertas,
            'sugestoes': args.sugestoes,
            'decisao': args.decisao,
        }
        try:
            entrada = registrar(args.operacao, args.skill, **opcoes)
            print(f"+ Registrado: {entrada['operacao']} de {entrada['skill']} em {entrada['timestamp']}")
            print(f"  Reversivel ate: {entrada['reversivel_ate']}")
            sys.exit(0)
        except Exception as e:
            print(f"ERRO: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.cmd == 'listar':
        listar(args.ultimas)
    elif args.cmd == 'buscar':
        buscar(args.termo)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
