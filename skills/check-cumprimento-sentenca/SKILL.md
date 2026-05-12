---
name: check-cumprimento-sentenca
description: |
  Verifica os requisitos e produz o roteiro de cumprimento de sentença em ações previdenciárias, acidentárias, cíveis e de família. Cobre: cálculo de atualização (SELIC/IPCA-E), conta de liquidação, intimação do devedor (INSS, União ou particular), RPV vs. precatório, penhora e expropriação em ações cíveis, cumprimento de alimentos (art. 528 CPC). INVOQUE quando: "cumprir sentença", "liquidação de sentença", "RPV", "precatório", "penhora em cumprimento", "calcular o que o INSS deve", "INSS não cumpriu", "como cobrar a sentença". NÃO usar para checklist pré-protocolo de ação nova (→ check-protocolo).
project: Proj02
nucleo: N1
frente: transversal
camada: C4
categoria: capability
justificativa: Produz roteiro acionável de cumprimento com cálculos, prazos e documentos exigidos — output concreto diferenciado por tipo de réu
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to:
  - mod4
licoes_aplicadas:
  - L1, L2, L3, L11, L12, L19
regras_aplicaveis:
  - R1, R6, R10, R11
---

# check-cumprimento-sentenca — Roteiro de Cumprimento de Sentença

## §0 — Ativação e gate

Inputs obrigatórios antes de prosseguir:

1. **Tipo de réu**: INSS/União (→ art. 535 CPC) | particular (→ art. 523 CPC) | alimentos (→ art. 528 CPC)
2. **Trânsito em julgado**: confirmado? Data do trânsito?
3. **Natureza do crédito**: benefício previdenciário/acidentário | danos morais/materiais | alimentos
4. **Valor estimado do débito** (para classificar RPV vs. precatório)

Se qualquer campo estiver ausente, solicito antes de prosseguir. Não estimo valores sem dados.

## §1 — Escopo

FAÇO:
- Classificar o cumprimento: RPV | precatório | execução cível | alimentos (art. 528)
- Calcular limiar RPV 2026: 60 × R$ 1.621,00 = **R$ 97.260,00**
- Determinar índice de atualização monetária aplicável (SELIC ou IPCA-E)
- Produzir roteiro sequencial com prazos, normas e documentos por tipo de réu
- Identificar documentos necessários: planilha de cálculo, certidão de trânsito, decisão
- Sinalizar riscos processuais: multa 10%, honorários 10%, prisão civil, penhora online

NÃO FAÇO:
- Redigir a petição de cumprimento → delego para skill C5 pertinente + mod4
- Verificar checklist de ação nova → delego para check-protocolo
- Calcular o valor exato do débito (sem planilha de cálculo fornecida)
- Verificar procedimento local de prisão civil (varia por tribunal)

## §2 — Pipeline por tipo de réu

### BLOCO A — Fazenda Pública (INSS, União, autarquias) → art. 535 CPC

```
P1. CLASSIFICAÇÃO DO CRÉDITO
    — Benefício previdenciário/acidentário: natureza alimentar → prioridade no RPV
    — Danos morais contra INSS: natureza não-alimentar → fila normal
    — Verificar se há cumulação (benefício + danos morais): separar em dois pedidos

P2. ATUALIZAÇÃO MONETÁRIA (referência: RE 870.947 STF, 20/09/2017)
    — Parcelas até 11/2021: IPCA-E + juros TR (período anterior ao RE)
    — Parcelas a partir de 12/2021: SELIC acumulada (substitui IPCA-E + TR)
    — Honorários advocatícios: calculados sobre o total corrigido (art. 85 §§ 3-4 CPC)

P3. LIMIAR RPV vs. PRECATÓRIO (SM 2026 = R$ 1.621,00)
    — RPV: crédito < 60 SM = R$ 97.260,00
    — Idoso/deficiente: RPV dobrado = 120 SM = R$ 194.520,00 (art. 100 §2 CF)
    — Precatório: crédito ≥ limiar → apresentar ao TRF/TJ até 01/07 para pagamento
      no exercício seguinte

P4. INTIMAÇÃO DA FAZENDA (art. 535 CPC)
    — Prazo: 60 dias (não 15) para cumprimento espontâneo
    — Fazenda não impugna e não paga: multa 10% automática após os 60 dias
    — Fazenda impugna: contestação em 30 dias → juiz decide

P5. CHECKLIST DOCUMENTAL
    — Certidão de trânsito em julgado
    — Planilha de cálculo (SELIC acumulada via Banco Central ou planilha do INSS)
    — Decisão condenatória + acórdão (se houver)
    — Petição de cumprimento + requerimento de RPV/precatório
    — Comprovante de pagamento de custas (se exigido pelo TRF/TJ)
```

