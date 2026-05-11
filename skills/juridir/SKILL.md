---
title: juridir
description: "Organiza pastas jurídicas brasileiras de forma autonarrativa: lê, converte para PDF, comprime, nomeia TIPO-SUJEITO-DATA, agrupa imagens de conjunto em PDF único, preserva tudo em _APAGAR antes de qualquer alteração. A skill decide sozinha; não devolve pendência."
version: 2.0.0
category: capability
núcleo: TBD
frente: transversal
camada: C1
projeto: TBD
author: Raquel de Almeida Marques
verified_in: 2026-05-11
git_repo: C:\RaquelSkills
git_auto_commit: true
---

# juridir — Organização de Pasta Jurídica

**Ativar quando a usuária mencionar:** organizar pasta, classificar documentos, padronizar
nomes, renomear arquivos jurídicos, limpar pasta do cliente, achar duplicatas, extrair dados
de um caso, arrumar bagunça, holerites/CNIS/laudos/certidões desorganizados, pasta com nome
de cliente brasileiro.

A skill decide sozinha. Não devolve pendência sem esgotar a cascata de classificação.

---

## §0 — Princípio organizador

O objetivo é deixar a pasta autonarrativa: a leitura da listagem de arquivos reconstrói o
caso sem abrir nenhum documento. Para isso, cada arquivo precisa de três atributos: (1) tipo
correto — o que o documento é juridicamente; (2) sujeito correto — a quem pertence; (3) data
correta — quando foi emitido ou gerado. O nome canônico é a síntese desses três atributos.

**Regra absoluta de preservação:** nenhum arquivo é destruído ou apagado. Toda cópia original
de arquivo que vai ser renomeado, convertido, comprimido ou movido é preservada em
`_APAGAR/__ORIGINAIS__/` antes da operação. Duplicatas vão para `_APAGAR/duplicidade/`.
Lixo vai para `_APAGAR/lixo/`. A pasta `_APAGAR/` é criada na raiz da pasta processada.

## §0-Regras aplicáveis

- **R2 (preservação):** nunca deletar. Toda movimentação para fora do caminho ativo vai para
  `_APAGAR/` com estrutura de subpasta por motivo.
- **R3 (backup por arquivo):** antes de qualquer alteração em arquivo existente (rename,
  conversão, compressão), copiar o original para `_APAGAR/__ORIGINAIS__/` mantendo o
  nome original. Sem cópia bem-sucedida, abortar a operação naquele arquivo.
- **R6 (adaptação):** quando a classificação for ambígua, registrar hipótese e motivo no
  log; não travar o pipeline.
- **R11 (economia de ação):** processar em fases baratas antes das caras; usar cache de OCR
  e visão para não reprocessar arquivo já classificado.

## §0-Leituras obrigatórias antes de processar

1. `ASSETS/tipos.csv` — vocabulário fechado de TIPO
2. `ASSETS/pastas.csv` — vocabulário de subpastas substantivas
3. `DOCS/regras_nomeacao.md` — algoritmo de nomeação contextual
4. `DOCS/regras_pastas.md` — algoritmo de generalização hierárquica

---

## §1 — Escopo

**FAÇO:**
- Inventariar e classificar todos os arquivos da pasta (exceto `_APAGAR/`)
- Converter documentos para PDF (imagens, DOCX, XLSX, ODS, PPTX, HTML, TXT)
- Comprimir PDFs resultantes com ghostscript ou pikepdf (nível: printer)
- Agrupar imagens de conjunto (frente/verso, páginas de um todo) em PDF único antes de converter
- Nomear arquivos no padrão `TIPO-SUJEITO-DATA[.DISCRIMINANTE].pdf`
- Interpretar nome anterior, caminho de origem e conteúdo para determinar TIPO, SUJEITO e DATA
- Preservar cópia original em `_APAGAR/__ORIGINAIS__/` antes de qualquer alteração
- Mover duplicatas para `_APAGAR/duplicidade/`
- Mover lixo e irrecuperáveis para `_APAGAR/lixo/`
- Organizar arquivos em subpastas substantivas por afinidade
- Gerar `RESUMO.DOCX`, `ACESSOS.TXT` e `ASTREA.TXT` na raiz
- Renomear a pasta raiz no padrão Astrea ao final

