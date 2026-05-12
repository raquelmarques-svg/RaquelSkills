# casos-teste — widget-visual

## CT-01 — Composição de renda BPC (positivo)

**Entrada:**
- tipo: composicao-renda
- título: "Composição de Renda Familiar — BPC/LOAS"
- 3 membros: requerente (R$0), cônjuge (R$1.621,00), filha menor (R$0)

**Output esperado:**
- PNG com tabela 4 colunas + linha de total + linha de renda per capita
- Renda per capita = R$ 540,33 → "> ¼ SM ✗" (acima do limiar BPC)
- Paleta navy/creme aplicada

---

## CT-02 — Quadro de vínculos empregatícios (positivo)

**Entrada:**
- tipo: vinculos
- dados: 3 empregos com CNAE, admissão e rescisão

**Output esperado:**
- PNG com 6 colunas, 3 linhas de dados
- Linhas alternadas creme/cinza

---

## CT-03 — Linha do tempo de fatos (positivo)

**Entrada:**
- tipo: linha-do-tempo
- 5 eventos de 2018-2022, dimensões mistas

**Output esperado:**
- PNG com tabela ordenada cronologicamente
- Coluna dimensão preenchida (natural, clínico, jurídico...)

---

## CT-04 — Tipo inválido (negativo)

**Entrada:** `--tipo grafico-pizza`

**Output esperado:**
```
error: argument --tipo: invalid choice: 'grafico-pizza'
```
returncode ≠ 0

---

## CT-05 — JSON malformado em --dados (negativo)

**Entrada:** `--dados "nao_e_json"`

**Output esperado:**
```
ERRO: JSON inválido em --dados: ...
```
returncode = 1
