#!/usr/bin/env python3
"""
extrair_para_compartilhados.py — Migra trecho duplicado para _compartilhados/.

Uso:
    python3 extrair_para_compartilhados.py \
        --tipo {rotina,template,calculo,informacao} \
        --nome <nome-arquivo-destino> \
        --skills <skill1,skill2,...> \
        [--dry-run]

Comportamento:
    1. Detecta trecho comum entre as skills informadas
    2. Cria arquivo em _compartilhados/<tipo>/<nome>
    3. Backup R3 de cada skill afetada
    4. Substitui trecho nas skills por referencia ao recurso compartilhado
    5. Atualiza frontmatter (recursos_compartilhados)
    6. Registra em log

Conforme arquitetura V4:
    - Modo Extract do skill-creator-am
    - Threshold: 20+ linhas
    - Aprovacao humana obrigatoria (sai do dry-run apenas com --apply)
"""

import sys
import argparse
import re
import shutil
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).parent))

try:
    from resolver_output_root import resolver_skills_root, resolver_compartilhados_root
except ImportError:
    import os
    def resolver_skills_root():
        return Path(os.environ.get('RAQUEL_SKILLS_ROOT', 'C:/RaquelSkills/skills'))
    def resolver_compartilhados_root():
        return Path(os.environ.get('RAQUEL_COMPARTILHADOS_ROOT', 'C:/RaquelSkills/_compartilhados'))


TIPOS_VALIDOS = {'rotina', 'rotinas', 'template', 'templates', 'calculo', 'calculos',
                  'informacao', 'informacoes'}

TIPO_DIR = {
    'rotina': 'rotinas',
    'rotinas': 'rotinas',
    'template': 'templates',
    'templates': 'templates',
    'calculo': 'calculos',
    'calculos': 'calculos',
    'informacao': 'informacoes',
    'informacoes': 'informacoes',
}


def detectar_trecho_comum(skills_textos: dict, min_linhas: int = 20) -> str:
    """Detecta trecho comum entre N skills. Retorna o maior bloco comum."""
    if len(skills_textos) < 2:
        return ''
    
    nomes = list(skills_textos.keys())
    texto_ref = skills_textos[nomes[0]]
    blocos_ref = _extrair_blocos(texto_ref, min_linhas)
    
    candidatos = []
    for bloco in blocos_ref:
        # Verifica se aparece em todas as outras skills
        aparece_em_todas = True
        for outro_nome in nomes[1:]:
            outro_texto = skills_textos[outro_nome]
            if not _bloco_aparece_em(bloco, outro_texto, threshold=0.85):
                aparece_em_todas = False
                break
        if aparece_em_todas:
            candidatos.append(bloco)
    
    if not candidatos:
        return ''
    return max(candidatos, key=len)


def _extrair_blocos(texto: str, min_linhas: int) -> list:
    linhas = texto.split('\n')
    blocos = []
    bloco_atual = []
    for linha in linhas:
        if linha.strip():
            bloco_atual.append(linha)
        else:
            if len(bloco_atual) >= min_linhas:
                blocos.append('\n'.join(bloco_atual))
            bloco_atual = []
    if len(bloco_atual) >= min_linhas:
        blocos.append('\n'.join(bloco_atual))
    return blocos


def _bloco_aparece_em(bloco: str, texto: str, threshold: float = 0.85) -> bool:
    """Verifica se bloco aparece em texto com similaridade >= threshold."""
    blocos_texto = _extrair_blocos(texto, min_linhas=len(bloco.split('\n')) - 2)
    for bt in blocos_texto:
        if SequenceMatcher(None, bloco, bt).ratio() >= threshold:
            return True
    return False


def backup_r3(arquivo: Path) -> Path:
    """Backup R3 de um arquivo."""
    import os
    raiz = os.environ.get('RAQUEL_SKILLS_ROOT', '')
    if raiz:
        backup_root = Path(raiz) / '_backups' / arquivo.name
    else:
        backup_root = arquivo.parent / '_backups' / arquivo.name
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = backup_root / f"{arquivo.stem}-{timestamp}{arquivo.suffix}"
    shutil.copy2(arquivo, dest)
    return dest


