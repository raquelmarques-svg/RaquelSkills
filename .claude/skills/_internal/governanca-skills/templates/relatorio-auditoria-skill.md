# Relatorio de auditoria leve — {skill_id}

**Data:** {checked_at}
**Skill auditada:** {skill_id}
**Nivel da auditoria:** leve (apenas presenca estrutural)

## Escopo da auditoria

Esta auditoria confere apenas presenca de campos minimos. Nao avalia
qualidade do verbo dominante, adequacao de output, coerencia com
`_manifest`, duplicidade entre skills ou correcao juridica. Para esses
pontos, encaminhar a `healthcheck-biblioteca`.

## Campos obrigatorios no SKILL.md

| Campo | Presente |
|-------|----------|
| frontmatter.name | { } |
| frontmatter.description | { } |
| frontmatter.version | { } |
| frontmatter.layer | { } |
| frontmatter.activation | { } |
| Finalidade | { } |
| Transformacao | { } |
| Gatilhos | { } |
| Bloqueios | { } |
| Entrada minima | { } |
| Procedimento operacional obrigatorio | { } |
| Outputs | { } |
| Limites | { } |

## Pastas obrigatorias

| Pasta | Existe | Vazia |
|-------|--------|-------|
| assets | { } | { } |
| templates | { } | { } |
| schemas | { } | { } |
| scripts | { } | { } |
| references | { } | { } |
| examples | { } | { } |
| config | { } | { } |

## Tamanho do SKILL.md

Linhas: {linhas}
Limite minimo: 30
Limite maximo: 500

## Alertas

- {alerta_1}
- {alerta_2}

## Output do procedimento

```text
Status: AUDITORIA_OK | AUDITORIA_COM_ALERTAS | AUDITORIA_REPROVADA
Output produzido: relatorio-auditoria-skill.md
Lacunas: {lacunas}
Proxima acao: {proxima_acao}
Proxima skill permitida: healthcheck-biblioteca para profundidade
Bloqueios: governanca-skills nao avalia substancia.
```
