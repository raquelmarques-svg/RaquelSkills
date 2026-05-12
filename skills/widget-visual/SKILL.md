---
name: widget-visual
description: |
  Gera blocos PNG de tabelas e gráficos a partir de dados jurídicos estruturados para inserção direta em petições, manifestações e relatórios. Tipos suportados: tabela de composição de renda BPC, quadro de vínculos empregatícios, linha do tempo de fatos, comparativo de critérios, tabela genérica. INVOQUE quando: "gere um bloco visual", "crie tabela PNG", "visualize a composição de renda", "gráfico para petição", "quadro de vínculos em imagem", "linha do tempo visual", "widget-visual". NÃO usar para criar apresentações (→ pptx), criar DOCX (→ mod4), recortar PDF (→ recorte-pdf), extrair texto de PDF (→ levanta-fatos).
project: Proj02
nucleo: N1
frente: transversal
camada: C3
categoria: capability
justificativa: Produz PNG concreto acionável por mod4 — converte dados tabulares em prova visual sem transcrição manual
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to:
  - mod4
licoes_aplicadas:
  - L2, L3, L9, L10, L12, L13, L19
regras_aplicaveis:
  - R2, R6, R10, R11
---

# widget-visual — Geração de Blocos PNG para Petições

## §0 — Ativação e gate

Inputs obrigatórios antes de prosseguir:

1. **Tipo de widget**: `composicao-renda` | `vinculos` | `linha-do-tempo` | `comparativo` | `tabela`
2. **Dados**: valores em formato de lista ou tabela (fornecidos diretamente ou extraídos de dossie-caso)
3. **Título**: título que aparecerá no topo do bloco PNG
4. **Destino**: pasta de saída (padrão: pasta selecionada do Cowork)

Se tipo ou dados estiverem ausentes, solicito antes de prosseguir.

## §1 — Escopo

FAÇO:
- Gerar PNG de tabela de composição de renda per capita (BPC/LOAS) com membros e valores
- Gerar PNG de quadro de vínculos empregatícios (empresa, função, CNAE, período, renda)
- Gerar PNG de linha do tempo cronológica de fatos do caso
- Gerar PNG de comparativo em duas colunas (ex.: critério INSS vs. critério legal)
- Gerar PNG de tabela genérica N×M com cabeçalho formatado
- Aplicar paleta Almeida Marques (navy #1B3A6B + creme #F5F0E8)
- Salvar com nome descritivo e entregar via present_files

NÃO FAÇO:
- Inserir PNG no DOCX → delego para mod4
- Criar apresentação de slides → delego para pptx skill
- Recortar trecho de PDF → delego para recorte-pdf
- Calcular renda per capita → forneço o layout; cálculo é da usuária ou de analise-calculo-renda-bpc
- Gerar gráficos de barras/pizza (fora do padrão documental — avaliar sob demanda)

## §2 — Pipeline

```
P1. RECEBER E VALIDAR INPUTS
    — Confirmar tipo de widget (tabela ASSETS/tipos-de-widget.md)
    — Confirmar dados no formato adequado ao tipo
    — Confirmar título e destino

P2. MONTAR JSON DE INPUT (SCHEMAS/widget_input.schema.json)
    {
      "tipo": "<tipo>",
      "titulo": "<título>",
      "dados": [ ... ],
      "output_path": "<pasta>"
    }

P3. EXECUTAR SCRIPT
    python3 scripts/gerar_widget.py
      --tipo <tipo>
      --titulo "<titulo>"
      --dados '<json>'
      --output <destino>
      --prefixo <nome-caso>

P4. VERIFICAR OUTPUT
    — Confirmar que PNG foi gerado, tem dimensão > 0 e não está em branco
    — Se falhar: reportar erro com traceback resumido

P5. ENTREGAR
    — Mover PNG para pasta selecionada do Cowork
    — Apresentar via present_files
    — Informar: arquivo, dimensões, tipo de widget
```

## §3 — Output canônico

```
widget-visual: CONCLUÍDO
tipo: [composicao-renda | vinculos | linha-do-tempo | comparativo | tabela]
titulo: "[título do bloco]"
arquivo: [nome-caso]-[tipo]-[YYYYMMDD].png
dimensões: [L]×[A]px  |  DPI: 150
destino: [caminho]
proxima_acao: inserir no DOCX via mod4
```

Variante de erro:
```
widget-visual: ERRO
motivo: [tipo inválido | dados insuficientes | dependência matplotlib ausente]
acao_requerida: [descrição]
```

## §4 — Calibração

SCRIPT: `scripts/gerar_widget.py` — matplotlib + Pillow
DEPENDÊNCIAS: `pip install matplotlib pillow --break-system-packages`
PALETA: navy #1B3A6B · creme #F5F0E8 · texto #222222
LARGURA PADRÃO: 900px (compatível com coluna de petição A4)
ASSETS: tipos e esquemas de dados em `ASSETS/tipos-de-widget.md`
SCHEMA: contrato de input em `SCHEMAS/widget_input.schema.json`

## §5 — Auto-verificação

Verificação: 2026-05-12 · Próxima: 2026-08-12

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] §0 gate com 4 inputs obrigatórios
- [x] §1 FAÇO/NÃO FAÇO
- [x] §2 pipeline com script externo
- [x] §3 output canônico com variante de erro
- [x] §4 calibração com dependências declaradas
- [x] ASSETS/, SCHEMAS/, scripts/, tests/, examples/ presentes
- [x] Tamanho dentro do limite
