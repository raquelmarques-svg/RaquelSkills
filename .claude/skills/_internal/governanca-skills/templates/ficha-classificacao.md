# Ficha de classificacao — {conteudo_avaliado}

**Data:** {data}
**Conteudo avaliado:** {conteudo_avaliado}
**Modo:** classificacao

## Verbo dominante detectado

```text
{verbo_dominante_detectado}
```

## Skill-pai existente

| Item | Valor |
|------|-------|
| Existe skill-pai compativel? | { } |
| skill_id | {skill_pai_id} |
| Compatibilidade verbal | alta | media | baixa | nenhuma |

## Aplicacao da regra hierarquica

```text
Se existe skill-pai com verbo dominante compativel:
   o conteudo descreve suboperacao ?       Sim/Nao
   o conteudo tem output primario distinto? Sim/Nao
   o conteudo introduz risco operacional novo? Sim/Nao

Se nao existe skill-pai compativel:
   o conteudo passa nos tres testes da triade? Sim/Nao
```

## Destino recomendado

```text
[ ] skill autonoma
[ ] modo interno de {skill_pai_id}
[ ] asset
[ ] template
[ ] schema
[ ] script
[ ] reference
[ ] example
[ ] config
```

## Caminho destino sugerido

```text
{caminho_destino}
```

## Justificativa

{justificativa}

## Output do procedimento

```text
Status: VIRAR_SKILL_AUTONOMA | VIRAR_MODO_INTERNO | VIRAR_RECURSO_LOCAL |
        VIRAR_RECURSO_SHARED | REJEITADA_DUPLICIDADE
Output produzido: ficha-classificacao.md
Lacunas: {lacunas}
Proxima acao: {proxima_acao}
Proxima skill permitida: governanca-skills modo `criacao`,
                         migration-manager,
                         resource-registry,
                         conforme o destino.
Bloqueios: nenhuma escrita em .claude/skills/ por esta skill.
```