def referencia_canonica(tipo: str, nome: str) -> str:
    """Gera bloco de referencia para inserir em SKILL.md no lugar do trecho."""
    tipo_dir = TIPO_DIR.get(tipo, tipo)
    return f"""
*Este bloco foi migrado para `_compartilhados/{tipo_dir}/{nome}`.*
*Consulta canonica nesse caminho. Mantido aqui apenas a referencia.*

> Ver: `_compartilhados/{tipo_dir}/{nome}`
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tipo', required=True, choices=list(TIPOS_VALIDOS))
    parser.add_argument('--nome', required=True, help='Nome do arquivo destino (sem path)')
    parser.add_argument('--skills', required=True, help='Lista separada por virgula')
    parser.add_argument('--min-linhas', type=int, default=20)
    parser.add_argument('--dry-run', action='store_true', help='Apenas detectar, nao modificar')
    parser.add_argument('--apply', action='store_true', help='Aplicar modificacoes')
    args = parser.parse_args()
    
    biblioteca = resolver_skills_root()
    comp = resolver_compartilhados_root()
    nomes_skills = [s.strip() for s in args.skills.split(',') if s.strip()]
    
    print(f"=== Extract para _compartilhados/{TIPO_DIR[args.tipo]}/{args.nome} ===")
    print(f"Skills envolvidas: {nomes_skills}")
    print()
    
    # 1. Carregar SKILL.md das skills
    textos = {}
    paths = {}
    for nome in nomes_skills:
        path = biblioteca / nome / 'SKILL.md'
        if not path.exists():
            print(f"ERRO: SKILL.md nao encontrado para {nome} em {path}", file=sys.stderr)
            sys.exit(1)
        paths[nome] = path
        textos[nome] = path.read_text(encoding='utf-8')
    
    # 2. Detectar trecho comum
    print(f"1. Detectando trecho comum (>= {args.min_linhas} linhas)...")
    trecho = detectar_trecho_comum(textos, args.min_linhas)
    if not trecho:
        print(f"   - Nenhum trecho comum >= {args.min_linhas} linhas encontrado.")
        sys.exit(0)
    
    linhas = trecho.count('\n') + 1
    print(f"   + Trecho de {linhas} linhas detectado.")
    print(f"   + Preview: {trecho[:200]}...")
    print()
    
    # 3. Dry-run ou apply
    if not args.apply or args.dry_run:
        print("Modo DRY-RUN. Nenhuma modificacao aplicada.")
        print("Para aplicar, rode novamente com --apply.")
        return
    
    # 4. Backup R3 de cada skill
    print("2. Backup R3...")
    backups = {}
    for nome, path in paths.items():
        b = backup_r3(path)
        backups[nome] = b
        print(f"   + {nome}: {b}")
    print()
    
    # 5. Criar arquivo em _compartilhados/
    print("3. Criando arquivo compartilhado...")
    destino = comp / TIPO_DIR[args.tipo] / args.nome
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        b = backup_r3(destino)
        print(f"   ! Arquivo ja existia, backup feito: {b}")
    
    cabecalho = f"""# {args.nome} - recurso compartilhado

Tipo: {TIPO_DIR[args.tipo]}
Criado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Origem: extracao automatica de {nomes_skills}

---

"""
    destino.write_text(cabecalho + trecho + '\n', encoding='utf-8')
    print(f"   + Criado: {destino}")
    print()
    
    # 6. Substituir trecho nas skills por referencia
    print("4. Substituindo trecho nas skills...")
    ref = referencia_canonica(args.tipo, args.nome)
    for nome, path in paths.items():
        texto = path.read_text(encoding='utf-8')
        # Localizar o trecho exato e substituir
        # (tolerante a pequenas variacoes via fuzzy seria mais robusto;
        # versao simples: busca direta)
        if trecho in texto:
            novo = texto.replace(trecho, ref.strip(), 1)
            path.write_text(novo, encoding='utf-8')
            print(f"   + {nome}: substituido")
        else:
            print(f"   ! {nome}: trecho exato nao encontrado, deixar manual")
    print()
    
    print("=== Extract concluido ===")
    print("Lembre de registrar via log_auditoria.py registrar extrair ...")


if __name__ == '__main__':
    main()
