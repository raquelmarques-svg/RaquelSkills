#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar_frontmatter.py — Auditoria 2 (frontmatter completo V4).

Uso:
    python3 auditar_frontmatter.py <skill-path>
    python3 auditar_frontmatter.py --todas

Comportamento:
    - Parseia frontmatter YAML do SKILL.md
    - Verifica campos canônicos V4
    - Reporta ausências e inconsistências

Campos obrigatórios V4:
    name, description, project, nucleo, frente, camada,
    categoria, justificativa, verificado_em, version
    
Campos quase-obrigatórios:
    depends_on, chains_to, licoes_aplicadas, regras_aplicaveis,
    recursos_compartilhados, frentes_consultadas
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from resolver_output_root import resolver_skills_root
except ImportError:
    def resolver_skills_root():
        import os
        return Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))


CAMPOS_OBRIGATORIOS = [
    'name', 'description', 'project', 'nucleo', 'frente', 'camada',
    'categoria', 'verificado_em', 'version'
]

CAMPOS_QUASE_OBRIGATORIOS = [
    'justificativa', 'depends_on', 'chains_to',
    'licoes_aplicadas', 'regras_aplicaveis', 'recursos_compartilhados',
]

VALORES_VALIDOS = {
    'project': [f'Proj0{n}' for n in range(1, 8)],
    'nucleo': [f'N{n}' for n in range(1, 7)],
    'frente': ['transversal'] + [f'F{n}' for n in range(1, 7)],
    'camada': [f'C{n}' for n in range(0, 10)],
    'categoria': ['capability', 'preference', 'mista'],
}


def extrair_frontmatter(texto: str) -> dict:
    """Extrai frontmatter YAML do início do SKILL.md."""
    match = re.match(r'^---\n(.*?)\n---\n', texto, re.DOTALL)
    if not match:
        return {}
    yaml_text = match.group(1)
    if HAS_YAML:
        try:
            return yaml.safe_load(yaml_text) or {}
        except Exception:
            return {}
    # Fallback parser simples
    fm = {}
    for line in yaml_text.split('\n'):
        m = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def auditar_frontmatter(skill_dir: Path) -> dict:
    """Audita frontmatter de uma skill."""
    skill_md = skill_dir / 'SKILL.md'
    resultado = {
        'skill': skill_dir.name,
        'arquivo_existe': skill_md.exists(),
        'campos_obrigatorios_ausentes': [],
        'campos_quase_obrigatorios_ausentes': [],
        'valores_invalidos': [],
        'verificado_em_status': None,
        'dias_para_vencer': None,
        'aprovado': False,
    }
    
    if not skill_md.exists():
        resultado['campos_obrigatorios_ausentes'] = ['SKILL.md inexistente']
        return resultado
    
    texto = skill_md.read_text(encoding='utf-8', errors='ignore')
    fm = extrair_frontmatter(texto)
    
    if not fm:
        resultado['campos_obrigatorios_ausentes'] = ['frontmatter ausente ou inválido']
        return resultado
    
    # Campos obrigatórios
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in fm or not fm.get(campo):
            resultado['campos_obrigatorios_ausentes'].append(campo)
    
    # Campos quase-obrigatórios
    for campo in CAMPOS_QUASE_OBRIGATORIOS:
        if campo not in fm:
            resultado['campos_quase_obrigatorios_ausentes'].append(campo)
    
    # Valores válidos
    for campo, valores_ok in VALORES_VALIDOS.items():
        valor = fm.get(campo)
        if valor and valor not in valores_ok:
            resultado['valores_invalidos'].append({
                'campo': campo,
                'valor': valor,
                'esperado': valores_ok,
            })
    
    # verificado_em
    verificado = fm.get('verificado_em')
    if verificado:
        try:
            data = datetime.fromisoformat(str(verificado))
            agora = datetime.now()
            dias_passados = (agora - data).days
            dias_para_vencer = 90 - dias_passados
            resultado['dias_para_vencer'] = dias_para_vencer
            if dias_para_vencer < 0:
                resultado['verificado_em_status'] = 'vencido'
            elif dias_para_vencer < 15:
                resultado['verificado_em_status'] = 'próximo vencer'
            else:
                resultado['verificado_em_status'] = 'válido'
        except Exception:
            resultado['verificado_em_status'] = 'formato inválido'
    
    # Aprovado se zero obrigatórios ausentes e verificado válido
    resultado['aprovado'] = (
        not resultado['campos_obrigatorios_ausentes']
        and not resultado['valores_invalidos']
        and resultado['verificado_em_status'] in ('válido', 'próximo vencer')
    )
    
    return resultado


