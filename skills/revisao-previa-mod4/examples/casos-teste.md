# Casos-teste — revisao-previa-mod4

---

## Caso positivo 1 — Réplica pronta, sem problemas bloqueantes

**Contexto:** Skill replica entregou o texto da réplica. Usuária diz "pode revisar para o mod4?"

**Comportamento esperado:**
1. D1 (lógica): cada argumento de rebate tem norma + fato + conclusão → OK
2. D2 (pedidos): todos os pedidos da inicial estão repetidos + admissão ficta (art. 341) adicionada → OK
3. D3 (honorários): campo presente, 20%, base "condenacao" → OK
4. D4 (consistência): nome do autor e NB idênticos em todos os parágrafos → OK
5. D5 (redacional): sem frase-pórtico, sem lista ornamental → advertência: 1 travessão intercalador em parágrafo 4
6. D6 (schema): todos os campos obrigatórios identificados → OK
7. Output: `Status: PRONTO PARA mod4` com advertência sobre travessão
8. Preenche JSON status-pre-mod4.v1.json
9. Aguarda confirmação antes de acionar mod4

---

## Caso positivo 2 — Petição inicial com honorários ausentes

**Contexto:** Skill redigiu petição inicial de BPC. Honorários não foram incluídos.

**Comportamento esperado:**
1. D2: todos os pedidos obrigatórios presentes, exceto honorários
2. D3: honorários ausentes → skill calcula: retroativo 18 meses × R$1.621 = R$29.178 + proveito
   futuro R$19.452 = base R$48.630; honorários sugeridos = R$9.726 (20%)
3. Problema: tolerável (skill propõe e adiciona automaticamente)
4. Output: `Status: PRONTO PARA mod4` com advertência: "honorários ausentes — adicionados
   automaticamente: 20% sobre R$48.630,00 = R$9.726,00"
5. JSON preenchido com `"honorarios": {"percentual": 20, "base_calculo": "condenacao"}`

---

## Caso positivo 3 — Manifestação ao laudo com inconsistência tolerável

**Contexto:** Usuária entrega manifestação ao laudo de perito. CID no corpo é M54.5 mas no
pedido consta M51.1.

**Comportamento esperado:**
1. D4 (consistência): detecta divergência de CID entre corpo e pedido
2. Classifica como tolerável (não impede formatação mas pode confundir o juízo)
3. Output: PRONTO COM ADVERTÊNCIA: "CID divergente — corpo: M54.5; pedido: M51.1.
   Verificar qual está correto antes de protocolar."

---

## Caso negativo 1 — Petição sem pedido principal

**Contexto:** Usuária entrega petição inicial de B91 sem pedido de concessão do benefício.

**Comportamento esperado:**
1. D2: pedido principal ausente → BLOQUEANTE
2. Output: `Status: BLOQUEADO`
3. Problema 1: [PEDIDO AUSENTE] concessão do B91 com DIB desde a DII
4. Providência: redação sugerida do pedido
5. Skill NÃO aciona mod4

---

## Caso negativo 2 — Tipo de documento não identificável

**Contexto:** Usuária cola um texto sem contexto. Não é possível identificar se é inicial,
réplica, recurso ou outro.

**Comportamento esperado:**
1. D6: campo `tipo_documento` não identificável → BLOQUEANTE
2. Skill pergunta: "Qual o tipo deste documento? (petição inicial, réplica, manifestação ao
   laudo, recurso ordinário, embargos, artigo jurídico ou outro?)"
3. Não emite bloco PRONTO nem BLOQUEADO até receber a resposta
4. Com a resposta: prossegue normalmente com o checklist do tipo identificado
