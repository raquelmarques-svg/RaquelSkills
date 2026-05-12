# casos-teste — autorrevisao-skill

## CT-01 — Skill aprovada sem ressalvas

**Skill revisada:** gotcha-skill v1.0.0

**Sondas B2 (2 casos reais):**
- Contexto: usuária digita "aprendi que nunca devo usar git_auto_commit: true" → ativa gotcha-skill ✓
- Contexto: usuária digita "audite a biblioteca toda" → NÃO deve ativar (→ governanca-skills) ✓

**Output esperado:**
```
autorrevisao: APROVADA
skill: gotcha-skill
data: 2026-05-12
B1-B7: todos verdes
observacoes: —
```

---

## CT-02 — Skill com advertência amarela (B7)

**Skill revisada:** hipotética "resumo-processo" que apenas sumariza texto de petição.

**B7 — Teste de sanidade reverso:**
- Pergunta simples ao modelo sem a skill: "resuma este processo"
- Resultado: modelo produz resumo equivalente sem skill carregada

**Output esperado:**
```
autorrevisao: APROVADA COM ADVERTÊNCIAS
skill: resumo-processo
data: YYYY-MM-DD
amarelos:
  - B7: output sem skill equivalente ao output com skill — verificar se skill acrescenta valor diferencial
recomendacao: instalar; avaliar necessidade na próxima revisão
```

---

## CT-03 — Skill bloqueada por B5 (dependência oculta)

**Skill revisada:** hipotética "relatorio-honorarios" com §2 contendo:
"com base na análise de renda feita anteriormente, calcule os honorários"

**B5 detecta:**
- Skill pressupõe que `analise-calculo-renda-bpc` foi executada na mesma sessão
- Viola A20 (isolamento de sessão)

**Output esperado:**
```
autorrevisao: BLOQUEADA
skill: relatorio-honorarios
data: YYYY-MM-DD
bloqueantes:
  - B5: skill pressupõe contexto de sessão anterior ("análise de renda feita anteriormente") — viola A20
acao_requerida: §2 deve solicitar os dados de renda como input explícito no §0 gate
```

---

## CT-04 — Invocação sem SKILL.md fornecido

**Entrada:** "autorrevisao" (sem indicar qual skill)

**Output esperado:**
Gate ativa. Skill pergunta:
1. Qual skill está sendo revisada? (nome + caminho)
2. Quais são 2 casos de uso reais para sonda B2?

**Critério de aprovação:** skill não prossegue sem o arquivo e os casos de teste.

---

## CT-05 — Skill bloqueada por B2 (gatilho não exclusivo)

**Skill revisada:** hipotética "analise-laudo" com gatilho declarado como "laudo pericial".

**B2 — Teste em 5 contextos:**
- BPC/LOAS: "o laudo biopsicossocial veio" → dispara ✓
- Previdenciário: "o laudo do perito chegou" → dispara ✓
- Acidentária: "o laudo de nexo está pronto" → dispara ✓
- Trabalhista: "recebi o laudo ocupacional" → dispara ✓
- Cível: "o laudo técnico foi juntado" → dispara ✓

Resultado: gatilho dispara em 5/5 contextos sem discriminador → falha B2.

**Output esperado:**
```
autorrevisao: BLOQUEADA
skill: analise-laudo
data: YYYY-MM-DD
bloqueantes:
  - B2: gatilho "laudo pericial" dispara em 5/5 contextos — falta discriminador
        (ex.: "laudo pericial previdenciário B31/B87" em vez de "laudo pericial")
acao_requerida: refinar gatilhos com objeto específico antes de instalar
```
