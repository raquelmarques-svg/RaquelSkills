# Lições L1-L11 — acúmulo da biblioteca Almeida Marques

Lições aprendidas em sessões reais de criação, refatoração e debug. Divididas em universais (aplicáveis a toda skill) e mod4-específicas (técnicas de DOCX corporativo).

## Lições universais

### L1 — Bugs de path só aparecem em ambiente real

Problema: skill testada em sandbox funciona; em Cowork local, quebra por caminhos absolutos ou separadores incompatíveis (`/` vs `\\`).

Aplicação: usar `pathlib.Path`, caminhos relativos, variável `RAQUEL_SKILLS_ROOT`, `resolver_output_root.py` para detecção de ambiente.

Aplica em: toda skill que escreve arquivos.

### L2 — Skill que mistura escopo, infla

Problema: skill começa com função A, ganha B "porque é parecido", depois C. Resultado: 700+ linhas, descrição confusa, gatilhos ambíguos.

Aplicação: §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito desde a primeira versão. Recusar adições que extrapolam escopo. Sugerir skill nova.

Aplica em: toda skill, sempre.

### L3 — Regras "fortes" são universais, não condicionais

Problema: cláusulas condicionais ("se cliente for X, então R1"). Resultado: ambiguidade, R1 violada em limites.

Aplicação: R1-R11 são universais ou não aplicam. Condicional é sintoma de cláusula mal formulada.

Aplica em: toda skill, sempre.

### L4 — Pergunta a cada turno > marcador textual

Problema: marcadores textuais ("Status: PRONTO") não controlam fluxo real de execução.

Aplicação: perguntas explícitas em vez de marcadores. Estado em frontmatter YAML. Bifurcações são perguntas, não inferências.

Aplica em: skills que pedem confirmação, encadeamento ou bifurcação.

### L5 — Andaime invisível

Problema: método de redação (Save the Cat, 3 atos) aparece no output. Resultado: peça processual com vocabulário ficcional.

Aplicação: métodos ficam no raciocínio interno, nunca no output. Vocabulário canônico jurídico sempre.

Aplica em: skills que produzem texto.

### L6 — Versão instalada ≠ versão entregue

Problema: versão local diverge silenciosamente da que Claude lê em sandbox.

Aplicação: versionamento semântico MAJOR.MINOR.PATCH no frontmatter. Sincronia R8 reduz drift. Log registra versão usada.

Aplica em: toda skill com versionamento.

### L7 — Encadeamento condicional sob comando

Problema: `chains_to` executado automaticamente. Cadeia explode em casos não desejados.

Aplicação: `chains_to` declara capacidade, não dispara automaticamente. Perguntar antes de encadear (L4).

Aplica em: skills que chamam outras.

### L8 — Skill ambiente-consciente

Problema: skill funciona em Claude.ai, quebra em Cowork por diretórios diferentes.

Aplicação: `resolver_output_root.py` detecta ambiente. Sandbox: `/mnt/user-data/outputs/`. Cowork: relativo a `RAQUEL_SKILLS_ROOT`.

Aplica em: toda skill que escreve arquivos.

### L9 — Python 3 é nativamente UTF-8; nunca omitir acentos

Problema: strings Python sem acento "por precaução" produzem DOCX com "Excelentissimo" e "Sao Paulo". Erro silencioso — arquivo gerado, conteúdo ilegível profissionalmente.

Aplicação:
- Linha 1: `#!/usr/bin/env python3`
- Linha 2: `# -*- coding: utf-8 -*-`
- `encoding='utf-8'` explícito em todo `open()`, `read_text()`, `write_text()`
- `ET.tostring(doc, encoding='unicode')` para ElementTree
- Acentuação completa em todas as strings literais
- Verificação visual obrigatória: abrir o DOCX no Word antes de entregar

Aplica em: toda skill com scripts Python que geram texto ou arquivos.

### L10 — Skill sem artefatos é esqueleto

Problema: skill entregue apenas com SKILL.md. Claude inventa conteúdo na hora do uso, gerando inconsistência entre sessões.

