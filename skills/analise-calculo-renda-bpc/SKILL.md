---
name: analise-calculo-renda-bpc
description: >
  Dado um processo BPC/LOAS indeferido por renda, mapeia a composição do cálculo
  de renda per capita do INSS, verifica o SM vigente na data da decisão, identifica
  vícios autônomos com remissão documental, gera blocos visuais como PNG compactos
  e recorta trechos ipsis litteris dos documentos administrativos para inserção
  direta em petições e manifestações.
project: Previdenciário
nucleo: BPC-LOAS
frente: Análise-Administrativa
camada: Ferramenta
categoria: capability
version: 1.0.0
verificado_em: 2026-05-12
upstream:
  - pericia-previdenciaria
downstream:
  - mod4
  - replica
recursos_compartilhados:
  - scripts/pdf_recorte_por_texto.py
  - scripts/html_blocos_para_png.py
  - ASSETS/sm_historico.md
  - ASSETS/normas_bpc.md
---

# analise-calculo-renda-bpc

## §0 — Ativação e gates

### Gatilhos positivos (ativo quando ao menos um aparecer)

| Gatilho | Exemplos |
|---|---|
| Cálculo INSS BPC | "como o INSS chegou a esse valor", "por que foi indeferido por renda" |
| Composição de renda | "o que entrou no cálculo", "quais rendas foram consideradas" |
| Vício no cálculo | "erro no cálculo", "SM errado", "renda sem prova", "CadÚnico desatualizado" |
| Mapeamento documental | "de onde veio esse valor", "qual documento prova isso", "qual ID do documento" |
| Geração visual | "mapa do cálculo", "gerar imagens", "bloco para a petição", "widget" |
| Recorte ipsis litteris | "recortar trecho", "pegar a tabela", "ilustração do processo" |

### Gatilhos negativos (NÃO ativo)

- Redação de petição ou manifestação → mod4 / skill C5
- Cálculo de benefício previdenciário (B31, B87) → pericia-previdenciaria
- Impugnação de laudo médico → pericia-previdenciaria
- Análise normativa isolada do Decreto 12.534/2025 → skill C5

### Gate de entrada

Verificar antes de iniciar:
1. Processo administrativo PDF disponível (com Detalhe da Análise)
2. Data da decisão de indeferimento (buscar no próprio processo se não informada)

R1: perguntar antes de gerar qualquer arquivo de output (PNG, HTML, DOCX, ZIP).
R2: nunca apagar arquivos. Mover para _APAGAR/ com timestamp.
R11: não executar pipeline pesado sem confirmar necessidade.

---

## §1 — Escopo

FAÇO:
- Localizar "CÁLCULO DA RENDA FAMILIAR" no processo PDF
- Extrair cada parcela de renda (valor, tipo, origem, base probatória)
- Verificar SM vigente na data da decisão vs. SM usado pelo INSS
- Calcular limiar correto e comparar com per capita apurado
- Mapear documentos (ID, nome, data, seção, item, status probatório)
- Identificar e ordenar vícios autônomos por força probatória
- Gerar 4 blocos visuais PNG (cálculo, documentos, vícios, fluxo)
- Recortar trechos ipsis litteris do PDF com âncoras de texto precisas
- Produzir schema JSON da análise para consumo por outras skills

NÃO FAÇO:
- Redigir a peça final → mod4 / skill C5
- Avaliar deficiência biopsicossocial → pericia-previdenciaria
- Calcular atrasados ou competências → skill específica

DELEGO PARA:
- mod4: inserção das imagens no DOCX corporativo
- replica: uso da análise como base da réplica
- pericia-previdenciaria: questões sobre laudo e avaliação médica

---

## §2 — Pipeline operacional

Ver references/01-metodo-analise-calculo.md para detalhe de cada etapa.

