---
name: governanca-skills
description: |
  Executa auditoria R9 completa da biblioteca de skills Almeida Marques, verificando conformidade A1-A21 para cada skill instalada. Produz relatório consolidado com status VERDE/AMARELO/VERMELHO por skill e sumário executivo. INVOQUE quando: "audite a biblioteca", "rodar R9", "checar todas as skills", "governanca", "relatório de conformidade", "quantas skills passam em A1-A21", "audit mensal", "governanca-skills". NÃO use para: criar skill nova (→ skill-creator-am), revisar skill específica recém-criada (→ autorrevisao-skill), registrar lição aprendida (→ gotcha-skill), corrigir violações encontradas (→ skill-creator-am modo Edit).
project: Proj02
nucleo: N5
frente: transversal
camada: C6
categoria: governance
justificativa: Única skill que auditoria toda a biblioteca — sem ela, degradação silenciosa das constraints é inevitável
version: 1.1.0
verificado_em: 2026-05-18
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to: []
licoes_aplicadas:
  - L2, L3, L4, L5, L12, L19, L20, L21, L22, L23, L24, L25, L26, L27
regras_aplicaveis:
  - R6, R9, R10, R11
---

# governanca-skills — Auditoria R9 da biblioteca

## §0 — Ativação e gate

Esta skill precisa de:
1. **Caminho da biblioteca** (padrão: `C:\RaquelSkills\skills\`)
2. **Escopo** (todas as skills ou lista específica)
3. **Modo** (`completo` = A1-A23 | `rápido` = apenas bloqueantes A1/A2/A11/A17/A19)

Se o caminho não for confirmado, uso o padrão. Se o modo não for informado, uso `completo`.

## §1 — Escopo

FAÇO:
- Descobrir todas as skills instaladas (subdiretórios com SKILL.md)
- Para cada skill: executar checklist A1-A23 e classificar VERDE/AMARELO/VERMELHO
- Produzir relatório consolidado com contagem e lista de ações requeridas
- Identificar skills com bloqueantes (VERMELHO) e advertências (AMARELO)
- Gerar sumário executivo: N skills, X verdes, Y amarelas, Z vermelhas

NÃO FAÇO:
- Corrigir as violações encontradas (delego para skill-creator-am modo Edit)
- Revisar skill individual recém-criada (delego para autorrevisao-skill)
- Registrar lições derivadas da auditoria (delego para gotcha-skill)
- Commitar as correções no git (informa comandos, não executa)

## §2 — Pipeline de auditoria

```
P1. DESCOBERTA
    — Listar subdiretórios de skills/ com SKILL.md presente
    — Registrar skills sem SKILL.md como VERMELHO imediato

P2. PARSE
    — Para cada skill: ler frontmatter YAML + contar linhas
    — Extrair: depends_on, chains_to, git_auto_commit, verificado_em,
               campos V4 (project, nucleo, frente, camada, categoria, justificativa)

P3. CHECKLIST A1-A23
    — A1:  linhas ≤ 500                              [bloqueante se > 500]
    — A2:  frontmatter V4 completo                    [bloqueante se campo ausente]
    — A3:  verificado_em ≤ 90 dias                    [amarelo se vencido]
    — A4:  §0 gate presente                           [bloqueante se ausente]
    — A5:  §1 FAÇO/NÃO FAÇO presente                  [bloqueante se ausente]
    — A6:  §2 pipeline presente                       [amarelo se ausente]
    — A7:  §3 output canônico presente                [bloqueante se ausente]
    — A8:  §4 calibração presente                     [amarelo se ausente]
    — A9:  §5 auto-verificação presente               [amarelo se ausente]
    — A10: version semântico (X.Y.Z)                  [amarelo se formato incorreto]
    — A11: depends_on só aponta para skills/           [bloqueante se arquivo externo]
    — A12: categoria e justificativa presentes        [bloqueante se ausentes]
    — A13: git_repo declarado                         [amarelo se ausente]
    — A14: licoes_aplicadas não vazio                 [amarelo se ausente]
    — A15: regras_aplicaveis não vazio                [amarelo se ausente]
    — A16: git_auto_commit declarado                  [bloqueante se ausente]
    — A17: git_auto_commit: false por padrão          [bloqueante se true sem §4-G]
    — A18: chains_to → skills instaladas              [bloqueante se skill inexistente]
    — A19: informacoes/ não em depends_on             [bloqueante se presente]
    — A20: sem frases de contexto implícito           [bloqueante se detectado]
    — A21: chain depth ≤ 3 transitivo                 [amarelo se > 3]
    — A22: MODELOS/ com ≥ 70% conteúdo real (amostragem) [amarelo se placeholder > 30%]
    — A23: ASSETS/ autossuficientes                   [amarelo se arquivo só com cabeçalhos ou vazio]

P4. CONSOLIDAÇÃO
    — VERDE:    sem bloqueantes nem advertências
    — AMARELO:  ≥ 1 advertência, sem bloqueantes
    — VERMELHO: ≥ 1 bloqueante
```

## §3 — Output canônico

Relatório em formato MODELOS/relatorio-audit-mensal.md:

```
AUDITORIA R9 — [data]
biblioteca: [caminho]
total_skills: N  |  verdes: X  |  amarelas: Y  |  vermelhas: Z

VERMELHAS (ação requerida):
  [nome]: A[X], A[Y] — [descrição breve]

AMARELAS (advertência):
  [nome]: A[X] — [descrição breve]

VERDES: [lista]

SUMÁRIO: biblioteca [APROVADA|COM ADVERTÊNCIAS|COM BLOQUEANTES]
```

## §4 — Calibração

DADO NECESSÁRIO: caminho da biblioteca
SCRIPT AUXILIAR: `scripts/rodar_audit_r9.py` — executa A1-A23 via Python

Para rodar o script diretamente (bash):
```bash
python3 scripts/rodar_audit_r9.py --skills-dir C:/RaquelSkills/skills
```

**Nota sobre A22:** amostragem = ler os primeiros 30 tokens de cada arquivo em MODELOS/ e verificar proporção de placeholders `[colchetes]` vs. conteúdo real. Se > 30% do arquivo for placeholder, classificar AMARELO.

**Nota sobre A23:** verificar se cada arquivo em ASSETS/ tem ao menos um parágrafo de conteúdo real (não apenas cabeçalho `##` seguido de linha vazia). Arquivo com apenas cabeçalhos = AMARELO.

## §5 — Auto-verificação

Verificação: 2026-05-18 · Próxima: 2026-08-18

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] §0 com gate explícito
- [x] §1 FAÇO/NÃO FAÇO
- [x] Output canônico
- [x] A22 e A23 adicionados ao checklist (L27)
- [x] Tamanho dentro do limite
