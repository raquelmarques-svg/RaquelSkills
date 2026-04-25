# Exemplo de classificacao — destino: asset

**Data:** 2026-04-25
**Conteudo avaliado:** "Lista de criterios para decidir se um pedido de
tutela de urgencia esta bem fundamentado: existencia de prova
inequivoca, periculum in mora demonstrado, reversibilidade da medida,
ausencia de irreversibilidade pelo lado contrario, proporcionalidade
entre risco e medida."
**Modo:** classificacao

## Verbo dominante detectado

```text
nenhum verbo proprio. O conteudo descreve criterios estaticos.
```

## Skill-pai existente

| Item | Valor |
|------|-------|
| Existe skill-pai compativel? | Sim |
| skill_id | peticao-processual |
| Compatibilidade verbal | media (criterios sao orientadores da redacao) |

## Aplicacao da regra hierarquica

```text
O conteudo descreve suboperacao? Nao. Descreve criterio.
O conteudo tem output primario distinto? Nao. Nao gera output proprio.
O conteudo introduz risco operacional novo? Nao.
```

Conclusao: o conteudo e criterio, nao operacao. Nao deve virar skill nem
modo interno. Aplicar Teste 3 do asset criterios-skill-vs-recurso.md.

## Destino recomendado

```text
[ ] skill autonoma
[ ] modo interno
[X] asset
[ ] template
[ ] schema
[ ] script
[ ] reference
[ ] example
[ ] config
```

## Caminho destino sugerido

```text
opcao 1 (especifico): peticao-processual/assets/criterios-tutela-urgencia.md
opcao 2 (transversal): _shared/assets/criterios-tutela-urgencia.md

decisao: opcao 1, porque o criterio e usado primariamente em peca de
peticao-processual. Mover para _shared/ apenas se for reutilizado por
ms, acp ou alimentos.
```

## Justificativa

O conteudo nao executa operacao propria. Ele orienta criterio.
Criterio pertence a `assets/` da skill que o aplica. A regra hierarquica
identificou skill-pai compativel (peticao-processual). A localizacao em
skill especifica e preferivel a `_shared/` ate haver multiplos usuarios
do criterio na biblioteca, evitando promover prematuramente para
recurso compartilhado.

## Output do procedimento

```text
Status: VIRAR_RECURSO_LOCAL
Output produzido: ficha-classificacao.md
Lacunas: nenhuma.
Proxima acao: registrar em peticao-processual/assets/criterios-tutela-urgencia.md
              via resource-registry e file-safety.
Proxima skill permitida: resource-registry, file-safety.
Bloqueios: governanca-skills nao escreve em .claude/skills/ por si.
```
