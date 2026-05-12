# Modelo de entrada — lição aprendida (formato L[N])

## Estrutura canônica

```markdown
## L[N] — [título imperativo: o que NÃO fazer ou o que SEMPRE fazer]

| Campo           | Valor                                      |
|-----------------|--------------------------------------------|
| skill_afetada   | [nome exato ou "geral"]                    |
| categoria       | [frontmatter|gate|output|dependência|gatilho|cadeia|isolamento|outro] |
| descoberto_via  | [auditoria R9 | autorrevisao-skill | produção | observação direta] |
| data            | YYYY-MM-DD                                 |
| auditoria_ref   | [A[X] se aplicável, ou —]                  |

**Comportamento inesperado:**
[Uma frase: o que aconteceu.]

**Causa raiz:**
[Uma frase: por que aconteceu.]

**Correção aplicada:**
[Uma frase: o que foi mudado para corrigir.]

**Regra derivada:**
[Instrução direta ao modelo: "Sempre...", "Nunca...", "Verificar... antes de..."]

**Remissões:** [A[X], R[Y], L[M] se aplicável, ou —]
```

## Exemplos de títulos bem formados

- L19 — Nunca definir git_auto_commit: true sem pipeline §4-G verificado
- L20 — Verificar existência da skill destino antes de declarar chains_to
- L21 — Nunca incluir arquivo de informacoes/ em depends_on como se fosse skill

## Critérios de qualidade

1. Título começa com verbo modal (Nunca, Sempre, Verificar, Garantir)
2. Causa raiz é uma frase simples, não uma lista
3. Regra derivada é instrução direta ao modelo (segunda pessoa implícita)
4. Remissões só citam entidades que existem (A[X] de auditorias, R[Y] de regras, L[M] de lições)
