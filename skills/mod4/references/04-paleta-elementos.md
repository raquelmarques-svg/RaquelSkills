# mod4 / reference 04 — Paleta e elementos gráficos

## Paleta canônica

| Token | Hex | Uso |
|---|---|---|
| Navy | `#2C3B44` | Títulos de seção, cabeçalhos de tabela, barra esquerda da caixa de destaque, bordas externas de tabela |
| Creme-claro | `#F5F1E8` | Fundo da caixa de destaque, zebra linhas pares de tabela |
| Creme | `#EEECE1` | Fundo exclusivo de ementa de jurisprudência |
| Cinza-texto | `#555555` | Rodapé — texto |
| Cinza-linha | `#888888` | Linha superior do rodapé, paginação N/T |
| Cinza-interno | `#CCCCCC` | Linhas internas de tabela |
| Corpo | `#222222` | Texto do corpo |
| Quase-preto | `#111111` | Endereçamento, nome da ação, títulos |
| Branco | `#FFFFFF` | Texto em cabeçalho navy de tabela |

Regra: elementos coloridos não excedem 5% da área útil total.

## Caixa de destaque

Único tipo de caixa autorizado. Uso: síntese de fundamento, alerta metodológico neutro, dispositivo de pedido.

```xml
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="8505" w:type="dxa"/>
    <w:tblBorders>
      <w:top    w:val="nil"/>
      <w:left   w:val="single" w:sz="24" w:color="2C3B44"/>
      <w:bottom w:val="nil"/>
      <w:right  w:val="nil"/>
      <w:insideH w:val="nil"/>
      <w:insideV w:val="nil"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="8505"/></w:tblGrid>
  <w:tr><w:tc>
    <w:tcPr>
      <w:tcW w:w="8505" w:type="dxa"/>
      <w:shd w:val="clear" w:color="auto" w:fill="F5F1E8"/>
      <w:tcMar>
        <w:top w:w="120" w:type="dxa"/>
        <w:left w:w="284" w:type="dxa"/>
        <w:bottom w:w="120" w:type="dxa"/>
        <w:right w:w="284" w:type="dxa"/>
      </w:tcMar>
    </w:tcPr>
    <w:p>
      <w:pPr>
        <w:ind w:left="0" w:firstLine="0"/>
        <w:jc w:val="both"/>
        <w:spacing w:before="0" w:after="0" w:line="288" w:lineRule="auto"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/>
          <w:sz w:val="22"/>
          <w:color w:val="444444"/>
        </w:rPr>
        <w:t xml:space="preserve">TEXTO DA CAIXA</w:t>
      </w:r>
    </w:p>
  </w:tc></w:tr>
</w:tbl>
```

Ativada via `{"tipo": "caixa_destaque", "texto": "..."}` no schema. Tipos proibidos: `caixa_vicio`, `caixa_tese`, `caixa_advertencia`, `caixa_ressalva`.

## Tabela genérica do CORPO

Cabeçalho: fundo `#2C3B44`, texto branco `#FFFFFF`, Cambria 10pt negrito, centrado.
Zebra: linhas pares fundo `#F5F1E8`; linhas ímpares sem fundo.
Bordas externas: `#2C3B44` 4pt. Bordas internas horizontais: `#CCCCCC` 1pt. Verticais internas: sem borda.
Parágrafo em célula: `firstLine=0 left=0`, Cambria 10pt, entrelinha 288.

## Tabela DAS PROVAS

Duas colunas fixas: Documento (4500 DXA) + O que demonstra (4005 DXA). Total: 8505 DXA.
Colunas Tipo e Grau são suprimidas silenciosamente pelo script se presentes no input.
Cabeçalho: navy + texto branco. Zebra: creme-claro. Mesmo padrão da tabela genérica.

## Citação longa (blockquote)

Para transcrições literais de 4+ linhas. Recuo esquerdo 816 DXA, direito 408 DXA.
Borda esquerda 40pt `#AAAAAA`. Itálico, Cambria 11pt, entrelinha 288.
Nunca para paráfrase — apenas transcrição literal de documento, laudo ou decisão.

## Ementa de jurisprudência

Estrutura obrigatória:
- Bloco A: fundo `#EEECE1`, tribunal em Cambria 11pt negrito `#2C3B44`, ementa em Cambria 9pt smallCaps `#444444`
- Bloco B: aplicação ao caso em Cambria 11pt normal `#222222`, mesmo recuo
- Bloco C: referência completa em Cambria 10pt negrito `#2C3B44`

O fundo `#EEECE1` é exclusivo de ementa. Nunca usar em outro contexto.

## Densidade por seção

| Elemento | Peso |
|---|---|
| Parágrafo | 1 |
| Blockquote | 2 |
| Tabela | 3 |
| Caixa de destaque | 2 |

Limite por seção romana: 6 pontos. Acima de 6 → subdividir com decimal (1.1, 1.2).
O script emite aviso quando o limite é excedido; não bloqueia a geração.
