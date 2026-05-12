# Checklist pré-protocolo — Benefícios por Incapacidade

Espécies cobertas: B31 (auxílio-doença comum), B91 (auxílio-doença acidentário),
B92 (aposentadoria por invalidez acidentária), B94 (aposentadoria por incapacidade permanente),
B87 (auxílio-acidente).
Fundamento: arts. 18–36, 42–47, 59–63 Lei 8.213/91; art. 21-A (NTEP).
Data de referência: 2026-05-12.

---

## Bloco A — Qualidade de segurado e carência

| # | Item | Status | Obs |
|---|---|---|---|
| A1 | CNIS completo (todos os vínculos, todas as competências) | | |
| A2 | Qualidade de segurado na DII confirmada (dentro do período de graça?) | | |
| A3 | Carência mínima: 12 contribuições mensais (art. 25 I Lei 8.213/91) | | |
| A4 | DII identificada (data em que o cliente parou de trabalhar) | | |
| A5 | DID identificada (data de início da doença, conforme prontuário) | | |

**Verificação obrigatória — período de graça (art. 15 Lei 8.213/91):**
- Desemprego involuntário: 12 meses (pode ser estendido até 36 meses com ≥ 120 contrib.)
- Desemprego com seguro-desemprego: prorrogado enquanto durar o benefício
- Sem vínculo: 12 meses após a última contribuição

---

## Bloco B — Documentos clínicos

| # | Item | Status | Obs |
|---|---|---|---|
| B1 | Laudo médico com CID principal (e secundários se houver), DID, DII, prognóstico | | |
| B2 | Descrição de limitações funcionais (o que o cliente não consegue mais fazer) | | |
| B3 | Exames de imagem (RM, TC, RX, USG) com data e achados descritivos | | |
| B4 | Prontuário médico (histórico de consultas e tratamento) | | |
| B5 | Receitas médicas com medicamentos em uso | | |
| B6 | Atestados de afastamento do empregador | | |
| B7 | Alta hospitalar (se houve internação) | | |

**Verificação:** CID do laudo corresponde ao CID do benefício INSS no CNIS? Se divergir → sinalizar.

---

## Bloco C — Nexo causal (obrigatório para B91/B92)

| # | Item | Status | Obs |
|---|---|---|---|
| C1 | CAT (Comunicação de Acidente de Trabalho) registrada | | |
| C2 | PPP (Perfil Profissiográfico Previdenciário) com CNAE e descrição de atividades | | |
| C3 | CTPS com vínculo ativo ou recente no CNAE relevante | | |
| C4 | NTEP verificado: par CNAE x CID consta da Lista A (Decreto 3.048 Anexo II)? | | |
| C5 | PPRA (Programa de Prevenção de Riscos Ambientais) do empregador | | |
| C6 | PCMSO (Programa de Controle Médico de Saúde Ocupacional) | | |

**Verificação NTEP — se par consta da Lista A:**
`ntep_aplicavel: true` → presunção de nexo opera de pleno direito (art. 21-A Lei 8.213/91).
O INSS deve afastar com laudo Tipo A — o ônus é dele.

**Verificação de espécie:**
- CAT presente + NTEP verdadeiro → B91, não B31
- CNIS mostra B31 quando deveria ser B91 → vício de espécie (sinalizar)

---

## Bloco D — Documentos laborais

| # | Item | Status | Obs |
|---|---|---|---|
| D1 | CTPS completa (todos os vínculos, todas as anotações) | | |
| D2 | Contrato de trabalho ou registros de vínculo | | |
| D3 | Rescisão contratual (TRCT) se vínculo encerrado | | |
| D4 | Holerites dos últimos 12 meses antes do afastamento | | |
| D5 | Extrato de FGTS (para pedido de FGTS + multa quando B91/B92) | | |

---

## Bloco E — Verificações jurídicas obrigatórias

| # | Verificação | OK/Alerta |
|---|---|---|
| E1 | Espécie correta: B31 vs. B91 vs. B92 vs. B94? | |
| E2 | DII vs. DIB: diferença gera retroativo (art. 58 Lei 8.213/91)? | |
| E3 | DID anterior ao vínculo? Risco: INSS alega doença preexistente. Contra-argumento: concausa / agravamento | |
| E4 | Benefício cessado (DCB presente no CNIS)? Direito à prorrogação ou revisão? | |
| E5 | FGTS depositado durante afastamento? (obrigatório durante B91/B92) | |
| E6 | Estabilidade acidentária (art. 118 Lei 8.213/91): 12 meses após cessação do B91? | |
| E7 | Auxílio-acidente (B87): sequela permanente que reduz capacidade? | |

---

## Bloco F — Lacunas e providências

**Bloqueantes:**
- Laudo médico sem DII → retornar ao médico
- Qualidade de segurado não confirmável (CNIS incompleto) → requerer CNIS atualizado
- Vínculo não comprovado para B91 → requerer CTPS ou extrato CNIS com CNAE
- CAT ausente quando NTEP verdadeiro → considerar CAT extemporânea (via sindicato ou pelo próprio segurado)

**Toleráveis:**
- PPP ausente → requerer por ofício ao empregador após distribuição
- PPRA/PCMSO ausente → requerível ao empregador ou SRTE
- Exame de imagem desatualizado → requerer atualização por diligência

---

## Bloco G — Pedidos a incluir

- Concessão/restabelecimento do benefício na espécie correta (B31/B91/B92/B94)
- DIB desde a DII (retroativo — art. 58 Lei 8.213/91)
- Reconversão de espécie (B31 → B91) quando NTEP verdadeiro e CAT presente
- Correção monetária + juros SELIC
- Tutela de urgência quando cessação recente e vulnerabilidade comprovada
- Para B91: estabilidade de 12 meses + FGTS durante afastamento + multa 40%
- Para B87: parcelas vencidas desde o fim da incapacidade total
- Gratuidade de justiça
