---
name: autorrevisao-skill
description: |
  Revisa comportamento e ativação de skill recém-criada, produzindo relatório de conformidade pragmática. Verifica se a skill ativa quando deve, não ativa quando não deve, e se o output declarado corresponde ao output efetivo. Complementa as auditorias estruturais A1-A21 (que verificam forma) com verificação comportamental (que verifica função real). INVOQUE quando: "revise a skill criada", "confira antes de instalar", "a skill vai funcionar?", "teste os gatilhos", "autorrevisao". NÃO use para: auditar a biblioteca inteira (→ governanca-skills), criar skill nova (→ skill-creator-am), corrigir frontmatter (→ edição manual ou skill-creator-am Edit).
project: Proj02
nucleo: N5
frente: transversal
camada: C6
categoria: capability
justificativa: Produz relatório acionável de conformidade comportamental — output concreto que libera ou bloqueia a instalação da skill revisada
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to: []
licoes_aplicadas:
  - L2, L3, L4, L5, L12, L20
regras_aplicaveis:
  - R6, R10, R11
---

# autorrevisao-skill — Revisão comportamental pós-criação

## §0 — Ativação e gate

Esta skill recebe como input o SKILL.md de uma skill recém-criada. Sem o arquivo, não procede.

Antes de revisar, pergunto:
1. Qual skill está sendo revisada? (nome + caminho)
2. Há casos de uso reais que posso usar como sonda de ativação?

## §1 — Escopo

FAÇO:
- Verificar se os gatilhos linguísticos ativam no contexto certo (V8-D1)
- Verificar se o §1 FAÇO/NÃO FAÇO corresponde ao que a description promete
- Verificar se o §0 gate impede ativação sem input suficiente
- Verificar se o output declarado é produzível pelo modelo sem dependências ocultas
- Verificar se chains_to aponta para skills instaladas com schema (A18)
- Produzir relatório APROVADA / APROVADA COM ADVERTÊNCIAS / BLOQUEADA

NÃO FAÇO:
- Corrigir o SKILL.md (delego para skill-creator-am modo Edit)
- Auditar a biblioteca inteira (delego para governanca-skills)
- Executar a skill revisada (delego para a própria skill)
- Registrar lições aprendidas da revisão (delego para gotcha-skill)

## §2 — Pipeline de revisão (7 verificações comportamentais)

```
B1. Coerência description ↔ §1
    — description promete o que §1 FAÇO entrega?
    — §1 NÃO FAÇO exclui o que description não promete?

B2. Exclusividade de gatilhos
    — Testar cada gatilho em 5 contextos distintos do escritório
    — Gatilho que dispara em ≥ 3 contextos sem discriminador: falha

B3. Gate de §0
    — §0 lista todos os inputs que a skill precisa?
    — Se skill for invocada sem esses inputs, ela para ou inventa?

B4. Output verificável
    — O output declarado (JSON, DOCX, relatório, bloco PRONTO) é produzível?
    — Existe MODELO/ ou SCHEMA/ que define a estrutura?

B5. Dependências ocultas
    — Skill pressupõe contexto de outra skill ativa? (violação A20)
    — Skill pressupõe arquivo que pode não existir?

B6. Contratos de interface (A18)
    — chains_to aponta para skills instaladas com schema?
    — depends_on aponta para skills, não arquivos?

B7. Teste de sanidade reverso
    — Se eu descrever o problema que esta skill resolve em linguagem simples,
      o modelo chega ao mesmo resultado SEM a skill?
    — Se sim: skill pode ser desnecessária (alerta, não bloqueio)
```

## §3 — Output canônico

Relatório em três variantes:

**APROVADA**
```
autorrevisao: APROVADA
skill: [nome]
data: YYYY-MM-DD
B1-B7: todos verdes
observacoes: —
```

**APROVADA COM ADVERTÊNCIAS**
```
autorrevisao: APROVADA COM ADVERTÊNCIAS
skill: [nome]
data: YYYY-MM-DD
amarelos:
  - B[N]: [descrição]
recomendacao: instalar; corrigir advertências na próxima versão
```

**BLOQUEADA**
```
autorrevisao: BLOQUEADA
skill: [nome]
data: YYYY-MM-DD
bloqueantes:
  - B[N]: [descrição]
acao_requerida: corrigir antes de instalar
```

## §4 — Calibração

VERIFICAR: skill em análise existe e SKILL.md está acessível
DADO NECESSÁRIO: caminho da skill + ao menos 2 casos de uso reais para sonda B2

## §5 — Auto-verificação

Verificação: 2026-05-12 · Próxima: 2026-08-12

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] §0 com gate explícito
- [x] §1 FAÇO/NÃO FAÇO
- [x] Output canônico em três variantes
- [x] Tamanho dentro do limite