**NÃO FAÇO:**
- Abrir, editar ou assinar documentos
- Enviar arquivos para sistemas externos
- Criar peças processuais → delego para skills C5
- Organizar pastas que não sejam de cliente jurídico → uso geral não é escopo

**DELEGO PARA:**
- `mod4` — se for necessário gerar DOCX formatado a partir do conteúdo
- `juridir` não encadeia automaticamente outras skills

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Pedido de organização | "organize a pasta do cliente X", "arrumar essa bagunça" |
| Padronização | "padronizar nomes", "renomear arquivos", "padrão canônico" |
| Duplicidade | "achar duplicatas", "tem arquivos repetidos" |
| Lote documental | "recebi holerites/CNIS/laudos do cliente novo" |
| Reprocessamento | "apareceram arquivos novos, reprocessa" |

**NÃO disparo quando:** o pedido é criar peça processual (→ skills C5) ou formatar DOCX (→ mod4).

---

## §3 — Padrão de nomeação: TIPO-SUJEITO-DATA

### Formato canônico

```
TIPO-SUJEITO-DATA[.DISCRIMINANTE].pdf
```

- **TIPO:** 2–4 caracteres maiúsculos, vocabulário fechado em `ASSETS/tipos.csv`
  (ex: `RG`, `CNIS`, `HOL`, `LAU`, `CT`, `PT`, `SENT`, `REC`, `BOL`)
- **SUJEITO:** primeirome + últimosobrenome, sem acento, 6–12 chars, sem hífen interno
  (ex: `MARIASOUZA`, `JOAOPINTO`)
- **DATA:** `AAAAMMDD` do documento; se desconhecida, `AAAAMMXX` (mês) ou `AAAAXXXX` (ano)
  (ex: `20240315`, `202403XX`, `2024XXXX`)
- **DISCRIMINANTE:** apenas quando necessário para distinguir arquivos do mesmo TIPO+SUJEITO+DATA:
  `[FACE]-[NPROC]-[STATUS]-[VNN]`
- **Charset:** apenas A-Z, 0-9 e hífen. Sem underscore fora de `_APAGAR/`. Sem acento. Sem espaço.

### Inferência semântica do nome

Antes de usar qualquer pipeline de OCR ou visão, a skill interpreta o arquivo por quatro
dimensões simultâneas e independentes:

1. **Nome anterior literal:** siglas, padrões regex, números de processo, datas embutidas
   (`wpp_2024-03-15_123.jpg` → DATA=20240315; `CPF_123456789.pdf` → provável identificação)
2. **Nome anterior semântico:** o que o nome sugere funcionalmente, mesmo em abreviação
   informal (`laudo-joao-costas.pdf` → LAU; `contra-cheque-marco.pdf` → HOL)
3. **Caminho de origem:** pasta-mãe, hierarquia de diretórios, nome do projeto
   (`cliente/maria-silva/medico/` → SUJEITO=MARIASOUZA; `exames/2023/` → período provável)
4. **Conteúdo:** OCR de cabeçalho, visão multimodal, padrões estruturais internos

As quatro dimensões são ponderadas em conjunto. Nenhuma sozinha é definitiva. Conflito entre
dimensões é resolvido pela mais confiável para aquele campo específico: DATA geralmente vem do
conteúdo; SUJEITO geralmente vem do caminho ou nome; TIPO geralmente vem do conteúdo ou nome
semântico.

---

## §4 — Conversão e compressão de PDF

### Conversão para PDF

Todo arquivo que não for PDF nativo é convertido antes de ser nomeado e movido. Ordem de
preferência de conversão:

| Formato de origem | Ferramenta preferida | Fallback |
|---|---|---|
| JPG, PNG, TIFF, BMP, WEBP | Pillow → PDF | img2pdf |
| DOCX, ODT | LibreOffice headless | python-docx → HTML → PDF |
| XLSX, ODS | LibreOffice headless | openpyxl → HTML → PDF |
| HTML | weasyprint | wkhtmltopdf |
| TXT | reportlab | pandoc |
| Áudio (MP3, M4A, OGG) | whisper → TXT → PDF | sem conversão |

Fotos genuinamente não-documentais (imagem de lesão, foto de residência, selfie) ficam como
JPG com tipo `FO`.

