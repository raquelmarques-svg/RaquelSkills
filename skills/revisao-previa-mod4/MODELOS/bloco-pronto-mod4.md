# Template — Bloco de saída PRONTO PARA mod4

Consumido por: revisao-previa-mod4 §6.
Instrução de uso: substituir todos os campos em [COLCHETES] pelo valor real.
Após produzir este bloco, aguardar confirmação da Raquel antes de acionar mod4.

---

## Bloco PRONTO (nenhum problema bloqueante)

```
---
Status: PRONTO PARA mod4
Revisado por: revisao-previa-mod4 v1.0.0
Data: [AAAA-MM-DD]
Problemas toleráveis: [lista ou "nenhum"]
---

{
  "tipo_documento": "[tipo — ver enum no schema]",
  "processo": {
    "numero": "[nnnnnnn-DD.AAAA.J.TT.OOOO]",
    "vara": "[nome da vara]",
    "comarca": "[cidade/UF]",
    "tipo_justica": "[estadual | federal | trabalhista]"
  },
  "partes": {
    "autor": {
      "nome": "[Nome completo]",
      "qualificacao": "[brasileiro(a), [estado civil], [profissão], portador(a) do CPF [000.000.000-00], residente e domiciliado(a) na [endereço completo], [cidade/UF]"
    },
    "reu": {
      "nome": "[Nome do réu]",
      "qualificacao": "[qualificação ou omitir se padrão]"
    }
  },
  "corpo_texto": "[texto completo da peça em Markdown — substituir aqui]",
  "pedidos": [
    "[Pedido 1 — com fundamento normativo]",
    "[Pedido 2]",
    "[Pedido N]"
  ],
  "honorarios": {
    "percentual": [número],
    "base_calculo": "[condenacao | proveito_economico | valor_causa]"
  },
  "data_protocolizacao": "[AAAA-MM-DD ou null]",
  "observacoes_formatacao": "[instruções específicas para mod4 ou omitir]"
}
```

---

## Bloco BLOQUEADO (um ou mais problemas impedem o avanço)

```
---
Status: BLOQUEADO
Revisado por: revisao-previa-mod4 v1.0.0
Data: [AAAA-MM-DD]
---

Problemas bloqueantes encontrados:

1. [PEDIDO AUSENTE] [Nome do pedido] — fundamento: [art. X Lei Y]
   Providência: adicionar o pedido na seção DOS PEDIDOS com a seguinte redação sugerida:
   "[Texto sugerido do pedido]"

2. [INCONSISTÊNCIA] [Descrição] — encontrado em: [trecho específico]
   Providência: corrigir [campo X] para [valor correto]

3. [CAMPO SCHEMA AUSENTE] campo `[nome]` do status-pre-mod4.v1.json não identificado
   Providência: informar [dado específico]

Após resolver os itens acima: reexecutar revisao-previa-mod4 para emissão do bloco PRONTO.
```

---

## Bloco PRONTO COM ADVERTÊNCIAS (toleráveis — prosseguir com ciência)

```
---
Status: PRONTO PARA mod4
Revisado por: revisao-previa-mod4 v1.0.0
Data: [AAAA-MM-DD]
Advertências (toleráveis — não bloqueiam):
  - [Advertência 1: descrição + localização no texto]
  - [Advertência 2]
---

[JSON completo igual ao bloco PRONTO]
```
