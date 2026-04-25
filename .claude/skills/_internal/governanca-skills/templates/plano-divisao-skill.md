# Plano de divisao — {skill_id}

**Data:** {data}
**Skill alvo:** {skill_id}
**Modo:** divisao

## Sintomas detectados

```text
[ ] SKILL.md acima de 500 linhas;
[ ] mais de cinco modos internos;
[ ] mais de um Procedimento operacional obrigatorio;
[ ] outputs primarios de tipos distintos;
[ ] gatilhos cobrindo familias semanticas distintas;
[ ] bloqueios internos invasivos.
```

## Verbos dominantes detectados

| # | Verbo | Procedimento proprio? | Output proprio? | Bloqueios proprios? |
|---|-------|-----------------------|-----------------|---------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Skills resultantes propostas

### Skill A: {nome_a}
- Verbo dominante: 
- Output primario: 
- Status enum: 
- Aliases sugeridos: 

### Skill B: {nome_b}
- Verbo dominante: 
- Output primario: 
- Status enum: 
- Aliases sugeridos: 

## Recursos a redistribuir

| Recurso atual | Tipo | Destino sugerido |
|---------------|------|------------------|
| | | |

## Alteracoes necessarias no _manifest

```text
aliases.yaml         => atualizar entradas
precedencia.yaml     => criar regras de precedencia entre as novas skills
bloqueios.yaml       => declarar bloqueios reciprocos
chamadas-permitidas.yaml => atualizar grafo
```

Encaminhamento: manifest-manager.

## Migracao de conteudo

Conteudo redistribuido entre as skills resultantes deve passar por
migration-manager para registro em `_migration/mapa-origem-destino.yaml`.

## Output do procedimento

```text
Status: DIVISAO_RECOMENDADA
Output produzido: plano-divisao-skill.md
Lacunas: {lacunas}
Proxima acao: aprovar plano e gerar SkillCreationSpec para cada skill resultante
Proxima skill permitida: governanca-skills modo `criacao`,
                         migration-manager,
                         manifest-manager.
Bloqueios: governanca-skills nao executa a divisao por si.
```