### Agrupamento de imagens de conjunto

Antes de converter individualmente, a skill detecta conjuntos de imagens que formam um todo:

- **Frente/verso:** mesmo SUJEITO + TIPO + DATA + padrão de nome (`_F`/`_V`, `front`/`back`,
  `frente`/`verso`, sequência numérica com ≤ 2 arquivos)
- **Páginas de documento:** mesmo SUJEITO + TIPO + DATA + sequência numérica (`_01`, `_02`…)
  ou timestamps próximos (< 5 min) de câmera
- **Lote de WhatsApp:** arquivos com prefixo `wpp_`/`IMG-`/`IMG_` + timestamp sequencial
  + mesmo remetente inferido

Imagens detectadas como conjunto são agrupadas em PDF único com páginas na ordem inferida
antes de qualquer conversão individual. O agrupamento é registrado no log com a lista de
arquivos-fonte.

### Compressão de PDF

Todo PDF (nativo ou convertido) é comprimido após a nomeação. Ferramenta: ghostscript
(`-dPDFSETTINGS=/printer`). Fallback: pikepdf com compressão de fluxo. A compressão é
aplicada apenas se reduzir o tamanho em ≥ 10%; caso contrário, o arquivo não é substituído.
O original pré-compressão já está em `_APAGAR/__ORIGINAIS__/` por força de R3.

---

## §5 — Estrutura de preservação _APAGAR

```
_APAGAR/
├── __ORIGINAIS__/     cópias dos arquivos antes de renomear/converter/comprimir
│   └── [nome-original-intacto]
├── duplicidade/       arquivos com conteúdo idêntico (hash SHA-256) a outro já processado
│   └── [nome-original]
└── lixo/              lixo de sistema, corrompidos, irrecuperáveis, inúteis ao caso
    └── [nome-original]
```

**Regra de precedência:** se um arquivo é duplicata E precisa ser convertido, vai para
`duplicidade/` sem conversão — não é necessário converter o que não vai ser usado.

---

## §6 — Ordem de execução

**Fase 1 — Inventário e triagem barata.**
Hash SHA-256 de todos os arquivos. Detecção de lixo de sistema (`ASSETS/lixo_sistema.csv`).
Detecção de duplicatas (hash exato → `_APAGAR/duplicidade/`). Classificação por sinais
externos baratos (regex sobre nome, extensão, EXIF, metadado). Arquivos já no padrão
canônico pulam a Fase 2.

**Fase 2 — Compreensão profunda.**
Inferência de SUJEITO pelo caminho e nome anterior (§3 — 4 dimensões). OCR superficial
(cabeçalho e primeira página). Visão multimodal para imagens com confiança baixa. OCR
profundo e extração estruturada para CNIS, holerite, sentença, laudo, RG. Cache em
`~/.juridir-cache/ocr/` e `~/.juridir-cache/visao/` por hash.

**Fase 3 — Agrupamento de conjuntos de imagens.**
Detecção de frente/verso, páginas, lotes WhatsApp (§4 — Agrupamento). Geração de PDF único
por conjunto. Registro dos arquivos-fonte no log. Originais das imagens individuais → R3
(`_APAGAR/__ORIGINAIS__/`).

**Fase 4 — Conversão, nomeação e compressão.**
Para cada arquivo (ou PDF de conjunto): (a) R3 — cópia em `_APAGAR/__ORIGINAIS__/`; (b)
conversão para PDF se necessário; (c) nomeação canônica TIPO-SUJEITO-DATA; (d) compressão
se ganho ≥ 10%.

**Fase 5 — Organização em subpastas.**
Árvore de afinidade (`ASSETS/arvore_afinidade.csv`) aplicada. Máximo 10 subpastas por
nível; excedente funde o par mais afim. Subpasta de processo: `NUMEROCNJ-MATERIA-TEMA`.

**Fase 6 — Geração de artefatos.**
`RESUMO.DOCX` (síntese do caso + seção VII Cadastro Astrea), `ACESSOS.TXT` (senhas, logins,
números) e `ASTREA.TXT` (campos prontos para colar) na raiz. Artefatos técnicos
(caso.json, log.csv) em `~/.juridir-cache/execucoes/`. Diretórios vazios removidos.
Pasta raiz renomeada para padrão Astrea: `NOME SOBRENOME - TIPO - DIREITO - TEMA` (máx. 80 chars).

