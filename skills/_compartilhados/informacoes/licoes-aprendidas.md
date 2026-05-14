# Lições Aprendidas — Biblioteca Almeida Marques

Formato: L[N] · data · contexto · regra · como aplicar
Gerenciado por: gotcha-skill (appenda ao final)
Lido por: skill-creator-am (antes de Create/Edit), gotcha-skill (deduplicação)

---

## L1 · mai/2026 · widget-visual
Output mudou de PNG (matplotlib) para show_widget exclusivo. gerar_widget.py produz resultado inferior — bitmap sem antialiasing, sem webfonts, sem hierarquia visual.
**Regra:** nunca usar gerar_widget.py em sessões interativas. Usar mcp__visualize__show_widget com HTML.
**Exceção:** html_para_imagem.py apenas em pipeline automatizado sem browser.

## L2 · mai/2026 · widget-visual
Dimensões canônicas: 567px × 340px (≈15cm × 9cm). Excesso → redesenhar priorizando carga decisória, depois quebrar em W1/W2/W3. Nunca comprimir fonte abaixo de 10px.
**Como aplicar:** avaliar altura estimada antes de renderizar; se exceder, suprimir acessório antes de quebrar.

## L3 · mai/2026 · widget-visual
Estilo extravagante tem parâmetros aprovados: full-bleed backgrounds, números 42–52px, ícones Tabler, split panels 4px, badges border-radius 20px, dourado #FFD700 em fundos escuros.
**Paleta estendida:** crimson #7B1010, floresta #0F3D2E.

## L4 · mai/2026 · git / PowerShell
PowerShell 5 Expand-Archive rejeita extensão .skill com InvalidArgument IOException.
**Regra:** antes de extrair .skill, copiar com novo nome .zip; extrair; remover .zip temp.
**Comando:** `Copy-Item arquivo.skill arquivo-temp.zip; Expand-Archive arquivo-temp.zip -DestinationPath destino -Force; Remove-Item arquivo-temp.zip`

## L5 · mai/2026 · git
HEAD.lock órfão bloqueia git commit após processo travado.
**Regra:** `Remove-Item .git\HEAD.lock -Force` antes de retry. Erro: "Unable to create HEAD.lock: File exists."

## L6 · mai/2026 · git / PowerShell
Get-Content exibe UTF-8 como mojibake no terminal PowerShell padrão — cosmético. O arquivo no disco e no repositório está íntegro.
**Como verificar:** abrir no VSCode ou Notepad++ para confirmar encoding correto.

## L7 · mai/2026 · arquitetura de skills
Skills legacy (sem version/verificado_em) são negligentes em ITIL/COBIT/AAO. Duplicam conteúdo, contradizem comandos atuais, violam arquitetura V4.
**Regra:** refatorar antes de instalar. Nunca instalar .skill legacy diretamente.

## L8 · mai/2026 · _compartilhados/
_compartilhados/ estava referenciado em 6 skills de produção mas o diretório não existia. Broken references causam falhas silenciosas — a skill executa sem contrato.
**Regra:** verificar existência de todos os paths em recursos_compartilhados: antes de declarar skill como funcional.

## L9 · mai/2026 · arquitetura de componentes
padrao-redacional não é skill — é biblioteca (_compartilhados/). Instalar como skill cria risco de ativação com contexto vazio e sem pipeline útil.
**Regra:** conteúdo consumido por 3+ skills via depends_on vai em _compartilhados/, não como skill standalone.

## L10 · mai/2026 · arquitetura de skills
Bloco LEITURA+OUTPUT+ATUALIZAÇÃO estava duplicado em 13 skills (143 linhas de ruído idêntico).
**Regra:** comportamento transversal vai em _compartilhados/informacoes/comportamento-base.md, referenciado uma vez por skill via depends_on.

## L11 · mai/2026 · nomeação de skills
monitor-publicacoes: nome enganoso — conteúdo real é checklist pré-protocolo avançado (BLOCOs A–H de competência, foro, documentos, custas, gratuidade). check-representacao-trabalhista: nome enganoso — conteúdo real é protocolo de audiência CLT.
**Regra:** ao receber skill para instalar, ler §1 FAÇO/NÃO FAÇO. Nome não garante escopo.

## L12 · mai/2026 · versionamento
skill-creator-am em produção estava em v1.6.0; pacote uploaded era v1.4.0 — produção estava à frente do git.
**Regra:** verificar version em produção antes de aceitar qualquer pacote de atualização. `grep "^version:" SKILL.md` no arquivo instalado.