### BLOCO B — Réu particular → art. 523 CPC

```
P1. INTIMAÇÃO DO DEVEDOR (art. 523 CPC)
    — Prazo: 15 dias para pagamento voluntário
    — Termo inicial: intimação do devedor (via advogado ou publicação)
    — Se pagar no prazo: sem multa, sem honorários adicionais

P2. INADIMPLEMENTO (art. 523 §1 CPC)
    — Multa automática: 10% sobre o débito
    — Honorários adicionais: 10% sobre o débito
    — Total acrescido ao crédito: não precisa de nova decisão — automático

P3. PENHORA (art. 831 CPC)
    — Ordem de preferência legal (art. 835 CPC):
        1º dinheiro (penhora online SISBAJUD)
        2º títulos da dívida pública
        3º títulos e valores mobiliários
        4º veículos (RENAJUD)
        5º bens imóveis
        6º bens móveis em geral
    — SISBAJUD: requerer via sistema — juiz defere; banco bloqueia em 24h

P4. EXPROPRIAÇÃO
    — Adjudicação (art. 876 CPC): credor pede ficar com o bem pelo valor da avaliação
    — Alienação particular (art. 879 CPC): credor ou devedor indica comprador em 15 dias
    — Leilão judicial (art. 881 CPC): publicação de edital → prazo mínimo 5 dias úteis
```

### BLOCO C — Alimentos → art. 528 CPC

```
P1. ESCOPO DO CUMPRIMENTO ESPECIAL
    — Cobre apenas as 3 ÚLTIMAS prestações vencidas (prestações pretéritas anteriores
      a essas 3 seguem o rito comum do art. 523 CPC — execução de título)
    — Calcular: 3 × valor mensal × índice de atualização (INPC para alimentos, por convenção)

P2. INTIMAÇÃO ESPECIAL (art. 528 CPC)
    — Prazo: 3 dias para pagar OU justificar impossibilidade
    — Se pagar: execução encerrada
    — Se justificar: juiz avalia — se aceita, converte para art. 523

P3. PRISÃO CIVIL (art. 528 §3 CPC) — não paga e não justifica
    — Prazo da prisão: 1 a 3 meses
    — Regime: fechado; não substitui a dívida (paga e é solto, mas ainda deve)
    — Mandado expedido ao TJXX — verificar procedimento da central local
    — Reiteração: possível se inadimplência continuar após soltura

P4. DESCONTO EM FOLHA/BENEFÍCIO (art. 529 CPC) — alternativa à prisão
    — Requerer ao juiz ofício ao empregador/INSS para desconto
    — Limitado a 50% dos rendimentos líquidos do devedor
    — Mais eficaz quando devedor tem emprego formal ou benefício previdenciário
```

## §3 — Output canônico

Ao final do pipeline, apresento:

```
CUMPRIMENTO DE SENTENÇA — [data]
réu: [INSS/União | particular | devedor de alimentos]
natureza_crédito: [alimentar | não-alimentar]
valor_estimado: R$ [X]
classificação: [RPV | PRECATÓRIO | EXECUÇÃO CÍVEL | ALIMENTOS art. 528]
limiar_RPV_2026: R$ 97.260,00 (60 SM) | R$ 194.520,00 (idoso/deficiente)

RITO APLICÁVEL: art. [523 | 535 | 528] CPC
prazo_intimação: [15 | 60 | 3] dias
índice_atualização: [SELIC | IPCA-E | INPC]
multa_inadimplemento: [10% + 10% honorários | não aplicável]

DOCUMENTOS NECESSÁRIOS:
  [ ] Certidão de trânsito em julgado
  [ ] Planilha de cálculo com índice [SELIC|IPCA-E|INPC]
  [ ] Petição de cumprimento/requerimento [RPV|precatório|penhora]
  [ ] [item específico do caso]

PRÓXIMA AÇÃO: [descrição da primeira providência concreta]
RISCO PRINCIPAL: [multa automática | decadência RPV | prescrição execução]
```

## §4 — Calibração

DADO NECESSÁRIO: tipo de réu + natureza do crédito + valor estimado + data do trânsito
BASE NORMATIVA: CPC arts. 523, 528, 535 · CF art. 100 · RE 870.947 STF · SM 2026 = R$ 1.621,00

## §5 — Auto-verificação

Verificação: 2026-05-12 · Próxima: 2026-08-12

Checklist:
- [x] Frontmatter V4 completo (version: 1.0.0)
- [x] verificado_em ≤ 90 dias
- [x] §0 gate com 4 campos obrigatórios
- [x] §1 FAÇO/NÃO FAÇO canônico
- [x] §2 pipeline por tipo de réu (3 blocos)
- [x] §3 output canônico com checklist documental
- [x] §4 calibração com base normativa
- [x] Tamanho dentro do limite