---

## §7 — Cascata de classificação (princípio de autonomia)

A skill não devolve pendência sem esgotar a cascata:

1. Sinais externos baratos (regex no nome, extensão, EXIF)
2. Inferência semântica das 4 dimensões (§3)
3. OCR superficial (cabeçalho, primeira página)
4. Análise estrutural (layout característico por TIPO)
5. OCR profundo (páginas internas)
6. Visão multimodal (imagens não-documentais ou baixa confiança)
7. Comparação cruzada com outros arquivos da pasta (contexto resolve ambíguos)
8. Decisão por melhor hipótese, com motivo e confiança registrados no log

---

## §8 — Estado final da pasta

```
NOME SOBRENOME - TIPO - DIREITO - TEMA/
├── RESUMO.DOCX
├── ACESSOS.TXT
├── ASTREA.TXT
├── [SUBPASTAS-SUBSTANTIVAS]/
│   └── TIPO-SUJEITO-DATA[.DISCRIMINANTE].pdf
└── _APAGAR/
    ├── __ORIGINAIS__/
    ├── duplicidade/
    └── lixo/
```

Sem prefixos numéricos. Sem pastas técnicas na raiz. Sem underscore fora de `_APAGAR/`.

---

## §9 — Dependências

```
python-docx    geração de RESUMO.DOCX
pypdf          leitura de PDF nativo
pikepdf        compressão de PDF (fallback)
ghostscript    compressão de PDF (preferido)
Pillow         agrupamento e conversão de imagens
img2pdf        conversão de imagem para PDF (fallback)
LibreOffice    conversão de DOCX/XLSX para PDF
ocrmypdf       OCR de PDF imagem
tesseract-ocr  OCR de imagens (idioma 'por' obrigatório)
weasyprint     conversão HTML → PDF
reportlab      conversão TXT → PDF
ffprobe        duração de áudio/vídeo (opcional)
openai-whisper transcrição local de áudio (opcional; modelo large-v3)
anthropic      visão multimodal (opcional; sem ANTHROPIC_API_KEY degrada para FO genérico)
```

---

## §10 — Casos-teste

**Positivos:**
1. Pasta com `IMG_001.jpg`, `IMG_002.jpg` (frente/verso de RG) + `holerite-marco-2024.pdf` →
   agrupa imagens em `RG-MARIASOUZA-20240315.pdf`, renomeia holerite para
   `HOL-MARIASOUZA-202403XX.pdf`, comprime ambos, copia originais em `_APAGAR/__ORIGINAIS__/`.
2. Pasta com `laudo-joao-costas.pdf` e cópia idêntica `laudo-joao-costas (1).pdf` →
   processa o primeiro, move duplicata para `_APAGAR/duplicidade/` sem reprocessar.
3. Pasta com `wpp_2024-03-10_001.jpg` a `wpp_2024-03-10_008.jpg` do mesmo remetente →
   detecta lote WhatsApp, agrupa em PDF único `APRE-MARIASOUZA-20240310.pdf`.

**Negativos:**
1. Pedido de criar petição a partir dos documentos organizados → recusa, redireciona para
   skill C5 correspondente.
2. Pasta de fotos pessoais sem relação com processo jurídico → sinaliza escopo inadequado
   e aguarda confirmação antes de processar.

---

## §11 — Configuração

`config.yaml` na raiz da skill ou `~/.juridir/config.yaml`. Flags de execução:
- `--dry-run`: simula sem mover arquivos
- `--sem-visao`: desliga visão multimodal
- `--sem-ocr`: classifica apenas por sinais externos
- `--sem-compressao`: pula etapa de compressão de PDF

Diagnóstico de ambiente impresso no início: `verificar_ambiente()` mostra explicitamente o
que está degradado e a consequência operacional. Sem `ANTHROPIC_API_KEY`, imagens caem em
fallback `FO` em vez de serem lidas como documento.

---

## Status

**Instalado:** 2026-05-11
**Versão:** 2.0.0
**Última auditoria:** 2026-05-11
**Próxima auditoria:** 2026-08-09
