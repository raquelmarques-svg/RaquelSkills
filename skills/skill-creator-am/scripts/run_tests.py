#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_tests.py — Executa casos de teste de uma skill contra scripts Python.

Uso:
    python3 run_tests.py <skill-path>
    python3 run_tests.py <skill-path> --caso caso-01
    python3 run_tests.py <skill-path> --json

Estrutura esperada em tests/:
    tests/
    ├── run_tests.py          ← este arquivo (copiado para cada skill)
    └── caso-NN/
        ├── input.json        ← input real do caso
        └── expected_output.md ← fragmento esperado no output

Comportamento:
    1. Detecta script principal da skill (primeiro .py em scripts/)
    2. Para cada caso em tests/caso-*/
       a. Executa o script com input.json
       b. Compara output com expected_output.md
       c. Reporta pass/fail
    3. Retorna exit code 0 se todos passam, 1 se algum falha.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def encontrar_script_principal(skill_path: Path) -> Path | None:
    """Encontra o script Python principal da skill."""
    scripts_dir = skill_path / 'scripts'
    if not scripts_dir.exists():
        return None
    # Priorizar scripts com 'gerar' ou 'principal' no nome
    for nome in ['gerar_mod4.py', 'organizar.py', 'calcular.py']:
        p = scripts_dir / nome
        if p.exists():
            return p
    # Fallback: primeiro .py que não seja utilitário
    utilitarios = {'backup_skill.py', 'run_tests.py', 'resolver_output_root.py',
                   'auditar_frontmatter.py', 'auditar_tamanho.py', 'package_skill.py',
                   'inserir_clausulas.py', 'verificar_duplicacao.py'}
    for p in sorted(scripts_dir.glob('*.py')):
        if p.name not in utilitarios:
            return p
    return None


def executar_caso(script: Path, caso_dir: Path, config: Path | None = None) -> dict:
    """Executa um caso de teste e retorna resultado."""
    input_json = caso_dir / 'input.json'
    expected = caso_dir / 'expected_output.md'

    if not input_json.exists():
        return {'status': 'SKIP', 'motivo': 'input.json ausente'}

    cmd = [sys.executable, str(script), '--input', str(input_json), '--output', '/tmp/test_output.docx']
    if config and config.exists():
        cmd += ['--config', str(config)]

    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60, encoding='utf-8')
        saida = resultado.stdout + resultado.stderr

        if resultado.returncode != 0:
            return {
                'status': 'FAIL',
                'motivo': f'Exit code {resultado.returncode}',
                'saida': saida[:500]
            }

        # Verificar fragmento esperado se existir
        if expected.exists():
            fragmento = expected.read_text(encoding='utf-8').strip()
            # Verificação simples: fragmentos-chave devem aparecer na saída
            linhas_chave = [l.strip() for l in fragmento.split('\n') if l.strip() and not l.startswith('#')]
            falhas = [l for l in linhas_chave[:5] if l and l not in saida]
            if falhas:
                return {
                    'status': 'FAIL',
                    'motivo': f'Output não contém: {falhas[0][:80]}',
                    'saida': saida[:300]
                }

        return {'status': 'PASS', 'saida': saida[:200]}

    except subprocess.TimeoutExpired:
        return {'status': 'FAIL', 'motivo': 'Timeout (60s)'}
    except Exception as e:
        return {'status': 'ERROR', 'motivo': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Executa testes de uma skill AM')
    parser.add_argument('skill_path', help='Caminho para o diretório da skill')
    parser.add_argument('--caso', help='Executar apenas este caso (ex: caso-01)')
    parser.add_argument('--json', action='store_true', help='Output em JSON')
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    tests_dir = skill_path / 'tests'

    if not tests_dir.exists():
        print(f'tests/ não encontrado em {skill_path}')
        sys.exit(0)  # Não é erro — skill pode não ter testes ainda

    script = encontrar_script_principal(skill_path)
    if not script:
        print('Nenhum script principal encontrado em scripts/')
        sys.exit(1)

    config = skill_path / 'CONFIG' / 'tipografia.json'

    # Listar casos
    casos = sorted(tests_dir.glob('caso-*/'))
    if args.caso:
        casos = [c for c in casos if c.name == args.caso]

    if not casos:
        print('Nenhum caso encontrado em tests/')
        sys.exit(0)

    resultados = {}
    passou = 0
    falhou = 0

    for caso_dir in casos:
        nome = caso_dir.name
        r = executar_caso(script, caso_dir, config)
        resultados[nome] = r
        if r['status'] == 'PASS':
            passou += 1
        elif r['status'] in ('FAIL', 'ERROR'):
            falhou += 1

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    if args.json:
        print(json.dumps({
            'timestamp': timestamp,
            'skill': str(skill_path.name),
            'script': str(script.name),
            'total': len(casos),
            'passou': passou,
            'falhou': falhou,
            'resultados': resultados
        }, ensure_ascii=False, indent=2))
    else:
        print(f'\n=== Testes: {skill_path.name} ({timestamp}) ===')
        print(f'Script: {script.name}')
        print(f'Casos: {len(casos)} | Passou: {passou} | Falhou: {falhou}\n')
        for nome, r in resultados.items():
            icone = '✓' if r['status'] == 'PASS' else '✗' if r['status'] == 'FAIL' else '⚠'
            motivo = f" — {r.get('motivo', '')}" if r['status'] != 'PASS' else ''
            print(f'  {icone}  {nome}{motivo}')
        print()

    sys.exit(0 if falhou == 0 else 1)


if __name__ == '__main__':
    main()
