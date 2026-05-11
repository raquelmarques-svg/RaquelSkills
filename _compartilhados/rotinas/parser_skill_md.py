#!/usr/bin/env python3
"""
parser_skill_md.py — Parse e edicao estrutural de SKILL.md.

Uso programatico:
    from parser_skill_md import SkillMD
    sm = SkillMD('caminho/SKILL.md')
    sm.frontmatter['version']           # le campo
    sm.set_frontmatter('version', '1.0.1')
    sm.set_frontmatter('verificado_em', '2026-05-11')
    sm.inserir_apos_secao('§0', 'novo conteudo')
    sm.inserir_secao('§0-Regras universais', conteudo, posicao='depois de §0')
    sm.save()                            # grava com backup R3

Uso CLI:
    python3 parser_skill_md.py <skill-md-path> info
    python3 parser_skill_md.py <skill-md-path> listar-secoes
    python3 parser_skill_md.py <skill-md-path> ler-secao "§1"

Conforme arquitetura V4:
    - Backup R3 antes de qualquer save
    - Estrutura §0…§N preservada
    - Frontmatter YAML preservado em ordem
"""

import sys
import re
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


class SkillMD:
    """Parser e editor estrutural de um SKILL.md."""
    
    def __init__(self, path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"SKILL.md nao existe: {self.path}")
        self._texto = self.path.read_text(encoding='utf-8')
        self._parse()
    
    def _parse(self):
        """Separa frontmatter, corpo e secoes."""
        m = re.match(r'^---\n(.*?)\n---\n', self._texto, re.DOTALL)
        if not m:
            self._frontmatter_raw = ''
            self.frontmatter = {}
            self._corpo = self._texto
        else:
            self._frontmatter_raw = m.group(1)
            self._corpo = self._texto[m.end():]
            self.frontmatter = self._parse_yaml_simples(self._frontmatter_raw)
        self._mapear_secoes()
    
    def _parse_yaml_simples(self, yaml_text: str) -> dict:
        """Parser YAML minimo (sem dependencia externa)."""
        try:
            import yaml
            return yaml.safe_load(yaml_text) or {}
        except ImportError:
            pass
        fm = {}
        current_key = None
        current_block = []
        for line in yaml_text.split('\n'):
            # Bloco multilinha (|)
            if current_key and (line.startswith('  ') or line == ''):
                current_block.append(line[2:] if line.startswith('  ') else line)
                continue
            if current_key:
                fm[current_key] = '\n'.join(current_block).rstrip()
                current_key = None
                current_block = []
            m = re.match(r'^([a-z_]+):\s*\|\s*$', line)
            if m:
                current_key = m.group(1)
                continue
            m = re.match(r'^([a-z_]+):\s*(.*)$', line)
            if m:
                fm[m.group(1)] = m.group(2).strip()
        if current_key:
            fm[current_key] = '\n'.join(current_block).rstrip()
        return fm
    
    def _mapear_secoes(self):
        """Mapeia secoes (## §N — Titulo) no corpo."""
        self.secoes = {}
        self._secoes_ordem = []
        padrao = r'^## (§[\w\-]+(?:[ -][^\n]+)?)\s*$'
        matches = list(re.finditer(padrao, self._corpo, re.MULTILINE))
        for i, m in enumerate(matches):
            nome = m.group(1).strip()
            inicio = m.start()
            fim = matches[i+1].start() if i+1 < len(matches) else len(self._corpo)
            self.secoes[nome] = {
                'titulo_completo': nome,
                'inicio': inicio,
                'fim': fim,
                'texto': self._corpo[inicio:fim],
            }
            self._secoes_ordem.append(nome)
    
    def set_frontmatter(self, campo: str, valor):
        """Atualiza um campo do frontmatter."""
        self.frontmatter[campo] = valor
    
    def ler_secao(self, ident: str) -> str:
        """Retorna texto de uma secao (busca por prefixo, ex.: '§1')."""
        for nome, dado in self.secoes.items():
            if nome.startswith(ident):
                return dado['texto']
        return ''
    
    def inserir_apos_secao(self, ident: str, texto_novo: str):
        """Insere texto logo apos a secao identificada."""
        for nome, dado in self.secoes.items():
            if nome.startswith(ident):
                fim = dado['fim']
                novo = "\n" + texto_novo.rstrip() + "\n\n"
                self._corpo = self._corpo[:fim] + novo + self._corpo[fim:]
                self._mapear_secoes()
                return True
        raise KeyError(f"Secao nao encontrada: {ident}")
    
    def inserir_em_secao(self, ident: str, texto_novo: str):
        """Anexa texto ao final de uma secao existente."""
        for nome, dado in self.secoes.items():
            if nome.startswith(ident):
                # Inserir antes do final da secao (preservando blank lines)
                inicio_proxima = dado['fim']
                # Recuar ate ultimo conteudo nao-vazio
                pos = inicio_proxima - 1
                while pos > dado['inicio'] and self._corpo[pos] in '\n ':
                    pos -= 1
                pos += 1  # apos ultimo conteudo
                novo = "\n" + texto_novo.rstrip() + "\n"
                self._corpo = self._corpo[:pos] + novo + self._corpo[pos:]
                self._mapear_secoes()
                return True
        raise KeyError(f"Secao nao encontrada: {ident}")
    
    def _serializar_frontmatter(self) -> str:
        """Re-serializa o frontmatter mantendo ordem original quando possivel."""
        # Estrategia: re-usa raw, atualizando apenas chaves modificadas
        # via str_replace simples. Para robustez total, usar pyyaml.
        try:
            import yaml
            return yaml.safe_dump(self.frontmatter, allow_unicode=True,
                                  sort_keys=False, default_flow_style=False)
        except ImportError:
            pass
        # Fallback: usar raw original (nao reflete mudancas em frontmatter)
        return self._frontmatter_raw
    
    def save(self, criar_backup: bool = True):
        """Grava SKILL.md com backup R3."""
        if criar_backup:
            self._backup_r3()
        novo_texto = "---\n" + self._serializar_frontmatter() + "---\n" + self._corpo
        self.path.write_text(novo_texto, encoding='utf-8')
    
    def _backup_r3(self):
        """Backup R3 obrigatorio."""
        import os
        raiz = os.environ.get('RAQUEL_SKILLS_ROOT', '')
        if raiz:
            backup_root = Path(raiz) / '_backups' / self.path.name
        else:
            backup_root = self.path.parent / '_backups' / self.path.name
        backup_root.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        dest = backup_root / f"{self.path.stem}-{timestamp}{self.path.suffix}"
        shutil.copy2(self.path, dest)
        if not dest.exists():
            raise RuntimeError(f"Backup R3 falhou: {dest}")


