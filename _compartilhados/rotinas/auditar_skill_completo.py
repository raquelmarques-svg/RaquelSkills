#!/usr/bin/env python3
"""
auditar_skill_completo.py — Orquestrador R9 (auditoria mensal).

Uso:
    python3 auditar_skill_completo.py <skill-path>
    python3 auditar_skill_completo.py --todas
    python3 auditar_skill_completo.py --todas --salvar

Comportamento:
    Roda as 12 auditorias pos-criacao em sequencia.
    Coleta resultados, prioriza achados (vermelho > amarelo > verde).
    Gera relatorio consolidado por skill.
    Opcao --salvar grava em governanca/audit-YYYYMM.md.

Conforme arquitetura V4:
    - Cláusula R9 (auditoria mensal)
    - Modo Audit do skill-creator-am
    - 12 auditorias documentadas em references/02-auditorias-pos-criacao.md
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

# Imports relativos aos outros scripts
sys.path.insert(0, str(Path(__file__).parent))

try:
    from resolver_output_root import resolver_skills_root, resolver
except ImportError:
    import os
    def resolver_skills_root():
        return Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))
    def resolver():
        return Path(os.environ.get('RAQUEL_OUTPUT_ROOT', 'C:/RaquelSkills/outputs'))

try:
    from auditar_tamanho import auditar_skill as auditar_tamanho_skill
except ImportError:
    auditar_tamanho_skill = None

try:
    from auditar_frontmatter import auditar_frontmatter
except ImportError:
    auditar_frontmatter = None

try:
    from inserir_clausulas import auditar as auditar_clausulas
except ImportError:
    auditar_clausulas = None

try:
    from verificar_duplicacao import verificar_skill_unica
except ImportError:
    verificar_skill_unica = None


LIMITES_DESCRIPTION = 1024  # L11 — limite Anthropic


def extrair_frontmatter_dict(skill_md_path: Path) -> dict:
    """Parse de frontmatter retornando dict."""
    if not skill_md_path.exists():
        return {}
    texto = skill_md_path.read_text(encoding='utf-8', errors='ignore')
    m = re.match(r'^---\n(.*?)\n---\n', texto, re.DOTALL)
    if not m:
        return {}
    yaml_text = m.group(1)
    try:
        import yaml
        return yaml.safe_load(yaml_text) or {}
    except ImportError:
        fm = {}
        for line in yaml_text.split('\n'):
            mm = re.match(r'^([a-z_]+):\s*(.*)$', line)
            if mm:
                fm[mm.group(1)] = mm.group(2).strip()
        return fm


def auditoria_5_description_diretiva(skill_dir: Path) -> dict:
    """A5 — Descrição diretiva. Verifica formato VERBO + GATILHOS + PROIBIÇÃO + limite chars."""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return {'status': 'vermelho', 'detalhe': 'SKILL.md inexistente'}
    
    texto = skill_md.read_text(encoding='utf-8', errors='ignore')
    m = re.match(r'^---\n(.*?)\n---\n', texto, re.DOTALL)
    if not m:
        return {'status': 'vermelho', 'detalhe': 'frontmatter ausente'}
    
    fm = m.group(1)
    desc_match = re.search(r'^description: \|\n((?:  .*\n)+)', fm, re.MULTILINE)
    if not desc_match:
        desc_match = re.search(r'^description:\s+(.*?)$', fm, re.MULTILINE)
        if not desc_match:
            return {'status': 'vermelho', 'detalhe': 'description ausente'}
        desc = desc_match.group(1)
    else:
        desc = '\n'.join(line[2:] if line.startswith('  ') else line for line in desc_match.group(1).split('\n')).rstrip()
    
    achados = []
    
    if len(desc) > LIMITES_DESCRIPTION:
        achados.append(f'description {len(desc)} chars > {LIMITES_DESCRIPTION} (L11 violado)')
    
    primeira_palavra = desc.split()[0] if desc.split() else ''
    verbos_validos = {'Cria', 'Gera', 'Audita', 'Organiza', 'Calcula', 'Monitor', 'Crie',
                       'Gere', 'Audite', 'Organize', 'Calcule', 'Monitore', 'Produz',
                       'Analisa', 'Verifica', 'Refator', 'Extrai', 'Detecta', 'Aplica'}
    if not any(primeira_palavra.startswith(v) for v in verbos_validos):
        achados.append(f'primeira palavra "{primeira_palavra}" nao e verbo imperativo')
    
    if 'INVOQUE' not in desc and 'Gatilhos' not in desc and 'invoque' not in desc.lower():
        achados.append('"INVOQUE quando" ou "Gatilhos" ausente')
    
    if 'NÃO use' not in desc and 'Não use' not in desc and 'NAO use' not in desc:
        achados.append('proibicao inversa ("NÃO use para") ausente')
    
    if achados:
        return {'status': 'vermelho' if len(desc) > LIMITES_DESCRIPTION else 'amarelo',
                'detalhe': '; '.join(achados), 'chars': len(desc)}
    return {'status': 'verde', 'chars': len(desc)}


def auditoria_9_casos_teste(skill_dir: Path) -> dict:
    """A9 — Casos-teste presentes (3 positivos + 2 negativos)."""
    examples = skill_dir / 'examples'
    if not examples.exists():
        return {'status': 'vermelho', 'detalhe': 'pasta examples/ nao existe'}
    positivos = list(examples.glob('caso-positivo-*.md'))
    negativos = list(examples.glob('caso-negativo-*.md'))
    achados = []
    if len(positivos) < 3:
        achados.append(f'positivos: {len(positivos)}/3')
    if len(negativos) < 2:
        achados.append(f'negativos: {len(negativos)}/2')
    if achados:
        return {'status': 'amarelo' if (len(positivos) + len(negativos)) >= 3 else 'vermelho',
                'detalhe': '; '.join(achados)}
    return {'status': 'verde', 'detalhe': f'{len(positivos)}+{len(negativos)}'}


def auditoria_12_verificado_em(fm: dict) -> dict:
    """A12 — verificado_em <= 90 dias."""
    verificado = fm.get('verificado_em')
    if not verificado:
        return {'status': 'vermelho', 'detalhe': 'campo ausente'}
    try:
        data = datetime.fromisoformat(str(verificado))
        dias_passados = (datetime.now() - data).days
        dias_restantes = 90 - dias_passados
        if dias_restantes < 0:
            return {'status': 'vermelho', 'detalhe': f'vencido ha {abs(dias_restantes)} dias'}
        elif dias_restantes < 15:
            return {'status': 'amarelo', 'detalhe': f'vence em {dias_restantes} dias'}
        return {'status': 'verde', 'detalhe': f'{dias_restantes} dias restantes'}
    except Exception as e:
        return {'status': 'vermelho', 'detalhe': f'data invalida: {e}'}


def auditar_skill_completo(skill_dir: Path, biblioteca: Path = None) -> dict:
    """Roda todas as 12 auditorias em sequencia."""
    resultado = {
        'skill': skill_dir.name,
        'timestamp': datetime.now().isoformat(),
        'auditorias': {},
        'score': 100,
        'classificacao': '',
    }
    
    fm = extrair_frontmatter_dict(skill_dir / 'SKILL.md')
    
    # A1 Tamanho
    if auditar_tamanho_skill:
        r = auditar_tamanho_skill(skill_dir)
        resultado['auditorias']['A1_tamanho'] = {
            'status': {'verde': 'verde', 'amarelo': 'amarelo', 'laranja': 'amarelo', 'vermelho': 'vermelho'}.get(r.get('status_geral'), 'amarelo'),
            'detalhe': f"SKILL.md {r.get('SKILL.md', {}).get('linhas', '?')} linhas"
        }
    
    # A2 Frontmatter
    if auditar_frontmatter:
        r = auditar_frontmatter(skill_dir)
        if r.get('aprovado'):
            resultado['auditorias']['A2_frontmatter'] = {'status': 'verde', 'detalhe': 'completo'}
        elif r.get('campos_obrigatorios_ausentes'):
            resultado['auditorias']['A2_frontmatter'] = {
                'status': 'vermelho',
                'detalhe': f"ausentes: {r['campos_obrigatorios_ausentes']}"
            }
        else:
            resultado['auditorias']['A2_frontmatter'] = {'status': 'amarelo', 'detalhe': 'parcial'}
    
    # A3 Licoes (verificacao heuristica)
    licoes = fm.get('licoes_aplicadas', [])
    if isinstance(licoes, list) and licoes:
        resultado['auditorias']['A3_licoes'] = {'status': 'verde', 'detalhe': f'{len(licoes)} aplicadas'}
    else:
        resultado['auditorias']['A3_licoes'] = {'status': 'amarelo', 'detalhe': 'lista vazia ou ausente'}
    
    # A4 Clausulas
    if auditar_clausulas:
        r = auditar_clausulas(skill_dir)
        ausentes = r.get('clausulas_ausentes', [])
        if ausentes:
            resultado['auditorias']['A4_clausulas'] = {'status': 'amarelo',
                'detalhe': f"ausentes: {ausentes}"}
        else:
            resultado['auditorias']['A4_clausulas'] = {'status': 'verde', 'detalhe': 'completo'}
    
    # A5 Descricao diretiva (inclui L11)
    resultado['auditorias']['A5_descricao'] = auditoria_5_description_diretiva(skill_dir)
    
    # A6 Pragmatica - manual, marcar amarelo padrao
    resultado['auditorias']['A6_pragmatica'] = {'status': 'amarelo', 'detalhe': 'avaliacao manual'}
    
    # A7 12 dimensoes - so se categoria producao texto
    if fm.get('categoria') == 'capability' and any(
        kw in str(fm.get('description', '')).lower() for kw in ['peticao', 'recurso', 'replica']
    ):
        resultado['auditorias']['A7_dimensoes'] = {'status': 'amarelo', 'detalhe': 'avaliacao manual'}
    else:
        resultado['auditorias']['A7_dimensoes'] = {'status': 'verde', 'detalhe': 'N/A'}
    
    # A8 Vocabulario - manual
    resultado['auditorias']['A8_vocabulario'] = {'status': 'amarelo', 'detalhe': 'avaliacao manual'}
    
    # A9 Casos-teste
    resultado['auditorias']['A9_casos_teste'] = auditoria_9_casos_teste(skill_dir)
    
    # A10 Duplicacao
    if verificar_skill_unica and biblioteca:
        r = verificar_skill_unica(skill_dir, biblioteca)
        if r.get('total_bloqueio', 0) > 0:
            resultado['auditorias']['A10_duplicacao'] = {'status': 'vermelho',
                'detalhe': f"{r['total_bloqueio']} bloqueio"}
        elif r.get('total_alerta', 0) > 0:
            resultado['auditorias']['A10_duplicacao'] = {'status': 'amarelo',
                'detalhe': f"{r['total_alerta']} alerta"}
        else:
            resultado['auditorias']['A10_duplicacao'] = {'status': 'verde', 'detalhe': 'sem duplicacao'}
    
    # A11 Dependencias - heuristica
    depends = fm.get('depends_on', [])
    chains = fm.get('chains_to', [])
    if depends or chains:
        resultado['auditorias']['A11_dependencias'] = {'status': 'verde', 'detalhe': f'd:{len(depends or [])} c:{len(chains or [])}'}
    else:
        resultado['auditorias']['A11_dependencias'] = {'status': 'amarelo', 'detalhe': 'sem dependencias declaradas'}
    
    # A12 verificado_em
    resultado['auditorias']['A12_verificado_em'] = auditoria_12_verificado_em(fm)
    
    # Score
    score = 100
    for a, dado in resultado['auditorias'].items():
        if dado.get('status') == 'vermelho':
            score -= 10
        elif dado.get('status') == 'amarelo':
            score -= 3
    resultado['score'] = max(score, 0)
    
    if score >= 90:
        resultado['classificacao'] = 'Excelente'
    elif score >= 75:
        resultado['classificacao'] = 'Boa'
    elif score >= 60:
        resultado['classificacao'] = 'Regular'
    elif score >= 40:
        resultado['classificacao'] = 'Atencao'
    else:
        resultado['classificacao'] = 'Critica'
    
    return resultado


def imprimir_relatorio(resultado: dict):
    cor = {'verde': 'verde', 'amarelo': 'amarelo', 'vermelho': 'vermelho'}
    print(f"\nAuditoria completa: {resultado['skill']}")
    print(f"Timestamp: {resultado['timestamp']}")
    print("=" * 70)
    for nome, dado in resultado['auditorias'].items():
        status = dado.get('status', '?')
        detalhe = dado.get('detalhe', '')
        print(f"  [{status:>8}] {nome}: {detalhe}")
    print(f"\nScore: {resultado['score']}/100")
    print(f"Classificacao: {resultado['classificacao']}")


def main():
    if len(sys.argv) < 2:
        print("Uso: auditar_skill_completo.py <skill-path> | --todas [--salvar]", file=sys.stderr)
        sys.exit(1)
    
    biblioteca = resolver_skills_root()
    salvar = '--salvar' in sys.argv
    
    if sys.argv[1] == '--todas':
        resultados = []
        for skill in sorted(biblioteca.iterdir()):
            if skill.is_dir() and (skill / 'SKILL.md').exists():
                r = auditar_skill_completo(skill, biblioteca)
                imprimir_relatorio(r)
                resultados.append(r)
        if salvar:
            mes = datetime.now().strftime('%Y%m')
            saida = resolver().parent / 'governanca' / f'audit-{mes}.md'
            saida.parent.mkdir(parents=True, exist_ok=True)
            with saida.open('w', encoding='utf-8') as f:
                f.write(f"# Auditoria R9 - {mes}\n\n")
                for r in resultados:
                    f.write(f"## {r['skill']}\n\n")
                    f.write(f"Score: {r['score']}/100 ({r['classificacao']})\n\n")
                    for nome, dado in r['auditorias'].items():
                        f.write(f"- {nome}: {dado.get('status')} — {dado.get('detalhe','')}\n")
                    f.write("\n")
            print(f"\n+ Salvo em: {saida}")
    else:
        skill = Path(sys.argv[1])
        if not skill.is_absolute():
            skill = biblioteca / skill.name
        if not skill.exists():
            print(f"ERRO: {skill} nao encontrada", file=sys.stderr)
            sys.exit(1)
        r = auditar_skill_completo(skill, biblioteca)
        imprimir_relatorio(r)


if __name__ == '__main__':
    main()
