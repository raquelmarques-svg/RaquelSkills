# Modelo — Relatório de auditoria mensal R9

## Cabeçalho

```
AUDITORIA R9 — YYYY-MM-DD  |  modo: completo
biblioteca: C:\RaquelSkills\skills
total: N  |  verdes: X  |  amarelas: Y  |  vermelhas: Z
```

## Seção VERMELHAS

```
── VERMELHAS (ação requerida) ────────────────────────────────────────
  [nome-skill]: [A-código] [descrição do problema]
  [nome-skill]: [A-código] [descrição do problema]
```

## Seção AMARELAS

```
── AMARELAS (advertência) ────────────────────────────────────────────
  [nome-skill]: [A-código] [descrição]
```

## Seção VERDES

```
── VERDES ────────────────────────────────────────────────────────────
  [lista de nomes]
```

## Sumário

```
SUMÁRIO: biblioteca [APROVADA | COM ADVERTÊNCIAS | COM BLOQUEANTES]
```

---

## Critérios de classificação

| Status    | Condição                                       |
|-----------|------------------------------------------------|
| VERDE     | zero bloqueantes, zero advertências            |
| AMARELO   | ≥ 1 advertência, zero bloqueantes             |
| VERMELHO  | ≥ 1 bloqueante                                 |

## Auditorias e nível de severidade

| Código | Severidade  | Verificação                                    |
|--------|-------------|------------------------------------------------|
| A1     | bloqueante  | Tamanho ≤ 500 linhas                           |
| A2     | bloqueante  | Frontmatter V4 completo                        |
| A3     | amarelo     | verificado_em ≤ 90 dias                        |
| A4     | bloqueante  | §0 gate presente                               |
| A5     | bloqueante  | §1 FAÇO/NÃO FAÇO presente                     |
| A6     | amarelo     | §2 pipeline presente                           |
| A7     | bloqueante  | §3 output canônico presente                    |
| A8     | amarelo     | §4 calibração presente                         |
| A9     | amarelo     | §5 auto-verificação presente                   |
| A10    | amarelo     | version X.Y.Z                                  |
| A11    | bloqueante  | depends_on só skills (não arquivos)            |
| A12    | bloqueante  | categoria e justificativa presentes            |
| A13    | amarelo     | git_repo declarado                             |
| A14    | amarelo     | licoes_aplicadas não vazio                     |
| A15    | amarelo     | regras_aplicaveis não vazio                    |
| A16    | bloqueante  | git_auto_commit declarado                      |
| A17    | bloqueante  | git_auto_commit: false por padrão              |
| A18    | bloqueante  | chains_to → skills instaladas                  |
| A19    | bloqueante  | informacoes/ não em depends_on                 |
| A20    | bloqueante  | sem contexto implícito de sessão               |
| A21    | amarelo     | chain depth ≤ 3 transitivo                     |
