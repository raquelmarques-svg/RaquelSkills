# Exemplo de plano de divisao — peticao-tudo

**Data:** 2026-04-25
**Skill alvo:** peticao-tudo (hipotetica, exemplo de skill inchada)
**Modo:** divisao

## Sintomas detectados

```text
[X] SKILL.md acima de 500 linhas (820 linhas);
[X] mais de cinco modos internos (8 modos);
[X] mais de um Procedimento operacional obrigatorio (4 secoes);
[X] outputs primarios de tipos distintos (.md, .docx, .pdf, JSON);
[X] gatilhos cobrindo familias semanticas distintas;
[X] bloqueios internos invasivos ("modo redacao nao deve invadir modo
    formatacao", "modo protocolo nao deve invadir modo revisao").
```

## Verbos dominantes detectados

| # | Verbo | Procedimento proprio? | Output proprio? | Bloqueios proprios? |
|---|-------|-----------------------|-----------------|---------------------|
| 1 | redigir | sim | rascunho-peca.md | sim |
| 2 | revisar | sim | relatorio-critica.md | sim |
| 3 | formatar | sim | peca-final.docx | sim |
| 4 | protocolar | sim | plano-protocolo.md | sim |

Quatro verbos dominantes, quatro outputs distintos. Skill viola o
principio de um verbo dominante por skill.

## Skills resultantes propostas

### Skill A: peticao-processual
- Verbo dominante: redigir
- Output primario: rascunho-peca.md
- Status enum: EXECUTADO, EXECUTADO_COM_LACUNAS, BLOQUEADO, REDIRECIONADO
- Aliases sugeridos: "escreva a peca", "redija a inicial", "minute"

### Skill B: revisao-juridica
- Verbo dominante: criticar
- Output primario: relatorio-critica.md
- Status enum: EXECUTADO, BLOQUEADO, REDIRECIONADO
- Aliases sugeridos: "critique a peca", "revise juridicamente"

### Skill C: mod4
- Verbo dominante: formatar
- Output primario: peca-final.docx
- Status enum: VALIDADO, ENTRADA_INSUFICIENTE, ERRO_TEMPLATE, ERRO_XML, ERRO_VALIDACAO
- Aliases sugeridos: "mod4" (literal e exclusivo)

### Skill D: peticionamento-eletronico
- Verbo dominante: protocolar
- Output primario: plano-protocolo.md
- Status enum: PROTOCOLO_APTO, PROTOCOLO_NAO_APTO, REDIRECIONADO
- Aliases sugeridos: "qual classe e assunto", "preparar protocolo"

## Recursos a redistribuir

| Recurso atual | Tipo | Destino sugerido |
|---------------|------|------------------|
| assets/padrao-redacional.md | asset transversal | _shared/assets/ |
| assets/criterios-revisao.md | asset especifico | revisao-juridica/assets/ |
| templates/peca-cambria.docx | template de formato | mod4/assets/template_mod4.docx |
| templates/checklist-pre-protocolo.md | template | revisao-preprotocolo/templates/ |
| scripts/gerar_docx.py | script de formato | mod4/scripts/ |
| scripts/validar_anexos.py | script de protocolo | peticionamento-eletronico/scripts/ |
| config/cores-escritorio.yaml | config visual | _shared/config/identidade-visual.yaml |
| references/manual-redacao.md | reference longa | _shared/references/ |

## Alteracoes necessarias no _manifest

```text
aliases.yaml         => remover "peticao-tudo"; adicionar aliases das 4 novas
precedencia.yaml     => criar regras de precedencia entre as 4 (mod4 sempre por
                        comando explicito; revisao-preprotocolo antes de mod4)
bloqueios.yaml       => declarar bloqueios reciprocos entre as 4
chamadas-permitidas.yaml => grafo: redigir -> revisar -> preprotocolo ->
                            protocolar -> mod4
```

Encaminhamento: manifest-manager.

## Migracao de conteudo

Conteudo redistribuido entre as quatro skills resultantes deve passar
por migration-manager para registro em `_migration/mapa-origem-destino.yaml`.
Inventario obrigatorio em `_migration/inventario-conteudos.md`.
Duplicidades em `_migration/duplicidades-controladas.md`.

## Nota sobre re-uso

A divisao revela que tres das quatro skills resultantes (peticao-processual,
revisao-juridica, mod4) ja existem na lista nuclear da V6.5.2. A skill
inchada `peticao-tudo` e um anti-padrao reproduzindo, em um arquivo so, o
que a arquitetura V6.5.2 distribui em quatro skills com fronteiras
claras. Apos a divisao, a skill original deve deixar de existir; nao
deve ser preservada como skill "guarda-chuva".

## Output do procedimento

```text
Status: DIVISAO_RECOMENDADA
Output produzido: plano-divisao-skill.md (este arquivo)
Lacunas: nenhuma.
Proxima acao: gerar SkillCreationSpec para cada uma das 4 skills resultantes,
              salvo as ja existentes na biblioteca nuclear.
Proxima skill permitida: governanca-skills modo `criacao`,
                         migration-manager,
                         manifest-manager.
Bloqueios: governanca-skills nao executa a divisao. Execucao depende de
           skill-creator-bridge sob autorizacao de file-safety.
```
