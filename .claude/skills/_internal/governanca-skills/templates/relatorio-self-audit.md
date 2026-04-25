# Relatorio de auto-auditoria — governanca-skills

**Data:** {data}
**Modo:** auditar-self
**Nivel:** leve (presenca estrutural apenas)

## Fronteira de competencia

```text
auditar-self            confere a propria estrutura minima;
healthcheck-biblioteca  confere integridade da biblioteca inteira.
```

Esta auto-auditoria nao substitui healthcheck-biblioteca. Para checagem
de coerencia com `_manifest`, ausencia de orfaos, fluxo de chamadas e
politica de arquivos da biblioteca, encaminhar a healthcheck-biblioteca.

## Estrutura propria

| Item | Presente |
|------|----------|
| SKILL.md | { } |
| README.md | { } |
| SKILL_CREATION_SPEC.yaml | { } |
| assets/ | { } |
| templates/ | { } |
| schemas/ | { } |
| scripts/ | { } |
| references/ | { } |
| examples/ | { } |
| config/ | { } |

## Modos declarados em SKILL.md

| Modo | Declarado | Procedimento citado | Template citado |
|------|-----------|---------------------|------------------|
| criacao | { } | { } | { } |
| auditoria | { } | { } | { } |
| classificacao | { } | { } | { } |
| divisao | { } | { } | { } |
| fusao | { } | { } | { } |
| auditar-self | { } | { } | { } |

## Recursos citados em SKILL.md presentes em disco

| Recurso citado | Existe |
|----------------|--------|
| | { } |

## Limites declarados

```text
[ ] nao escreve arquivos da biblioteca;
[ ] nao aciona skill-creator nativo diretamente;
[ ] nao altera _manifest;
[ ] nao executa migracao;
[ ] nao revisa merito;
[ ] nao redige peca;
[ ] nao gera docx;
[ ] nao realiza auditoria substantiva ou profunda.
```

## Output do procedimento

```text
Status: SELF_AUDIT_OK | SELF_AUDIT_COM_ALERTAS
Output produzido: relatorio-self-audit.md
Lacunas: {lacunas}
Proxima acao: encaminhar a healthcheck-biblioteca para auditoria de
              integridade da biblioteca.
Proxima skill permitida: healthcheck-biblioteca.
Bloqueios: auditar-self nao examina coerencia com _manifest.
```
