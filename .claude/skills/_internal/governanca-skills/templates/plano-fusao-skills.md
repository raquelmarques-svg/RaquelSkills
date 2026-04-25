# Plano de fusao — {skill_a_id} + {skill_b_id}

**Data:** {data}
**Skills alvo:** {skill_a_id}, {skill_b_id}
**Modo:** fusao

## Sintomas detectados

```text
[ ] verbo dominante coincidente;
[ ] output primario sobreposto;
[ ] aliases concorrentes em _manifest;
[ ] bloqueios mutuos para evitar invasao;
[ ] usuaria nao sabe qual chamar em qual situacao.
```

## Comparacao verbal

| Aspecto | {skill_a_id} | {skill_b_id} |
|---------|--------------|--------------|
| Verbo dominante | | |
| Output primario | | |
| Status enum | | |
| Permission profile | | |
| Aliases atuais | | |

## Decisao de absorcao

```text
Skill absorvedora: 
Skill absorvida:   
Justificativa:     
```

## Conteudos a migrar para a skill absorvedora

| Origem | Destino | Tipo |
|--------|---------|------|
| | | |

## Conteudos a migrar para _shared

| Origem | Destino | Tipo |
|--------|---------|------|
| | | |

## Conteudos a virar modo interno

| Origem | Modo interno na absorvedora |
|--------|------------------------------|
| | |

## Alteracoes no _manifest

```text
aliases.yaml         => remover aliases da absorvida, manter na absorvedora
precedencia.yaml     => remover entradas da absorvida
bloqueios.yaml       => atualizar bloqueios da absorvedora
chamadas-permitidas.yaml => atualizar grafo
```

## Risco de fusao indevida

A fusao e desaconselhada quando:

```text
- as skills tem permission_profile incompativel;
- as skills tem niveis de risco operacional muito distintos;
- a absorcao implicaria mais de cinco modos internos na absorvedora.
```

Nesses casos, manter as skills separadas e ajustar precedencia em vez de
fundir.

## Output do procedimento

```text
Status: FUSAO_RECOMENDADA
Output produzido: plano-fusao-skills.md
Lacunas: {lacunas}
Proxima acao: aprovar plano e executar migracao
Proxima skill permitida: migration-manager,
                         manifest-manager.
Bloqueios: governanca-skills nao executa a fusao por si.
```
