---
name: widget-visual
description: |
  Gera widgets HTML ricos via show_widget para exibição no chat e inserção em documentos via screenshot. Tipos suportados: composicao-renda, vinculos, linha-do-tempo, comparativo, tabela, e qualquer layout visual jurídico. INVOQUE quando: "gere um bloco visual", "crie tabela HTML", "visualize a composição de renda", "widget para petição", "quadro de vínculos", "linha do tempo visual", "widget-visual", "extravagante", "cores mais fortes". NÃO gera PNG em operação normal. NÃO usar para criar apresentações (→ pptx), criar DOCX (→ mod4), recortar PDF (→ recorte-pdf), extrair texto de PDF (→ levanta-fatos).
project: Proj02
nucleo: N1
frente: transversal
camada: C3
categoria: capability
justificativa: Produz widget HTML via show_widget — converte dados tabulares em prova visual para chat e documentos sem geração de arquivo
version: 2.0.0
verificado_em: 2026-05-13
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to: []
licoes_aplicadas:
  - L1, L2, L3, L9, L10, L12, L13, L19
regras_aplicaveis:
  - R1, R2, R6, R10, R11
---

# widget-visual — Widgets HTML para Chat e Documentos

## §0 — Ativação e gate

Inputs obrigatórios antes de prosseguir:

1. **Tipo de widget**: `composicao-renda` | `vinculos` | `linha-do-tempo` | `comparativo` | `tabela` | layout livre descrito pela usuária
2. **Dados**: valores em formato de lista ou tabela (fornecidos diretamente ou extraídos de dossie-caso)
3. **Título**: título que aparecerá no cabeçalho do bloco

Dimensões fixas — não negociáveis: `max-width: 567px` (≈15cm) · `max-height: 340px` (≈9cm) · `overflow: hidden`.
Nenhuma pasta de saída. Nenhum arquivo gerado. Output exclusivo: `mcp__visualize__show_widget`.

Se tipo ou dados estiverem ausentes, solicito antes de prosseguir.

## §1 — Escopo

FAÇO:
- Gerar widget HTML de composição de renda per capita (BPC/LOAS) com membros e valores
- Gerar widget HTML de quadro de vínculos empregatícios (empresa, função, CNAE, período, renda)
- Gerar widget HTML de linha do tempo cronológica de fatos do caso
- Gerar widget HTML de comparativo em duas colunas (ex.: critério INSS vs. critério legal)
- Gerar widget HTML de tabela genérica N×M com cabeçalho formatado
- Gerar layouts visuais livres quando a usuária descrever o conteúdo
- Aplicar paleta Almeida Marques padrão ou estilo extravagante (ver §4)
- Quebrar em múltiplos widgets (W1, W2, W3...) quando conteúdo exceder 340px de altura

NÃO FAÇO:
- Gerar PNG — proibido em operação interativa normal (edge case: html_para_imagem.py em pipeline automatizado sem browser)
- Chamar scripts/gerar_widget.py — obsoleto, substituído por show_widget
- Inserir widget no DOCX → delego para mod4 (que recebe screenshot da usuária)
- Criar apresentação de slides → delego para pptx skill
- Recortar trecho de PDF → delego para recorte-pdf
- Calcular renda per capita → forneço o layout; cálculo é da usuária ou de analise-calculo-renda-bpc

DELEGO PARA:
- `mod4` — quando widget aprovado deve ser inserido em DOCX (usuária faz screenshot e passa para mod4)
- `analise-calculo-renda-bpc` — quando cálculo de renda BPC é necessário antes do widget

## §2 — Pipeline

