# governanca-skills

Skill interna da Biblioteca Raquel Skills V6.5.2. Porta de entrada da
biblioteca para qualquer pedido que envolva decisao arquitetural sobre
skills.

## Funcao

Decide o que vira skill, modo interno, asset, template, schema, script,
reference, example ou config. Audita skills existentes em nivel leve.
Recomenda divisao e fusao. Auto-audita-se em nivel leve.

## O que esta skill nao faz

Nao escreve arquivos da biblioteca. Nao aciona skill-creator nativo
diretamente. Nao altera `_manifest`. Nao executa migracao. Nao revisa
merito juridico. Nao redige peca. Nao gera docx.

## Estrutura

```text
governanca-skills/
├── SKILL.md                     procedimento operacional
├── README.md                    este arquivo
├── SKILL_CREATION_SPEC.yaml     spec auto-bootstrap da propria skill
├── assets/                      criterios estaticos
├── templates/                   formas de saida
├── schemas/                     contratos de dados
├── scripts/                     precisao mecanica
├── references/                  documentacao longa
├── examples/                    calibracao de qualidade
└── config/                      parametros
```

## Cinco modos mais auditar-self

```text
criacao        produz SkillCreationSpec
auditoria      auditoria leve de skill existente
classificacao  decide entre skill, modo, asset, template, schema, script,
               reference, example, config
divisao        recomenda dividir skill inchada
fusao          recomenda fundir skills sobrepostas
auditar-self   auto-auditoria leve da propria governanca-skills
```

## Posicao no fluxo de criacao de skill

Esta skill emite a SkillCreationSpec. A criacao fisica de arquivos
pertence a `_internal/skill-creator-bridge`, sob autorizacao de
`_internal/file-safety`. A alteracao de `_manifest` pertence a
`_internal/manifest-manager`. A migracao de conteudo antigo pertence a
`_internal/migration-manager`.

## Auditoria

A auditoria aqui e leve apenas. Para auditoria de integridade da
biblioteca, usar `_internal/healthcheck-biblioteca`.

## Manutencao

Alteracoes nesta skill devem passar por:

```text
1. governanca-skills modo auditar-self
2. healthcheck-biblioteca
3. version-control
```

Skill nao deve crescer alem de cinco modos mais auditar-self. Se nova
funcao surgir, considerar mover para outra skill interna ou criar
skill interna nova, conforme o documento 6.

## Proibicao expressa

Esta skill nao executa o que pertence a outras skills internas.
Sobreposicao deve ser detectada pela propria skill em modo `fusao` ou
externamente em healthcheck-biblioteca, e corrigida via manifest-manager.