# CLI
def main():
    if len(sys.argv) < 3:
        print("Uso: parser_skill_md.py <skill-md-path> {info|listar-secoes|ler-secao <id>}", file=sys.stderr)
        sys.exit(1)
    
    sm = SkillMD(sys.argv[1])
    cmd = sys.argv[2]
    
    if cmd == 'info':
        print(f"Skill: {sm.frontmatter.get('name', '?')}")
        print(f"Versao: {sm.frontmatter.get('version', '?')}")
        print(f"Project: {sm.frontmatter.get('project', '?')}")
        print(f"Camada: {sm.frontmatter.get('camada', '?')}")
        print(f"Verificado em: {sm.frontmatter.get('verificado_em', '?')}")
        print(f"Total de secoes: {len(sm.secoes)}")
    elif cmd == 'listar-secoes':
        for nome in sm._secoes_ordem:
            dado = sm.secoes[nome]
            linhas = dado['texto'].count('\n')
            print(f"  {nome}  ({linhas} linhas)")
    elif cmd == 'ler-secao':
        if len(sys.argv) < 4:
            print("ler-secao requer identificador da secao", file=sys.stderr)
            sys.exit(1)
        print(sm.ler_secao(sys.argv[3]))
    else:
        print(f"Comando desconhecido: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
