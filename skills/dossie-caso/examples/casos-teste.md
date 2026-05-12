# Casos-teste — dossie-caso

---

## Caso positivo 1 — Dossie acidentario completo (Maria, hernia discal)

**Contexto:** Usuaria fornece relato verbal de cliente com acao acidentaria em fase pos-laudo.

**Comportamento esperado:**
1. Skill pergunta nome, CPF e numero do processo
2. Preenche qualificacao completa incluindo telefone, email e ponto de referencia
3. Registra fatos nas 5 dimensoes: natural (origem nordestina, 2 filhos), humano (14 anos em
   linha de montagem metalurgica), clinico (CID M51.1 + M54.5, RM confirmando hernia), previdenciario
   (NB B31 concedido em vez de B91, DCB em 2024-06), juridico (laudo Tipo B desfavoravel recebido,
   prazo 15 dias)
4. Questao de fato: "O trabalho contribuiu para a hernia?" — posicao autor: sim (NTEP Lista A),
   posicao INSS: nao (doenca degenerativa), prova que resolve: laudo Tipo A
5. Questao de direito: art. 21-A Lei 8.213/91 — CNAE 2910701 x CID M54.5 na Lista A — presuncao
   opera — onus do INSS afastar com laudo Tipo A (STJ Tema 503)
6. Provas: CAT (forte — empresa reconheceu nexo), CNIS (media — confirma vinculo), laudo Tipo B
   (contraria — insuficiente mas precisa ser respondido), RM (forte — confirma patologia)
7. Lacuna bloqueante: PPP ausente; como_suprir: oficio ao empregador
8. skill_recomendada: pericia-acidentaria

**Output esperado:** Dossie conforme dossie-caso.v1.json com todos os campos obrigatorios preenchidos.

---

## Caso positivo 2 — Dossie previdenciario BPC-LOAS (Joao, deficiencia intelectual leve)

**Contexto:** Usuaria fornece processo BPC negado por renda.

**Comportamento esperado:**
1. Skill qualifica autor com dados socioeconomicos detalhados (composicao familiar, renda per capita)
2. Fatos naturais: familia de 4 pessoas, renda mensal R$ 1.200,00 (abaixo de 1/4 SM per capita)
3. Fatos clinicos: deficiencia intelectual leve (CID F70) + epilepsia (CID G40), laudos psiquiatrico
   e neurologico
4. Fatos previdenciarios: NB BPC negado com fundamento em renda per capita calculada incorretamente
   (incluiu Bolsa Familia indevidamente)
5. Questao de fato: "O BF foi incluido no calculo de renda?" — sim, confirmado no despacho
6. Questao de direito: art. 20 §§2-3 Lei 8.742 + RE 580.963 STF — BF nao integra renda per capita
   para BPC
7. skill_recomendada: analise-calculo-renda-bpc

**Output esperado:** Dossie com foco previdenciario; lacuna bloqueante = laudo biopsicossocial CIF ausente.

---

## Caso positivo 3 — Atualizacao de dossie existente com novo fato juridico

**Contexto:** Dossie de Maria ja existe; usuaria informa que sentenca saiu desfavoravel.

**Comportamento esperado:**
1. Skill localiza dossie existente (nao cria novo — evita duplicata L16)
2. Adiciona fato juridico: "Sentenca de 2026-04-20 julgou improcedente por ausencia de nexo"
3. Atualiza fase_atual para "recurso"
4. Atualiza status_atual e proxima_acao
5. skill_recomendada: skill de recurso ordinario (a ser criada)

---

## Caso negativo 1 — Pedido de petica sem dossie previo

**Contexto:** Usuaria pede "escreva a replica para o caso da Maria".

**Comportamento esperado:**
1. Skill nao dispara — o pedido e de peca processual
2. Skill replica dispara diretamente
3. Se replica nao tiver dados suficientes, replica solicita que dossie-caso seja montado antes

**Nao fazer:** Montar dossie completo quando a usuaria so quer a replica e ja tem os dados.

---

## Caso negativo 2 — Dossie sem questao de direito identificada

**Contexto:** Usuaria fornece relato rico em fatos mas sem indicar qual tese juridica sustenta a acao.

**Comportamento esperado:**
1. Skill preenche todas as dimensoes de fatos disponiveis
2. Identifica que nenhuma questao de direito foi formulada
3. Aponta a omissao como lacuna bloqueante: "Nenhuma tese juridica identificada — dossie incompleto
   para uso por skill C5. Informar: qual beneficio e pretendido e com base em qual fundamento legal?"
4. Nao gera output como se o dossie estivesse completo

**Nao fazer:** Inventar questao de direito sem base nos fatos fornecidos.