Aplicação:
- MODELOS/ obrigatório quando skill produz texto jurídico estruturado
- ASSETS/ obrigatório quando skill usa normas, cálculos ou checklists
- SCHEMAS/ obrigatório quando skill recebe input com 5+ campos
- Cada modelo com ≥ 70% de conteúdo pronto (placeholder ≤ 30%)
- Pasta declarada em `recursos_compartilhados` mas vazia = falha bloqueante auditoria A13

Aplica em: toda skill que produz texto jurídico ou recebe input estruturado.

### L11 — Git sync é parte do pipeline, não etapa manual

Problema: skill gerada e empacotada mas não commitada. Próxima sessão Cowork não encontra versão nova. Drift silencioso entre web, Cowork e GitHub.

Aplicação:
- §4-G executa backup R3 + extração + commit + push imediatamente após empacotamento
- Skill não está "entregue" sem hash de commit confirmado
- Mensagem canônica: `feat(<nome>): v<versão> — <resumo>`
- `index.lock` bloqueante: `Remove-Item ".git\index.lock" -Force` antes do commit
- Verificar `git status` após push: repositório limpo = entrega concluída

Aplica em: toda skill criada ou modificada.

---

## Lições mod4-específicas (DOCX corporativo)

Aplicam-se apenas à mod4 e skills que produzem DOCX corporativo com template VML.

### LM1 — Pipeline zipfile sobre template (não from-scratch)

Problema: DOCX gerado from-scratch não tem formatação corporativa.

Aplicação: usar `template_mod4.docx` como base, manipular via `zipfile`, nunca `python-docx` do zero quando há template.

Aplica em: mod4 e skills com DOCX corporativo.

### LM2 — Letterhead VML: position:absolute, z-index:-251657728

Problema: marca d'água incorretamente posicionada quebra layout.

Aplicação: VML com `position:absolute` e `z-index:-251657728`. Três headers separados. `<w:titlePage/>` no sectPr.

Aplica em: mod4 apenas.

---

## Tabela de aplicabilidade

| Lição | Aplica em |
|---|---|
| L1 | Skills que escrevem arquivos |
| L2 | Toda skill |
| L3 | Toda skill |
| L4 | Skills que pedem confirmação ou encadeiam |
| L5 | Skills que produzem texto |
| L6 | Skills com versionamento |
| L7 | Skills que chamam outras |
| L8 | Skills que escrevem arquivos |
| L9 | Skills com scripts Python |
| L10 | Skills que produzem texto jurídico ou recebem input estruturado |
| L11 | Toda skill criada ou modificada |
| LM1 | mod4 e skills com DOCX corporativo |
| LM2 | mod4 apenas |

---

## Adição de lições futuras (L12+)

1. Capturar via `gotcha-skill` com caso concreto
2. Validar em 3 ocorrências reais
3. Adicionar aqui com formato: Problema → Aplicação → Aplica em
4. Atualizar tabela de aplicabilidade
5. Atualizar references 02 e 04
6. Aplicar retroativamente via modo Govern

### L12 — Escopo misto é o erro mais caro

Problema: skill criada com funções em camadas distintas (ex: análise C4 + geração visual C0 + extração C3). Não falha ruidosamente na criação — falha silenciosamente em produção: ativa quando não deveria, produz output inconsistente entre sessões, resiste a refatoração futura porque cada função tem dependências diferentes.

Sintomas de escopo misto:
- Gatilhos ambíguos que disparam em ≥ 3 contextos distintos
- R1 (confirmação de exportação) ocorre no meio do pipeline, não no início
- Skill tem "modo lite" e "modo completo" descritos no §1
- Scripts genéricos hardcoded que funcionariam em qualquer processo
- Assets (normas, SM histórico) que outras skills também precisariam
- Função visual (PNG, HTML, widget) misturada com função analítica (cálculo, classificação)

Aplicação:
- V8 em todo modo operacional: Create, Edit, Govern, Refactor, Diagnóstico
- V8 nunca é pulada mesmo quando o pedido parece óbvio
- Custo de split tardio é 5× maior que split na criação
- Quando V8 reprova: nomear as skills resultantes antes de criar qualquer uma

Aplica em: toda operação da skill-creator-am, sem exceção.
