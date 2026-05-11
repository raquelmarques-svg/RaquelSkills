# mod4 / reference 03 — Tipografia

Fonte única: Cambria em todos os níveis. Valores em twips (DXA). Fonte de verdade: `CONFIG/tipografia.json` — nunca hardcodar no script.

## Hierarquia tipográfica

| Nível | Campo JSON | Tam. (half-pt) | Atributos | Cor |
|---|---|---|---|---|
| Endereçamento | `tamanho.enderecamento` = 28 | 14pt | negrito, caixa alta, centrado | `#111111` |
| Nome da ação | `tamanho.nome_acao` = 28 | 14pt | negrito, caixa alta, centrado | `#111111` |
| Título seção | `tamanho.titulo_secao` = 28 | 14pt | negrito, caixa alta, justificado, keepNext | `#2C3B44` |
| Subtítulo (1.1) | `tamanho.subsecao` = 22 | 11pt | negrito | `#111111` |
| Síntese BLUF | `tamanho.sintese` = 22 | 11pt | negrito | `#111111` |
| Corpo | `tamanho.corpo` = 24 | 12pt | justificado | `#222222` |
| Blockquote | `tamanho.blockquote` = 22 | 11pt | itálico | `#444444` |
| Referência doc | `tamanho.referencia_doc` = 22 | 11pt | negrito | `#111111` |
| Caixa destaque | `tamanho.caixa_corpo` = 22 | 11pt | normal | `#444444` |
| Tabela cabeçalho | `tamanho.tabela_header` = 20 | 10pt | negrito | `#FFFFFF` |
| Tabela corpo | `tamanho.tabela_corpo` = 20 | 10pt | normal | `#111111` |
| Rodapé | `tamanho.rodape` = 18 | 9pt | normal, centrado | `#555555` |
| Assinatura nome | 24 | 12pt | negrito, centrado | `#111111` |
| Assinatura dados | 22 | 11pt | centrado | `#444444` |

## Espaçamentos (DXA = twips)

| Transição | before | after |
|---|---|---|
| Seção título | `espacamento.secao_before` = 400 | `espacamento.secao_after` = 240 |
| Subtítulo | `espacamento.subsecao_before` = 200 | `espacamento.subsecao_after` = 120 |
| Corpo | `espacamento.corpo_before` = 120 | `espacamento.corpo_after` = 120 |
| Síntese BLUF | `espacamento.sintese_before` = 60 | `espacamento.sintese_after` = 120 |
| Blockquote | `espacamento.blockquote_before` = 200 | `espacamento.blockquote_after` = 200 |

## Entrelinhas

| Contexto | Campo | Valor DXA |
|---|---|---|
| Corpo | `entrelinha.corpo` | 360 (1,5) |
| Blockquote | `entrelinha.blockquote` | 288 (1,2) |
| Caixa destaque | `entrelinha.caixa` | 288 |
| Tabela | `entrelinha.tabela` | 288 |

## Recuos

| Contexto | Campo | Valor DXA | Observação |
|---|---|---|---|
| Corpo — primeira linha | `indent.corpo_primeira_linha` | 720 | Explícito via `first_line=c(...)`. Nunca herdar. |
| Blockquote — esquerda | `indent.blockquote_esq` | 816 | |
| Blockquote — direita | `indent.blockquote_dir` | 408 | |
| Dentro de tabela | — | 0 | `firstLine=0 left=0` obrigatório |
| Dentro de caixa destaque | — | 0 | `firstLine=0` obrigatório |

## Regra crítica de herança

O estilo Normal no template define `firstLine=709`. O Word cancela silenciosamente essa herança quando qualquer `<w:pPr>` explícito existe no parágrafo — mesmo vazio, mesmo contendo apenas `<w:jc>`. Atributos ausentes assumem zero, não o valor do estilo.

Consequência: todo parágrafo gerado pelo script que tiver `<w:pPr>` deve declarar `firstLine` explicitamente. O script usa `c('indent.corpo_primeira_linha')` = 720 para o corpo e `0` para tabelas/caixas.

## Proibições absolutas

- Sublinhado em qualquer contexto
- Travessão intercalador (—) como pontuação
- Bullets Unicode manuais (• ● ▪ ◆ ⋆ ▲)
- Negrito inline: máximo 2 ocorrências por página fora de títulos e subtítulos
- Itálico: apenas termos estrangeiros, latinismos, títulos de obras; nunca para ênfase
- Caixa alta manual em corpo: usar `<w:caps/>` apenas em títulos de seção
- Cores fora da paleta canônica (reference 04)
