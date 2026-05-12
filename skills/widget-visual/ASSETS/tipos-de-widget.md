# Tipos de widget — especificações e esquema de dados

## 1. composicao-renda

**Uso**: tabela de composição de renda per capita para processos BPC/LOAS.

**Colunas obrigatórias**: Membro | Parentesco | Renda Bruta (R$) | Observação

**Linha de total**: gerada automaticamente — soma das rendas + renda per capita calculada.

**Dados esperados** (lista de dicts):
```json
[
  {"membro": "Maria Silva", "parentesco": "Requerente", "renda": 0, "obs": "incapacitada"},
  {"membro": "João Silva",  "parentesco": "Cônjuge",    "renda": 1621.00, "obs": "SM 2026"}
]
```

**SM 2026**: R$ 1.621,00 — limiar BPC: ¼ SM = R$ 405,25 per capita.

---

## 2. vinculos

**Uso**: quadro de vínculos empregatícios extraído de CTPS/CNIS.

**Colunas obrigatórias**: Empresa | Função | CNAE | Admissão | Rescisão | Remuneração

**Dados esperados**:
```json
[
  {"empresa": "Metal Ltda", "funcao": "Auxiliar de Produção",
   "cnae": "2599-3/99", "admissao": "2015-03-01", "rescisao": "2022-07-15",
   "remuneracao": "R$ 1.450,00"}
]
```

---

## 3. linha-do-tempo

**Uso**: cronologia visual de fatos relevantes do caso.

**Campos obrigatórios**: data | evento | dimensão (natural|humano|clínico|previdenciário|jurídico)

**Dados esperados**:
```json
[
  {"data": "2018-04-10", "evento": "Acidente de trabalho", "dimensao": "humano"},
  {"data": "2018-04-11", "evento": "CAT emitida", "dimensao": "previdenciário"}
]
```

---

## 4. comparativo

**Uso**: tabela dois critérios em colunas — ex.: posição do INSS vs. posição da defesa.

**Campos obrigatórios**: item | coluna_a | coluna_b

**Dados esperados**:
```json
{
  "cabecalho": ["Critério", "INSS", "Defesa"],
  "linhas": [
    ["Renda per capita", "R$ 500,00", "R$ 250,00"],
    ["Membros computados", "4", "2"]
  ]
}
```

---

## 5. tabela (genérica)

**Uso**: qualquer tabela N colunas × M linhas.

**Dados esperados**:
```json
{
  "cabecalho": ["Col1", "Col2", "Col3"],
  "linhas": [
    ["val1", "val2", "val3"],
    ["val4", "val5", "val6"]
  ]
}
```
