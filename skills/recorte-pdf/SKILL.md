---
name: recorte-pdf
description: |
  Recorta páginas ou regiões de um PDF de processo como imagem PNG — equivalente a um screenshot preciso para inserção direta em petições e manifestações. INVOQUE quando: "recorte esta página", "tire um print do processo", "screenshot desta decisão", "extraia esta parte do PDF", "quero inserir este trecho como imagem", "recorte o despacho", "print da página X". NÃO usar para extrair texto editável (→ levanta-fatos), para converter PDF inteiro (→ pdf skill), para organizar pasta (→ juridir).
project: Proj02
nucleo: N1
frente: transversal
camada: C3
categoria: capability
justificativa: Produz PNG acionável de trecho de processo para inserção em peças — elimina transcrição manual e preserva fidelidade documental
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to:
  - mod4
licoes_aplicadas:
  - L2, L3, L9, L12, L19
regras_aplicaveis:
  - R2, R6, R10, R11
---

# recorte-pdf — Recorte de Trechos de Processo como PNG

## §0 — Ativação e gate

Inputs obrigatórios:

1. **Arquivo PDF**: caminho ou arquivo anexado
2. **Página(s)**: número(s) de página — ex.: `3`, `3-5`, `3,7,12`
3. **Região** (opcional): "página inteira" (padrão) ou coordenadas aproximadas
   ex.: "metade superior", "rodapé", "bloco central"
4. **Destino**: onde salvar os PNGs (padrão: pasta selecionada do Cowork)

Se o PDF não estiver acessível, solicito antes de prosseguir.

## §1 — Escopo

FAÇO:
- Recortar páginas inteiras como PNG em alta resolução (150 DPI padrão, 300 DPI se solicitado)
- Recortar regiões específicas dentro de uma página (metade superior/inferior, bloco indicado)
- Processar múltiplas páginas em lote (ex.: págs. 3-7 → 5 PNGs numerados)
- Aplicar margem leve para não cortar texto na borda
- Salvar com nome descritivo: `[nome-processo]-p[N]-[descricao].png`
- Entregar via present_files

NÃO FAÇO:
- Extrair texto editável → delego para levanta-fatos ou pdf skill
- Converter o PDF inteiro → delego para pdf skill
- Fazer OCR → delego para levanta-fatos
- Editar ou anotar o PDF → fora do escopo

## §2 — Pipeline

```
P1. RECEBER INPUTS
    — Confirmar caminho do PDF e acessibilidade
    — Parsear lista de páginas (única / intervalo / lista)
    — Identificar região: inteira | superior | inferior | central | personalizada

P2. EXECUTAR SCRIPT
    — python3 scripts/recortar_pdf.py
        --pdf [caminho]
        --pages [lista]
        --region [inteira|superior|inferior|central]
        --dpi [150|300]
        --output [diretório de saída]

P3. VERIFICAR OUTPUT
    — Confirmar que cada PNG foi gerado e não está em branco
    — Se página em branco: reportar e sugerir DPI maior

P4. ENTREGAR
    — Mover PNGs para pasta selecionada do Cowork
    — Apresentar via present_files com nome e página correspondente
```

## §3 — Output canônico

```
recorte-pdf: CONCLUÍDO
arquivo_origem: [nome.pdf]
páginas_processadas: [lista]
arquivos_gerados:
  - [nome-processo]-p03-decisao.png
  - [nome-processo]-p04-decisao.png
dpi: 150
destino: [caminho]
```

Se falhar:
```
recorte-pdf: ERRO
motivo: [PDF protegido por senha | página fora do intervalo | arquivo não encontrado]
ação_requerida: [descrição]
```

## §4 — Calibração

SCRIPT: `scripts/recortar_pdf.py` — usa PyMuPDF (fitz)
DEPENDÊNCIA: `pip install pymupdf --break-system-packages`
DPI PADRÃO: 150 (adequado para petição impressa); usar 300 para zoom

## §5 — Auto-verificação

Verificação: 2026-05-12 · Próxima: 2026-08-12

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] §0 gate com 4 inputs
- [x] §1 FAÇO/NÃO FAÇO
- [x] §2 pipeline com script externo
- [x] §3 output canônico com variante de erro
- [x] Tamanho dentro do limite
