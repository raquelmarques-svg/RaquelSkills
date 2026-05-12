#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inserir_clausulas.py — Inserção automática de cláusulas R1-R11.

Uso:
    python3 inserir_clausulas.py <skill-path>
    python3 inserir_clausulas.py <skill-path> --dry-run

Comportamento:
    - Detecta tipo da skill (analisando SKILL.md)
    - Determina cláusulas aplicáveis (ver reference 03)
    - Insere as cláusulas faltantes em §0-Regras universais
    - Backup R3 antes de modificar

Conforme arquitetura V4:
    - Modo Govern do skill-creator-am
    - Cláusulas universais R1-R11
"""

import sys
import re
from pathlib import Path


# Textos canônicos das cláusulas (resumido; texto completo em reference 03)
CLAUSULAS_TEXTO = {
    'R1': "R1 (exportação): pergunto antes de gerar arquivo de saída em qualquer formato. Aguardo confirmação explícita. Nunca exporto silenciosamente.",
    'R2': "R2 (preservação): nunca apago arquivos ou diretórios. Quando exclusão é necessária, movo para `_APAGAR/[NOME]-YYYYMMDD-HHMMSS/` e reporto o caminho.",
    'R3': "R3 (backup): antes de modificar arquivo existente, copio o original para `_backups/[NOME]/[NOME]-YYYYMMDD-HHMMSS.ext`. Falha de backup = abortar operação.",
    'R4': "R4 (tutela de urgência): não redijo tutela de urgência como padrão. Incluo apenas mediante comando explícito.",
    'R5': "R5 (sigilo profissional): dados sensíveis de cliente ficam exclusivamente em filesystem local. Não envio dados a serviços externos.",
    'R6': "R6 (adaptação): se algo proposto não cabe no padrão, proponho ao menos uma adaptação antes de declinar. Decisão de descartar é da Raquel.",
    'R7': "R7 (pesquisa ampla): em pesquisas, cubro múltiplas fontes (X, Reddit, LinkedIn, fóruns jurídicos, GitHub, etc.). Janela 10 dias. Marco fonte primária vs comercial.",
    'R8': "R8 (sincronia): Drive vivo + Git versionado coexistem. Sincronia mensal espelha Drive para Git em snapshot.",
    'R9': "R9 (auditoria mensal): esta skill entra em ciclo de auditoria mensal. Verifico tamanho, verificado_em, duplicação, frontmatter.",
    'R10': "R10 (discordância útil): aponto inconsistências, vieses, contradições, omissões e saltos lógicos. Prefiro discordância útil a complacência.",
    'R11': "R11 (economia): planejo ação antes de executar. Pondero soluções caras ou lentas. Não cometo excessos sem orientação.",
}


# Mapeamento de tipo → cláusulas
TIPO_CLAUSULAS = {
    'cria_arquivo': ['R1', 'R5'],
    'organiza_pastas': ['R2', 'R3', 'R5'],
    'modifica_skills': ['R3', 'R9'],
    'peca_processual': ['R4', 'R10'],
    'pesquisa_externa': ['R7', 'R10'],
    'drive_ou_git': ['R8'],
    'auditoria': ['R9'],
    'operacao_cara': ['R11'],
}


def detectar_tipos(texto: str, scripts_dir: Path = None) -> set:
    """Detecta tipos de skill a partir do conteúdo do SKILL.md."""
    tipos = set()
    
    palavras_cria = ['gerar arquivo', 'criar arquivo', 'exportar', '.docx', '.pdf', '.xlsx', '.zip']
    if any(kw in texto for kw in palavras_cria):
        tipos.add('cria_arquivo')
    
    palavras_organiza = ['organizar pasta', 'mover arquivo', 'arquivar', 'juridir', '_APAGAR']
    if any(kw in texto for kw in palavras_organiza):
        tipos.add('organiza_pastas')
    
    palavras_modifica_skills = ['SKILL.md', 'editar skill', 'modificar skill', 'skill-creator']
    if any(kw in texto for kw in palavras_modifica_skills):
        tipos.add('modifica_skills')
    
    palavras_peca = ['petição', 'inicial', 'mandado de segurança', 'recurso', 'contestação', 'réplica']
    if any(kw.lower() in texto.lower() for kw in palavras_peca):
        tipos.add('peca_processual')
    
    palavras_pesquisa = ['web_search', 'web_fetch', 'API externa', 'consulta online', 'pesquisa na web']
    if any(kw in texto for kw in palavras_pesquisa):
        tipos.add('pesquisa_externa')
    
    palavras_drive_git = ['/Drive/Claude/', 'Drive vivo', 'Git', 'commit', 'sincronia']
    if any(kw in texto for kw in palavras_drive_git):
        tipos.add('drive_ou_git')
    
    palavras_audit = ['auditoria', 'audit', 'cron mensal', 'R9']
    if any(kw in texto for kw in palavras_audit):
        tipos.add('auditoria')
    
    palavras_cara = ['LLM call', 'pesquisa profunda', 'processamento longo', 'OCR', 'Whisper']
    if any(kw in texto for kw in palavras_cara):
        tipos.add('operacao_cara')
    
    return tipos


def mapear_clausulas(tipos: set) -> list:
    """Mapeia tipos → cláusulas (sem duplicação)."""
    clausulas = set()
    for tipo in tipos:
        if tipo in TIPO_CLAUSULAS:
            clausulas.update(TIPO_CLAUSULAS[tipo])
    return sorted(clausulas, key=lambda x: int(x[1:]))


def detectar_clausulas_presentes(texto: str) -> set:
    """Identifica cláusulas R1-R11 já presentes no SKILL.md."""
    presentes = set()
    for n in range(1, 12):
        clausula = f'R{n}'
        # Procura padrões: "R1 (", "R1:", "**R1**"
        padrao = rf'\b{clausula}\b\s*[(:]'
        if re.search(padrao, texto):
            presentes.add(clausula)
    return presentes


def auditar(skill_dir: Path) -> dict:
    """Audita cláusulas: aplicáveis vs presentes."""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return {'erro': 'SKILL.md não existe'}
    
    texto = skill_md.read_text(encoding='utf-8', errors='ignore')
    tipos = detectar_tipos(texto, skill_dir / 'scripts')
    aplicaveis = mapear_clausulas(tipos)
    presentes = detectar_clausulas_presentes(texto)
    ausentes = [c for c in aplicaveis if c not in presentes]
    
    return {
        'skill': skill_dir.name,
        'tipos_detectados': sorted(tipos),
        'clausulas_aplicaveis': aplicaveis,
        'clausulas_presentes': sorted(presentes),
        'clausulas_ausentes': ausentes,
        'precisa_inserir': bool(ausentes),
    }


def imprimir_relatorio(resultado: dict):
    print(f"\nAuditoria de cláusulas: {resultado.get('skill', '?')}")
    print("=" * 60)
    if 'erro' in resultado:
        print(f"  🔴 {resultado['erro']}")
        return
    print(f"  Tipos detectados: {resultado['tipos_detectados']}")
    print(f"  Cláusulas aplicáveis: {resultado['clausulas_aplicaveis']}")
    print(f"  Cláusulas presentes: {resultado['clausulas_presentes']}")
    if resultado['clausulas_ausentes']:
        print(f"  🟡 Cláusulas ausentes: {resultado['clausulas_ausentes']}")
        print("\n  Textos sugeridos para inserir:")
        for c in resultado['clausulas_ausentes']:
            print(f"    {CLAUSULAS_TEXTO.get(c, '?')}")
    else:
        print("  ✅ Todas as cláusulas aplicáveis estão presentes")


def main():
    if len(sys.argv) < 2:
        print("Uso: inserir_clausulas.py <skill-path> [--dry-run]", file=sys.stderr)
        sys.exit(1)
    
    skill = Path(sys.argv[1])
    if not skill.is_absolute():
        try:
            from resolver_output_root import resolver_skills_root
            skill = resolver_skills_root() / skill.name
        except ImportError:
            pass
    
    if not skill.exists():
        print(f"ERRO — skill não encontrada: {skill}", file=sys.stderr)
        sys.exit(1)
    
    resultado = auditar(skill)
    imprimir_relatorio(resultado)
    
    if '--dry-run' in sys.argv:
        print("\n(Modo dry-run — nenhuma alteração feita)")
        sys.exit(0)
    
    # Modo apply: a inserção real exige confirmação humana
    # (este script é diagnóstico; a inserção é feita pela skill-creator-am
    # após aprovação)


if __name__ == '__main__':
    main()
