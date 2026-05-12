# Casos-teste — levanta-fatos

---

## Caso positivo 1 — CNIS + CTPS + CAT

**Contexto:** Usuaria cola texto do CNIS e da CTPS de Maria da Silva e anexa a CAT.

**Comportamento esperado:**
1. Do CNIS: extrai NIT, vinculos com CNPJ/CNAE/competencias, beneficio B31 NB 123.456.789-0
   com DII 2023-08-10, DIB 2023-08-25, DCB 2024-06-30, RMI R$2.100,00
2. Da CTPS: confirma vinculo Metalurgica ABC Ltda, CNAE 2910701, funcao Operadora de Maquinas,
   admissao 2010-03-01, sem saida registrada
3. Da CAT: CID M54.5, data 2023-08-10, empregador Metalurgica ABC Ltda, CNAE 2910701
4. Verificacao NTEP: CNAE 2910701 x CID M54.5 — consta da Lista A -> `ntep_aplicavel: true`
5. Sinaliza: especie B31 (comum) quando CAT registrada sugere especie B91 (acidentaria)
6. Lacunas: PPP ausente, laudo medico ausente
7. Output: fatos-estruturados.v1.json com todos os campos disponiveis preenchidos

---

## Caso positivo 2 — Processo administrativo BPC com renda a calcular

**Contexto:** Usuaria envia despacho de indeferimento BPC e relatorio de composicao familiar.

**Comportamento esperado:**
1. Extrai: NB BPC, data da decisao, fundamento (renda per capita acima de 1/4 SM), composicao
   familiar (4 pessoas), renda total declarada pelo INSS (R$1.800,00 = R$450,00 per capita)
2. Sinaliza: BF de R$600,00 possivelmente incluido no calculo — inconsistencia (RE 580.963 STF
   exclui BF da renda BPC)
3. skill_recomendada: analise-calculo-renda-bpc
4. Nao calcula sozinha — apenas extrai e sinaliza

---

## Caso positivo 3 — Exame de imagem com data anterior ao vinculo

**Contexto:** Usuaria envia RM de 2019 e CTPS com admissao em 2020.

**Comportamento esperado:**
1. Extrai achados da RM: hernia discal L4-L5 com compressao radicular, data 2019-07-15
2. Extrai CTPS: admissao 2020-03-01
3. Sinaliza inconsistencia/risco: "RM de 2019-07-15 e anterior ao vinculo de 2020-03-01.
   Risco: INSS pode alegar doenca preexistente. Verificar se ha RM mais recente ou se
   o vicio de especie ou a concausa (agravamento) e o argumento correto."
4. Nao resolve o problema — apenas registra o risco em `observacoes`

---

## Caso negativo 1 — Laudo pericial judicial entre os documentos

**Contexto:** Usuaria envia laudo pericial do juizo junto com CNIS e CTPS.

**Comportamento esperado:**
1. Extrai dados factuais do laudo: CID, data, nome do perito, conclusao literal
2. Nao analisa se o laudo e Tipo A/B/C, nao avalia se o NTEP foi afastado, nao formula
   quesitos — esses sao papeis de pericia-acidentaria
3. Registra laudo como `tipo: laudo_pericial_INSS` em `documentos_presentes`
4. skill_recomendada: pericia-acidentaria

---

## Caso negativo 2 — Pedido de analise sem documentos

**Contexto:** Usuaria pede "levante os fatos do caso da Maria" sem fornecer documentos.

**Comportamento esperado:**
1. Skill nao inventa dados
2. Pergunta: "Quais documentos voce tem disponivel? Para extrair os fatos preciso de pelo
   menos um documento do caso (CNIS, CTPS, CAT, laudo ou processo administrativo)."
3. Se a usuaria fornece dados verbalmente (sem documentos), encaminha para dossie-caso,
   que aceita dados de relato direto marcados como `fonte: "Relato da usuaria"`