```
P1. RECEBER E VALIDAR INPUTS
    — Confirmar tipo de widget (ASSETS/tipos-de-widget.md)
    — Confirmar dados no formato adequado ao tipo
    — Confirmar título
    — Verificar se estilo extravagante foi solicitado (§4)

P2. AVALIAR ALTURA ESTIMADA
    — Estimar altura do conteúdo antes de renderizar
    — Se estimativa > 340px: redesenhar priorizando carga decisória (suprimir acessório)
    — Se redesenho não resolve: planejar múltiplos widgets W1, W2, W3...

P3. MONTAR HTML
    — Seguir paleta e tipografia de feedback_widgets_html.md
    — Aplicar dimensões: max-width 567px · overflow: hidden · altura auto até 340px
    — Se extravagante: full-bleed backgrounds, números 42-52px, ícones Tabler, badges 20px

P4. RENDERIZAR VIA show_widget
    — Chamar mcp__visualize__show_widget com o HTML montado
    — Confirmar exibição no chat

P5. REPORTAR
    — Informar tipo, título e quantidade de widgets gerados
    — Orientar sobre screenshot para inserção em documento
```

## §3 — Output canônico

```
widget-visual: CONCLUÍDO
tipo: [composicao-renda | vinculos | linha-do-tempo | comparativo | tabela | livre]
titulo: "[título do bloco]"
widgets_gerados: [1 | W1+W2+W3]
dimensoes: ≤ 567px × ≤ 340px por widget
output: show_widget (chat)
proxima_acao: screenshot para inserção em documento
```

Variante de erro:
```
widget-visual: ERRO
motivo: [tipo inválido | dados insuficientes | conteúdo irredutível acima de 340px]
acao_requerida: [descrição]
```

## §4 — Calibração

OUTPUT: `mcp__visualize__show_widget` — HTML rico via browser (nunca PNG em operação normal)
DIMENSÕES: max-width 567px · max-height 340px · overflow: hidden
SCRIPT gerar_widget.py: desativado para operação interativa — não chamar

PALETA PADRÃO (Almeida Marques):
- Header: #1B3A6B (navy) · texto header: #F5F0E8 (creme) · secundário: #a0b8d8
- Fundo geral: #F7F5F0 · cards: #FFFFFF · navy secundário: #2C4A8C
- Vermelho: #C0392B / fundo #FDECEA · verde: #2c7a2c / fundo #EFF8F0
- Laranja: #B06000 / fundo #FFF8F0 · chips: #E8EEF8

PALETA EXTRAVAGANTE (ativada por "extravagante", "cores mais fortes"):
- Full-bleed colored backgrounds (card inteiro navy, crimson #7B1010 ou floresta #0F3D2E)
- Números isolados 42-52px, font-weight: 900
- Split panels com borda lateral 4px na cor de ênfase
- Ícones Tabler: <i class="ti ti-NAME" aria-hidden="true">
- Badges border-radius: 20px, cores contrastantes
- Dourado #FFD700 como acento em fundos escuros
- Manter flat design: sem gradientes, sombras ou blur

TIPOGRAFIA: Inter sans-serif · labels 9-9.5px uppercase · corpo 11-12px · títulos 13-14px
ASSETS: tipos e esquemas de dados em ASSETS/tipos-de-widget.md

## §5 — Auto-verificação

Verificação: 2026-05-13 · Próxima: 2026-08-13

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] R1, R2, R6, R10, R11 presentes
- [x] §0 gate com inputs obrigatórios e dimensões declaradas
- [x] §1 FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] §2 pipeline sem script externo (show_widget nativo)
- [x] §3 output canônico com variante de erro
- [x] §4 calibração com paleta padrão e extravagante
- [x] ASSETS/, SCHEMAS/, scripts/, tests/, examples/ presentes
- [x] Tamanho dentro do limite

## §6 — Lições incorporadas

L1 (mai/2026) — Output mudou de PNG para show_widget exclusivo. gerar_widget.py produz resultado inferior. html_para_imagem.py permanece como edge case de pipeline automatizado sem browser — não chamar em sessões interativas.

L2 (mai/2026) — Dimensões canônicas: 567px × 340px. Excesso → redesenhar priorizando carga decisória, depois quebrar em W1/W2/W3. Nunca comprimir fonte abaixo de 10px ou sacrificar hierarquia visual.

L3 (mai/2026) — Estilo extravagante tem parâmetros concretos aprovados: full-bleed backgrounds, números 42-52px, ícones Tabler, split panels 4px, badges 20px, fundos escuros com dourado #FFD700. Paleta estendida: crimson #7B1010, floresta #0F3D2E.