```
1.  Localizar Detalhe da Análise (buscar "CÁLCULO DA RENDA FAMILIAR" via fitz)
2.  Extrair composição: parcela × valor × tipo × origem × base probatória
3.  Verificar SM: buscar "Valor do Salário Mínimo" na decisão
    → confrontar com ASSETS/sm_historico.md
    → calcular limiar correto (SM_correto / 4)
4.  Comparar: per_capita_INSS vs. limiar_correto e limiar_INSS
5.  Mapear documentos com ID PJe, seção, item, status (ver §3-B)
6.  Identificar vícios com checklist (ASSETS/checklist_vicios.md)
7.  Serializar análise como JSON (SCHEMAS/calculo_renda_input.schema.json)
8.  [R1] Confirmar geração de imagens antes de executar scripts
9.  Gerar blocos PNG via scripts/html_blocos_para_png.py
10. Gerar recortes PNG via scripts/pdf_recorte_por_texto.py
11. Copiar arquivos para pasta do cliente
12. Entregar análise + links de arquivos
```

---

## §3 — Estrutura de saída

### §3-A — Análise textual (chat)

Entregue sempre. Estrutura fixa:

1. **Composição do cálculo** — cada parcela com valor, tipo e base
2. **Verificação do SM** — SM usado vs. SM correto na data da decisão
3. **Tabela de documentos** — ID, nome, seção, status probatório
4. **Vícios ordenados** — cada vício com remissão documental precisa
5. **Conclusão aritmética** — per capita com SM correto e sem parcelas contestadas

### §3-B — Status probatório dos documentos

| Status | Cor | Significado |
|---|---|---|
| Cruzamento de base | Amarelo | Dado verificado em sistema federal (SIBEC, CNIS) |
| Autodeclaração | Vermelho | Apenas declaração no CadÚnico, sem verificação externa |
| Contradição interna | Vermelho | O próprio documento INSS contradiz a imputação |
| Prova favorável | Verde | Documento que apoia a autora |
| Peça do INSS | Cinza | Manifestação processual do impetrado |

### §3-C — Arquivos PNG gerados

Blocos visuais (cada um = uma seção da análise):
- bloco1_calculo.png — tabela de composição + comparação SM correto vs. errado
- bloco2_documentos.png — tabela de documentos com ID e status
- bloco3_vicios.png — cada vício com remissão
- bloco4_fluxo.png — fluxo decisório cronológico

Recortes ipsis litteris do processo:
- recA_tabela_percapita_sm.png — tabela da decisão (per capita + SM)
- recB_conclusao.png — texto da conclusão de indeferimento
- recC_rendas_declaradas.png — tabela de rendas declaradas (CadÚnico)
- recD_comprometimento.png — seção art. 20-B se presente

---

## §4 — Referências internas

- references/01-metodo-analise-calculo.md — pipeline completo de análise
- references/02-metodo-recorte-documentos.md — técnica de recorte por âncora
- references/03-sistema-visual-widget.md — design, cores, layout dos blocos PNG
- references/04-licoes-aprendidas.md — erros e lições desta iteração
- ASSETS/sm_historico.md — SM histórico com datas de vigência exatas
- ASSETS/normas_bpc.md — arcabouço normativo BPC/LOAS
- ASSETS/checklist_vicios.md — 10 vícios comuns com diagnóstico e remissão
- scripts/pdf_recorte_por_texto.py — recorte por âncora de texto (CLI)
- scripts/html_blocos_para_png.py — renderização HTML → PNG compacto (CLI)
- SCHEMAS/calculo_renda_input.schema.json — schema de input estruturado
- MODELOS/mapa_probatorio_html.html — template HTML completo do widget
- examples/casos-teste.md — 3 positivos + 2 negativos

---

## §5 — Calibração obrigatória por execução

Antes de qualquer análise, verificar:
1. SM vigente na data da decisão (não assumir — consultar ASSETS/sm_historico.md)
2. Se há página com "Valor do Salário Mínimo" — buscar textualmente no PDF
3. Se há seção "COMPROMETIMENTO DA RENDA" — indica despesas dedutíveis (art. 20-B) não consideradas
4. Defasagem do CadÚnico — calcular anos entre última atualização e data do requerimento
5. Se o CNIS foi consultado e está zerado — verificar se o INSS imputou renda de trabalho mesmo assim
