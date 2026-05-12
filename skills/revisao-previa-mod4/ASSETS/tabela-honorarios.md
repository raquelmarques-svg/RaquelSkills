# Tabela de honorários advocatícios

Consumido por: revisao-previa-mod4 §3 D3.
Data de referência: 2026-05-12. SM 2026: R$ 1.621,00.

---

## Regras gerais

**Juizados Especiais Federais (JEF) — art. 55 Lei 9.099/95:**
- Fase de conhecimento: sem condenação em honorários (cada parte arca com os seus), salvo má-fé
- Fase de execução/cumprimento: 10% sobre o valor executado
- ATENÇÃO: entendimento majoritário das Turmas Recursais aplica honorários ao INSS mesmo
  na fase de conhecimento quando há condenação. Verificar o entendimento do tribunal local.
- Base de cálculo: valor da condenação (retroativo + 12 meses de benefício como proveito econômico mínimo)

**Vara Federal / Vara Cível / Vara do Trabalho — art. 85 CPC:**
- Percentual: entre 10% e 20% sobre o valor da condenação ou do proveito econômico
- Para condenações contra Fazenda Pública: art. 85 §3º CPC (escala regressiva)
  - Até 200 SM (R$ 324.200): 10%–20%
  - De 200 a 2.000 SM: 8%–10%
  - De 2.000 a 20.000 SM: 5%–8%
  - Acima de 20.000 SM: 3%–5%
- Mínimo: R$ 1.000,00 (art. 85 §8º CPC), independentemente do percentual calculado

---

## Cálculo por tipo de ação

### BPC/LOAS

Base de cálculo típica:
- Retroativo: (meses entre DER e DIB) × BPC mensal (1 SM = R$ 1.621,00)
- Proveito futuro: 12 meses × R$ 1.621,00 = R$ 19.452,00
- Total mínimo para honorários: retroativo + R$ 19.452,00
- Honorários sugeridos: 20% × total

Exemplo: DER há 18 meses, retroativo = 18 × R$ 1.621,00 = R$ 29.178,00
Total base = R$ 29.178,00 + R$ 19.452,00 = R$ 48.630,00
Honorários = R$ 9.726,00

### Benefício por incapacidade (B31/B91)

Base de cálculo:
- Retroativo: (meses DII → DIB concedida pelo INSS ou DER) × RMI
- Para B31 → B91: acréscimo de SAT/RAT e eventuais diferenças de RMI
- Proveito futuro: 12 meses × RMI
- Honorários sugeridos: 15% (vara cível) ou 20% (JEF, fase de execução)

### Danos morais/materiais (vara cível/trabalhista)

- Honorários calculados sobre o total da condenação (danos morais + materiais + lucros cessantes + pensão)
- Percentual usual: 15%–20%
- Para pensão vitalícia: capitalizar a pensão para fins de base de cálculo (art. 85 §9º CPC)
  Fórmula: pensão mensal × 12 × anos de expectativa de vida restante (tabela IBGE)

### Artigo jurídico

- `honorarios: null` (não há condenação judicial)

---

## Campos do schema status-pre-mod4.v1.json

```json
"honorarios": {
  "percentual": 20,
  "base_calculo": "condenacao"
}
```

`base_calculo` aceita: `"condenacao"` | `"proveito_economico"` | `"valor_causa"`

---

## Honorários de sucumbência vs. contratuais

Esta tabela trata exclusivamente de honorários de sucumbência (pedidos na peça judicial).
Honorários contratuais (cláusula entre cliente e escritório) são registrados na planilha
financeira do escritório — não entram no pedido judicial.

Quando a peça inclui cláusula contratual de honorários: verificar se não há confusão entre
honorários contratuais e sucumbenciais. Os dois são devidos independentemente (art. 24 §1º Lei 8.906/94).