## L13 · mai/2026 · gotcha-skill
gotcha-skill falhou silenciosamente desde instalação — instruía appender em licoes-aprendidas.md que não existia.
**Regra:** ao instalar skill que declara depends_on com path em _compartilhados/, criar o arquivo referenciado antes ou imediatamente após a instalação.

---

## L22 — Sempre usar zipfile direto sobre template_mod4.docx — nunca depender de gerar_mod4.py

| Campo | Valor |
|---|---|
| skill_afetada | mod4 |
| categoria | dependência |
| descoberto_via | produção |
| data | 2026-05-14 |
| auditoria_ref | — |

**Comportamento inesperado:** O pipeline §3 do mod4 v4.2.0 referenciava `SCRIPTS/gerar_mod4.py` como método primário. O script intermediário introduz risco de perda do cabeçalho VML, das imagens e dos estilos calibrados do template.

**Causa raiz:** O script é uma camada desnecessária entre o JSON de input e o template DOCX. O zipfile direto acessa o template sem intermediário e preserva 100% dos elementos gráficos.

**Correção aplicada:** Zipfile direto sobre `ASSETS/template_mod4.docx` é o método padrão permanente a partir da v4.3.0. O resultado visual é superior ao gerado pelo script — cabeçalho VML, assinatura cursiva, paleta e tipografia intactos. Comprovou-se no redesprotocolamento do caso Beatriz Rodrigues (14/05/2026).

**Regra derivada:** Sempre manipular `word/document.xml` via `zipfile.ZipFile` diretamente sobre o template. Nunca usar `gerar_mod4.py` como intermediário — o script está descontinuado. Copiar o template para `/tmp/`, extrair todos os arquivos como dict, substituir apenas `word/document.xml`, remontar o ZIP.

**Remissões:** L1, L8 | LD5 | SCRIPTS/gerar_mod4_zipfile.py

---

## L23 — Usar placeholders intermediários em substituições XML em cascata

| Campo | Valor |
|---|---|
| skill_afetada | mod4 (geral — qualquer manipulação de document.xml) |
| categoria | output |
| descoberto_via | produção |
| data | 2026-05-14 |
| auditoria_ref | — |

**Comportamento inesperado:** Substituição sequencial de strings que formam cadeia (A→B, B→C, C→D) em documento XML produz dupla substituição: o texto recém-criado "B" é imediatamente reprocessado para "C" na etapa seguinte.

**Causa raiz:** `str.replace()` não distingue a origem da ocorrência; qualquer instância do padrão — inclusive as criadas na mesma execução — é afetada.

**Correção aplicada:** Placeholders únicos e não-colisionáveis (`>__MESA__<`, `>__MESB__<`, `>__DATA_A__<`) resolvem todas as substituições em bloco; os valores finais são restaurados em segunda passagem.

**Regra derivada:** Sempre que três ou mais substituições de texto XML formarem cadeia (valor de destino de uma é origem da próxima), usar placeholders intermediários na primeira passagem e resolver na segunda. Placeholders devem conter caracteres que não aparecem em XML válido (ex.: `>__TOKEN__<`).

**Remissões:** L9 | LD6 | references/05-licoes-mod4.md §LD6

---

## L24 — Substituir texto em `<w:t>` via padrão `>texto<`, nunca pela tag completa

| Campo | Valor |
|---|---|
| skill_afetada | mod4 (geral — qualquer manipulação de document.xml) |
| categoria | output |
| descoberto_via | produção |
| data | 2026-05-14 |
| auditoria_ref | — |

**Comportamento inesperado:** Substituição por `<w:t>texto</w:t>` falha silenciosamente quando a tag tem o atributo `xml:space="preserve"`, forma gerada pelo Word para textos com espaços iniciais ou finais.

**Causa raiz:** O Word gera duas formas do elemento: `<w:t>X</w:t>` e `<w:t xml:space="preserve">X</w:t>`. A busca pela tag completa sem atributo não casa com a segunda forma.

**Correção aplicada:** Usar `>X<` como padrão de busca casa com ambas as formas independentemente de atributos intermediários.

**Regra derivada:** Em qualquer substituição de conteúdo textual em `document.xml`, usar sempre `>texto_alvo<` como padrão de busca, nunca a tag completa `<w:t>texto_alvo</w:t>`. A forma curta é mais robusta e não produz misses silenciosos.

**Remissões:** L9, LD1 | LD7 | references/05-licoes-mod4.md §LD7
