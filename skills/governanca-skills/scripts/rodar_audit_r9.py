#!/usr/bin/env python3
"""
rodar_audit_r9.py — Auditoria R9 da biblioteca de skills Almeida Marques (A1-A21)

Uso:
    python3 rodar_audit_r9.py [--skills-dir CAMINHO] [--modo completo|rapido]

Saída: relatório de texto no stdout + arquivo audit_YYYY-MM-DD.txt no diretório corrente
"""

import os
import sys
import re
import yaml
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path


# ── Configuração ──────────────────────────────────────────────────────────────

BLOQUEANTES = {
    "A1", "A2", "A4", "A5", "A7", "A11", "A12", "A16", "A17", "A18", "A19", "A20"
}

CAMPOS_V4_OBRIGATORIOS = [
    "name", "description", "project", "nucleo", "frente", "camada",
    "categoria", "justificativa", "version", "verificado_em",
    "git_repo", "git_auto_commit", "depends_on", "chains_to"
]

FRASES_CONTEXTO_IMPLICITO = [
    "com base no que foi feito antes",
    "usando o contexto anterior",
    "conforme discutido anteriormente",
    "como analisado acima",
    "a partir da análise anterior",
    "com base na análise feita anteriormente",
    "usando o que foi levantado",
]


def parse_skill(skill_dir: Path):
    """Lê SKILL.md e retorna (frontmatter_dict, body_text, n_lines)."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None, None, 0
    raw = skill_file.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    n_lines = len(lines)

    # Extrai frontmatter YAML
    fm = {}
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            try:
                fm = yaml.safe_load(raw[3:end]) or {}
            except yaml.YAMLError:
                fm = {}
    body = raw
    return fm, body, n_lines


def get_installed_skills(skills_dir: Path):
    """Retorna set com nomes de skills que têm SKILL.md."""
    installed = set()
    for d in skills_dir.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            installed.add(d.name)
    return installed


def audit_skill(name: str, skill_dir: Path, installed: set, modo: str):
    """Executa A1-A21 e retorna lista de (codigo, nivel, descricao)."""
    fm, body, n_lines = parse_skill(skill_dir)
    issues = []

    def add(code, nivel, desc):
        issues.append((code, nivel, desc))

    if fm is None:
        add("A2", "BLOQUEANTE", "SKILL.md ausente")
        return issues

    # A1 — tamanho
    if n_lines > 500:
        add("A1", "BLOQUEANTE", f"{n_lines} linhas (limite: 500)")

    # A2 — frontmatter V4
    for campo in CAMPOS_V4_OBRIGATORIOS:
        if campo not in fm:
            add("A2", "BLOQUEANTE", f"campo '{campo}' ausente no frontmatter")

    # A3 — verificado_em ≤ 90 dias
    verificado_em = fm.get("verificado_em")
    if verificado_em:
        try:
            if isinstance(verificado_em, str):
                vd = datetime.strptime(str(verificado_em), "%Y-%m-%d").date()
            else:
                vd = verificado_em  # já é date
            if (date.today() - vd).days > 90:
                add("A3", "AMARELO", f"verificado_em={vd} há {(date.today()-vd).days} dias (limite: 90)")
        except ValueError:
            add("A3", "AMARELO", f"verificado_em formato inválido: {verificado_em}")

    # A4 — §0 gate
    if "## §0" not in body and "§0" not in body:
        add("A4", "BLOQUEANTE", "§0 gate ausente")

    # A5 — §1 FAÇO/NÃO FAÇO
    if "FAÇO" not in body or "NÃO FAÇO" not in body:
        add("A5", "BLOQUEANTE", "§1 FAÇO/NÃO FAÇO ausente ou incompleto")

    # A6 — §2 pipeline
    if "## §2" not in body and "§2" not in body:
        add("A6", "AMARELO", "§2 pipeline ausente")

    # A7 — §3 output
    if "## §3" not in body and "§3" not in body:
        add("A7", "BLOQUEANTE", "§3 output canônico ausente")

    # A8 — §4 calibração
    if "## §4" not in body and "§4" not in body:
        add("A8", "AMARELO", "§4 calibração ausente")

    # A9 — §5 auto-verificação
    if "## §5" not in body and "§5" not in body:
        add("A9", "AMARELO", "§5 auto-verificação ausente")

    # A10 — version semântico
    version = fm.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+$", str(version)):
        add("A10", "AMARELO", f"version '{version}' não segue formato X.Y.Z")

    # A11 — depends_on só skills (não arquivos)
    depends_on = fm.get("depends_on") or []
    if isinstance(depends_on, list):
        for dep in depends_on:
            dep_str = str(dep)
            if "/" in dep_str or "\\" in dep_str or dep_str.endswith(".json") or dep_str.endswith(".md"):
                add("A11", "BLOQUEANTE", f"depends_on contém caminho de arquivo: '{dep_str}'")

    # A12 — categoria e justificativa
    if not fm.get("categoria"):
        add("A12", "BLOQUEANTE", "campo 'categoria' ausente ou vazio")
    if not fm.get("justificativa"):
        add("A12", "BLOQUEANTE", "campo 'justificativa' ausente ou vazio")

    # A13 — git_repo
    if not fm.get("git_repo"):
        add("A13", "AMARELO", "git_repo não declarado")

    # A14 — licoes_aplicadas
    licoes = fm.get("licoes_aplicadas") or []
    if not licoes:
        add("A14", "AMARELO", "licoes_aplicadas vazio ou ausente")

    # A15 — regras_aplicaveis
    regras = fm.get("regras_aplicaveis") or []
    if not regras:
        add("A15", "AMARELO", "regras_aplicaveis vazio ou ausente")

    # A16 — git_auto_commit declarado
    if "git_auto_commit" not in fm:
        add("A16", "BLOQUEANTE", "git_auto_commit não declarado")

    # A17 — git_auto_commit: false por padrão
    git_ac = fm.get("git_auto_commit")
    if git_ac is True:
        # Verifica se §4-G pipeline está documentado
        if "§4-G" not in body and "git_auto_commit" not in body.lower():
            add("A17", "BLOQUEANTE", "git_auto_commit: true sem pipeline §4-G documentado")
        else:
            add("A17", "AMARELO", "git_auto_commit: true — verificar se §4-G pipeline está completo")

    # A18 — chains_to → skills instaladas
    chains_to = fm.get("chains_to") or []
    if isinstance(chains_to, list):
        for ct in chains_to:
            ct_str = str(ct).split("#")[0].strip()  # remove comentários inline
            if ct_str and ct_str not in installed and ct_str != name:
                add("A18", "BLOQUEANTE", f"chains_to aponta para skill não instalada: '{ct_str}'")

    # A19 — informacoes/ não em depends_on
    if isinstance(depends_on, list):
        for dep in depends_on:
            dep_str = str(dep)
            if "informacoes/" in dep_str or "informacoes\\" in dep_str:
                add("A19", "BLOQUEANTE", f"depends_on contém arquivo de informacoes/: '{dep_str}'")

    # A20 — sem contexto implícito de sessão
    body_lower = body.lower()
    for frase in FRASES_CONTEXTO_IMPLICITO:
        if frase.lower() in body_lower:
            add("A20", "BLOQUEANTE", f"contexto implícito de sessão detectado: '{frase[:50]}...'")
            break

    # A21 — chain depth ≤ 3 (análise transitiva simplificada)
    # Apenas alerta se chains_to não for vazio (verificação profunda requer grafo completo)
    if isinstance(chains_to, list) and len(chains_to) >= 3:
        add("A21", "AMARELO", f"chains_to com {len(chains_to)} destinos — verificar profundidade transitiva")

    return issues


def classificar(issues):
    """VERDE / AMARELO / VERMELHO."""
    codigos = {c for c, n, _ in issues}
    niveis = {n for _, n, _ in issues}
    if "BLOQUEANTE" in niveis:
        return "VERMELHO"
    if "AMARELO" in niveis:
        return "AMARELO"
    return "VERDE"


def gerar_relatorio(results: dict, skills_dir: Path, modo: str) -> str:
    hoje = date.today().isoformat()
    total = len(results)
    verdes   = sum(1 for r in results.values() if r["status"] == "VERDE")
    amarelas = sum(1 for r in results.values() if r["status"] == "AMARELO")
    vermelhas = sum(1 for r in results.values() if r["status"] == "VERMELHO")

    linhas = [
        f"AUDITORIA R9 — {hoje}  |  modo: {modo}",
        f"biblioteca: {skills_dir}",
        f"total: {total}  |  verdes: {verdes}  |  amarelas: {amarelas}  |  vermelhas: {vermelhas}",
        "",
    ]

    if vermelhas:
        linhas.append("── VERMELHAS (ação requerida) " + "─" * 40)
        for name, r in sorted(results.items()):
            if r["status"] == "VERMELHO":
                bloqueantes = [(c, d) for c, n, d in r["issues"] if n == "BLOQUEANTE"]
                for code, desc in bloqueantes:
                    linhas.append(f"  {name}: [{code}] {desc}")
        linhas.append("")

    if amarelas:
        linhas.append("── AMARELAS (advertência) " + "─" * 44)
        for name, r in sorted(results.items()):
            if r["status"] == "AMARELO":
                advertencias = [(c, d) for c, n, d in r["issues"] if n == "AMARELO"]
                for code, desc in advertencias:
                    linhas.append(f"  {name}: [{code}] {desc}")
        linhas.append("")

    if verdes:
        linhas.append("── VERDES " + "─" * 60)
        for name in sorted(r for r, v in results.items() if v["status"] == "VERDE"):
            linhas.append(f"  {name}")
        linhas.append("")

    if vermelhas > 0:
        linhas.append("SUMÁRIO: biblioteca COM BLOQUEANTES — corrigir antes de produção")
    elif amarelas > 0:
        linhas.append("SUMÁRIO: biblioteca COM ADVERTÊNCIAS — instalar com cautela")
    else:
        linhas.append("SUMÁRIO: biblioteca APROVADA — todas as skills conformes A1-A21")

    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(description="Auditoria R9 da biblioteca de skills Almeida Marques")
    parser.add_argument("--skills-dir", default="C:/RaquelSkills/skills",
                        help="Caminho para o diretório de skills")
    parser.add_argument("--modo", choices=["completo", "rapido"], default="completo",
                        help="completo=A1-A21 | rapido=apenas bloqueantes")
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        # Tentar caminho Linux equivalente
        linux_equiv = Path("/sessions/trusting-practical-bell/mnt/RaquelSkills/skills")
        if linux_equiv.exists():
            skills_dir = linux_equiv
        else:
            print(f"ERRO: diretório não encontrado: {skills_dir}", file=sys.stderr)
            sys.exit(1)

    installed = get_installed_skills(skills_dir)
    results = {}

    for skill_name in sorted(installed):
        skill_dir = skills_dir / skill_name
        issues = audit_skill(skill_name, skill_dir, installed, args.modo)

        if args.modo == "rapido":
            issues = [(c, n, d) for c, n, d in issues if c in BLOQUEANTES]

        results[skill_name] = {
            "status": classificar(issues),
            "issues": issues,
        }

    relatorio = gerar_relatorio(results, skills_dir, args.modo)
    print(relatorio)

    # Salvar arquivo
    out_file = Path(f"audit_{date.today().isoformat()}.txt")
    out_file.write_text(relatorio, encoding="utf-8")
    print(f"\nArquivo salvo: {out_file.resolve()}", file=sys.stderr)


if __name__ == "__main__":
    main()
