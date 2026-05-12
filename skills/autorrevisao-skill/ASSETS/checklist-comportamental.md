# Checklist comportamental B1–B7 — autorrevisao-skill

## B1 — Coerência description ↔ §1

Perguntas:
- A primeira frase da description começa com verbo imperativo?
- Os gatilhos listados na description estão refletidos no §2 da skill?
- O §1 FAÇO entrega exatamente o que a description promete — nem mais, nem menos?
- O §1 NÃO FAÇO exclui comportamentos que a description não cobre?

Falha se: description promete X mas §1 entrega X + Y sem justificativa.

## B2 — Exclusividade de gatilhos

Contextos de teste (aplicar a cada gatilho declarado):
- Contexto A: BPC/LOAS (renda, família, CadÚnico)
- Contexto B: benefício previdenciário (B31, B87, B91, incapacidade)
- Contexto C: ação trabalhista (acidentária, doença ocupacional)
- Contexto D: ação cível ou família (alimentos, divórcio)
- Contexto E: processo administrativo não-previdenciário

Critério: gatilho que dispara em ≥ 3 contextos sem discriminador = falha B2.
Resolução: adicionar objeto específico ao gatilho (ex.: "laudo pericial acidentário" em vez de "laudo pericial").

## B3 — Gate de §0

Perguntas:
- §0 lista todos os inputs necessários?
- Se a skill for invocada sem esses inputs, ela para e pede, ou continua e inventa?
- O gate é explícito (lista de campos) ou implícito (assume contexto anterior)?

Falha se: gate implícito — a skill pressupõe que Raquel já forneceu dados em turno anterior.

## B4 — Output verificável

Perguntas:
- O tipo de output está declarado (JSON, DOCX, relatório MD, bloco de texto)?
- Existe MODELO/ ou SCHEMA/ que define a estrutura completa do output?
- O output pode ser produzido pelo modelo sem acesso a sistemas externos?

Falha se: output requer dado que só existe em sistema externo (ex.: número de processo em tempo real) sem instrução explícita de como obtê-lo.

## B5 — Dependências ocultas

Perguntas:
- A skill usa frases como "com base no que foi feito antes", "usando o contexto anterior"?
- A skill pressupõe que outro arquivo existe em caminho específico sem verificar?
- A skill depende de outra skill estar ativa na mesma sessão?

Falha se: qualquer resposta for "sim" — viola A20 (isolamento de sessão).

## B6 — Contratos de interface

Perguntas:
- Cada entrada em chains_to existe em C:\RaquelSkills\skills\?
- Cada skill em chains_to tem SCHEMAS/ com schema de input?
- depends_on aponta apenas para skills, não para arquivos de schema ou reference files?

Falha se: chains_to aponta para skill inexistente (bloqueio A18) ou para ferramenta externa sem anotação.

## B7 — Teste de sanidade reverso

Procedimento:
1. Descrever o problema que a skill resolve em uma frase simples
2. Fazer a mesma pergunta ao modelo SEM carregar a skill
3. Comparar os outputs

Interpretação:
- Output com skill significativamente melhor: skill justificada
- Output sem skill equivalente: skill pode ser redundante (alerta amarelo — não bloqueio)
- Output sem skill melhor: skill está distorcendo o comportamento (bloqueio vermelho)