def imprimir_relatorio(resultado: dict):
    print(f"\nAuditoria de frontmatter: {resultado['skill']}")
    print("=" * 60)
    
    if not resultado['arquivo_existe']:
        print("  🔴 SKILL.md não existe")
        return
    
    if resultado['campos_obrigatorios_ausentes']:
        print(f"  🔴 Campos obrigatórios ausentes: {resultado['campos_obrigatorios_ausentes']}")
    else:
        print("  ✅ Campos obrigatórios: todos presentes")
    
    if resultado['campos_quase_obrigatorios_ausentes']:
        print(f"  🟡 Campos quase-obrigatórios ausentes: {resultado['campos_quase_obrigatorios_ausentes']}")
    
    if resultado['valores_invalidos']:
        print("  🔴 Valores inválidos:")
        for v in resultado['valores_invalidos']:
            print(f"     {v['campo']} = '{v['valor']}' (esperado: {v['esperado'][:3]}...)")
    
    if resultado['verificado_em_status']:
        cor = {'válido': '✅', 'próximo vencer': '🟡', 'vencido': '🔴', 'formato inválido': '🔴'}
        print(f"  {cor.get(resultado['verificado_em_status'], '?')} verificado_em: {resultado['verificado_em_status']}")
        if resultado['dias_para_vencer'] is not None:
            print(f"     Dias até vencer: {resultado['dias_para_vencer']}")
    
    print(f"\n  Status: {'✅ APROVADO' if resultado['aprovado'] else '🔴 REPROVADO'}")


def main():
    if len(sys.argv) < 2:
        print("Uso: auditar_frontmatter.py <skill-path> | --todas", file=sys.stderr)
        sys.exit(1)
    
    biblioteca = resolver_skills_root()
    
    if sys.argv[1] == '--todas':
        for skill in biblioteca.iterdir():
            if skill.is_dir():
                resultado = auditar_frontmatter(skill)
                imprimir_relatorio(resultado)
    else:
        skill = Path(sys.argv[1])
        if not skill.is_absolute():
            skill = biblioteca / skill.name
        resultado = auditar_frontmatter(skill)
        imprimir_relatorio(resultado)


if __name__ == '__main__':
    main()


def auditar_pastas_vs_frontmatter(skill_path: Path) -> list:
    """
    Verifica se pastas declaradas em recursos_compartilhados existem fisicamente.
    Retorna lista de falhas.
    """
    falhas = []
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return ['SKILL.md não encontrado']

    conteudo = skill_md.read_text(encoding='utf-8')
    partes = conteudo.split('---')
    if len(partes) < 3:
        return []

    try:
        if HAS_YAML:
            fm = yaml.safe_load(partes[1])
        else:
            return ['yaml não disponível para verificar recursos_compartilhados']
    except Exception:
        return []

    recursos = fm.get('recursos_compartilhados', {})
    if not isinstance(recursos, dict):
        return []

    # Verificar pastas principais declaradas
    pastas_esperadas = set()
    for categoria, itens in recursos.items():
        if not isinstance(itens, list):
            continue
        for item in itens:
            # Extrair pasta do caminho (ex: MODELOS/secao.md → MODELOS)
            pasta = str(item).split('/')[0]
            if pasta.isupper() or pasta in ['references', 'scripts', 'assets', 'SCHEMAS', 'MODELOS', 'ASSETS']:
                pastas_esperadas.add(pasta)

    for pasta in pastas_esperadas:
        caminho = skill_path / pasta
        if not caminho.exists():
            falhas.append(f'PASTA AUSENTE: {pasta}/ declarada em recursos_compartilhados mas não existe')
        elif not any(caminho.iterdir()):
            falhas.append(f'PASTA VAZIA: {pasta}/ existe mas não tem conteúdo')

    return falhas
