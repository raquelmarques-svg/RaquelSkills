---
name: check-cumprimento-sentenca
description: |
  Verifica os requisitos e produz o roteiro de cumprimento de sentença em ações previdenciárias, acidentárias, cíveis e de família. Cobre: cálculo de atualização (SELIC/IPCA-E), conta de liquidação, intimação do devedor (INSS, União ou particular), RPV vs. precatório, penhora e expropriação em ações cíveis, cumprimento de alimentos (art. 528 CPC). INVOQUE quando: "cumprir sentença", "liquidação de sentença", "RPV", "precatório", "penhora em cumprimento", "calcular o que o INSS deve". NÃO usar para checklist pré-protocolo de ação nova (→ check-protocolo).
project: Proj02
nucleo: N1
frente: transversal
camada: C4
categoria: capability
justificativa: Produz roteiro acionável de cumprimento com cálculos e documentos exigidos — output concreto, não apenas referência.
version: 0.1.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
status: Phase-B
depends_on: []
chains_to:
  - mod4
chains_from:
  - dossie-caso
licoes_aplicadas:
  - L1, L2, L11, L19
regras_aplicaveis:
  - R1, R6, R10, R11
---

# check-cumprimento-sentenca — Roteiro de Cumprimento de Sentença

## Status: Phase B — Estrutura criada, conteúdo pendente de desenvolvimento

Esta skill está na fila de desenvolvimento (Phase B). A estrutura foi criada para evitar
que cumprimento de sentença seja erroneamente processado por `check-protocolo`.

Ao ser invocada antes do desenvolvimento completo, a skill:
1. Identifica o tipo de cumprimento (RPV/precatório, cumprimento de alimentos, penhora cível)
2. Fornece o roteiro básico correspondente com base no conhecimento disponível
3. Sinaliza que o desenvolvimento completo está pendente

## §1 — Escopo planejado (Phase B)

FAREI:
- Verificar tipo de cumprimento: RPV (< 60 salários mínimos) vs. precatório
- Calcular atualização monetária: SELIC (condenações contra Fazenda após STF RE 870.947)
  ou IPCA-E (condenações gerais)
- Verificar conta de liquidação: critérios do INSS, planilha de cálculo
- Roteiro de intimação do devedor: art. 523 CPC (privado) ou art. 535 CPC (Fazenda Pública)
- Verificar prazo de 30 dias para cumprimento espontâneo (Fazenda: 60 dias)
- Para alimentos: art. 528 CPC — intimação + 3 dias + prisão civil ou desconto em folha
- Para RPV: verificar se o crédito é alimentar (preferência no pagamento)

NÃO FAREI:
- Redigir a petição de cumprimento → delego para skill C5 pertinente
- Verificar checklist de ação nova → delego para check-protocolo

## §2 — Trigger semântico (provisório)

Disparo quando: "cumprir sentença", "liquidação", "RPV", "precatório", "penhora",
"calcular o débito", "INSS não cumpriu", "prazo para cumprir".

## §3 — Roteiro básico (disponível antes do desenvolvimento completo)

### Para benefícios previdenciários/acidentários (INSS como réu):

1. Verificar se sentença transitou em julgado (certidão de trânsito)
2. Calcular o débito: parcelas vencidas (DIB → data do cálculo) × índice de atualização
3. Identificar: RPV (< 60 SM = R$ 97.260,00 em 2026) ou precatório (≥ 60 SM)
4. Para RPV: protocolar petição de cumprimento com planilha + pedir expedição de RPV
5. Para precatório: protocolar pedido de expedição de precatório ao tribunal

### Para danos morais/materiais (réu particular):

1. Intimação do devedor (art. 523 CPC): 15 dias para pagar + multa 10% + honorários 10%
2. Se não pagar: penhora (art. 831 CPC) → preferência: dinheiro > veículo > imóvel
3. Expropriação: adjudicação (credor fica com o bem) ou alienação por iniciativa particular

### Para alimentos (art. 528 CPC):

1. Intimação do devedor: 3 dias para pagar as 3 últimas parcelas vencidas
2. Se não pagar: prisão civil (1–3 meses) OU desconto em folha/benefício (art. 529 CPC)
3. Prisão civil: mandado expedido via central do TJXX — verificar procedimento local
