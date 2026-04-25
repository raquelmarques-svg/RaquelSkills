# Verbo dominante

Verbo dominante e a operacao central de uma skill. Toda skill deve ter
um, e apenas um. Skill com dois verbos dominantes e candidata a divisao.

## Definicao

```text
Verbo dominante = a operacao que, se removida, faz a skill perder sua
funcao. As demais operacoes sao subordinadas, instrumentais, secundarias.
```

Teste pratico:

```text
"Se eu remover X, a skill ainda faz seu trabalho?"
Se sim, X nao e o verbo dominante.
Se nao, X e o verbo dominante (ou um dos verbos dominantes, caso a skill
esteja inflada).
```

## Por que isso importa

Skills sem verbo dominante claro sofrem de:

```text
ativacao concorrente (varias skills disputando o mesmo gatilho);
inchaço (a skill cresce ate virar manual);
manutencao dificil (cada alteracao mexe em varios procedimentos);
output instavel (saida muda conforme a parte da skill que predomina);
sobreposicao com outras skills.
```

## Como detectar mais de um verbo dominante

Sinais:

```text
o SKILL.md tem mais de uma secao chamada Procedimento operacional;
os outputs primarios sao de naturezas diferentes (ex.: docx final +
relatorio + checklist);
os gatilhos disparam por palavras-chave de familias distintas;
os bloqueios mencionam invasao de escopo entre partes da propria skill;
a skill tem mais de cinco modos internos.
```

## Exemplos

```text
peticao-processual: verbo dominante = redigir.
revisao-juridica: verbo dominante = criticar.
revisao-preprotocolo: verbo dominante = validar.
mod4: verbo dominante = formatar.
peticionamento-eletronico: verbo dominante = protocolar.
levanta-fatos: verbo dominante = extrair.
honorarios: verbo dominante = calcular.
governanca-skills: verbo dominante = governar.
```

## Sinal de divisao

Quando uma skill descreve, no mesmo SKILL.md, redigir e revisar e
formatar e protocolar, ela tem quatro verbos dominantes. Recomendacao
imediata: dividir em quatro skills, com encadeamento claro no _manifest.

## Compatibilidade entre verbos

Verbos compativeis podem coexistir como skill-pai e modo interno. Verbos
incompativeis nao. Ver tabela em regra-hierarquica-casos-cinza.md.

## Nota sobre "auditar"

O verbo "auditar" e dominante para governanca-skills no modo `auditoria`
e tambem para healthcheck-biblioteca. A diferenca esta no objeto:

```text
governanca-skills audita uma skill, em nivel leve, na sua estrutura
interna minima.

healthcheck-biblioteca audita a biblioteca inteira, em nivel profundo,
com coerencia de manifest, ausencia de orfaos, conformidade da politica
de arquivos e relacao entre skills.
```

A coexistencia e admissivel porque o objeto e o nivel sao distintos.
