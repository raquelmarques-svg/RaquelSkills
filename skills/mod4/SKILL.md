---
name: mod4
description: |
  Ativa com o comando explícito "mod4". Nunca ativa por "petição", "manifestação", "recurso" ou "documento jurídico" sem o comando. Produz sempre .docx entregue via present_files — sem exceção, salvo comando explícito em contrário no mesmo turno.

  Gera documentos do escritório Almeida Marques em três camadas: (1) padrão gráfico — cabeçalho VML, Cambria, paleta navy/creme, assinatura cursiva, rodapé N/T; (2) estrutura obrigatória — seção "I. PRELIMINARES E REQUISITOS PROCESSUAIS" entre qualificação e fatos; (3) pipeline — zipfile direto sobre template_mod4.docx, substituição XML via word/document.xml, input por schema JSON.

  Escopo exclusivo: layout e estrutura do .docx. Conteúdo jurídico, revisão e honorários pertencem à skill revisao-previa-mod4, executada antes desta.
project: Proj02
nucleo: N1
frente: transversal
camada: C0
categoria: capability
justificativa: Produz arquivo .docx concreto entregue via present_files; não é preference porque gera output físico, não configura comportamento.
depends_on:
  - revisao-previa-mod4
chains_to:
  - present_files
frentes_consultadas:
  - transversal
recursos_compartilhados:
  assets:
    - ASSETS/template_mod4.docx
    - ASSETS/assinatura_raquel_almeida_marques.png
    - ASSETS/logo_almeida_marques.png
  scripts:
    - SCRIPTS/gerar_mod4_zipfile.py
  schemas:
    - SCHEMAS/mod4_input.schema.json
  config:
    - CONFIG/tipografia.json
  references:
    - references/01-pipeline.md
    - references/02-template.md
    - references/03-tipografia.md
    - references/04-paleta-elementos.md
    - references/05-licoes-mod4.md
licoes_aplicadas:
  - L1, L2, L3, L5, L6, L7, L8, L9, L22, L23, L24, LD1, LD2, LD3, LD4, LD5, LD6, LD7
regras_aplicaveis:
  - R1, R2, R3, R6, R9, R10, R11
verificado_em: 2026-05-14
version: 4.3.0
---

# mod4 — Padrão gráfico e estrutural do escritório

## §0 — Ativação e gates

Comando único: `mod4`. Sem gatilho implícito — nunca ativa por "petição", "manifestação", "recurso" ou equivalente sem o comando.

Pré-requisito obrigatório: o input deve ser o output de `revisao-previa-mod4`, identificável pelo bloco `Status: PRONTO PARA mod4`. Se ausente, executar `revisao-previa-mod4` antes de prosseguir.

Regra de saída inflexível: toda invocação produz `.docx` entregue via `present_files`. Pedir "peça curta", "teste" ou "rascunho" não dispensa o `.docx`. Exceção exige verbalização explícita no mesmo turno.

## §0 — Regras universais

R1 (exportação): o `.docx` principal não exige confirmação adicional — `mod4` já é a autorização. Arquivos adicionais (ZIP, PDF, relatório) exigem confirmação.

R2 (preservação): nunca apago arquivo. Itens removidos vão para `_APAGAR/NOME-YYYYMMDD-HHMMSS/` com caminho reportado.

R3 (backup): antes de modificar qualquer arquivo desta skill, copio para `_backups/mod4/ARQUIVO-YYYYMMDD-HHMMSS.ext`. Falha no backup = abortar.

R6 (adaptação): se algo no input não cabe no padrão, proponho ajuste antes de recusar. Decisão de descartar é da Raquel.

R9 (auditoria): participo do ciclo mensal de `governanca-skills`.

R10 (discordância útil): aponto inconsistência estrutural ou violação de padrão antes de gerar — nunca após.

R11 (economia de ação): uma invocação, um `.docx`. Não gero variantes sem pedido.

## §0 — Autopercepção (verificação leve pré-output)

Antes de gerar, verifico três pontos bloqueantes:

1. O input contém `Status: PRONTO PARA mod4`? Se não → executar `revisao-previa-mod4` primeiro.
2. Os campos obrigatórios do schema estão presentes (`enderecamento`, `qualificacao_autora`, `nome_acao`, `secoes`, `assinatura`)?
3. A seção PRELIMINARES está declarada como primeira entrada de `secoes[]`?

Se qualquer ponto falhar, sinalizo com o ponto específico e aguardo correção. Não prossigo com falha silenciosa.

## §1 — Escopo

FAÇO:
- Gerar `.docx` com padrão gráfico completo (cabeçalho VML, paleta, tipografia, assinatura, rodapé)
- Inserir seção PRELIMINARES obrigatória como primeira seção de mérito
- Normalizar tabelas e caixas de destaque conforme paleta navy/creme
- Entregar via `present_files`
- Aplicar patch no schema e no script quando tipos proibidos forem detectados no input

NÃO FAÇO:
- Redigir conteúdo jurídico → delego para skills C5
- Revisar texto ou verificar honorários → delego para `revisao-previa-mod4`
- Gerar `.docx` do zero via python-docx ou qualquer serializador → apenas zipfile direto sobre template (LD5)
- Usar `SCRIPTS/gerar_mod4.py` como intermediário → script descontinuado, inferior ao zipfile direto (L22)
- Incluir tutela de urgência → salvo pedido explícito no mesmo turno
- Usar caixas tipadas por função semântica → substituídas por `caixa_destaque` genérica

DELEGO PARA:
- `revisao-previa-mod4` — conteúdo, revisão, checklist pré-protocolo
- `present_files` — entrega do `.docx` gerado

## §2 — Paleta canônica

| Token | Hex | Uso exclusivo |
|---|---|---|
| Navy | `#2C3B44` | Títulos de seção, cabeçalhos de tabela, barra da caixa de destaque, bordas externas de tabela |
| Creme-claro | `#F5F1E8` | Fundo da caixa de destaque, zebra de linhas pares em tabelas |
| Creme | `#EEECE1` | Fundo de ementa de jurisprudência — exclusivo, nunca em corpo ou tabela comum |
| Cinza-texto | `#555555` | Rodapé |
| Cinza-linha | `#888888` | Linha superior do rodapé, paginação |
| Cinza-interno | `#CCCCCC` | Linhas internas de tabela |
| Corpo | `#222222` | Texto de corpo |
| Quase-preto | `#111111` | Endereçamento, nome da ação, títulos primários |

Regra absoluta: nenhuma cor fora desta paleta. Elementos de cor não excecem 5% da área útil total.

Ver detalhamento em `references/04-paleta-elementos.md`.

## §3 — Pipeline operacional (zipfile direto — método padrão)

**Método padrão desde v4.3.0 (L22):** manipulação direta do `word/document.xml` via `zipfile.ZipFile` sobre `ASSETS/template_mod4.docx`. Nunca usar `gerar_mod4.py` — o script adiciona camada desnecessária que produz resultado inferior e arrisca perda de VML, imagens e estilos calibrados.

Sequência obrigatória em toda invocação:

```
1. Verificar §0-Autopercepção (3 pontos bloqueantes)
2. Localizar template:
     find /mnt/skills -name "template_mod4.docx" 2>/dev/null
3. Copiar template para /tmp/output_work.docx
4. Abrir como zipfile; extrair todos os arquivos como dict {nome: bytes}
5. Decodificar word/document.xml com UTF-8
6. Aplicar substituições XML conforme §3-A (regras LD6 e LD7)
7. Recodificar word/document.xml como UTF-8
8. Remontar ZIP: iterar dict, substituir apenas word/document.xml,
   manter todos os demais arquivos byte a byte
9. Gravar resultado no destino final
10. Verificar checklist §7 (12 pontos)
11. present_files [caminho/destino/nome-descritivo.docx]
```

Script de referência: `SCRIPTS/gerar_mod4_zipfile.py`. Ver detalhes técnicos em `references/05-licoes-mod4.md`.

### §3-A — Regras de substituição XML (LD7 + LD6)

**LD7 — Padrão `>texto<` em vez da tag completa:**
```python
# CORRETO — casa com <w:t>X</w:t> e <w:t xml:space="preserve">X</w:t>
doc = doc.replace('>PLACEHOLDER<', '>valor_final<')

# ERRADO — falha silenciosamente quando ha xml:space="preserve"
doc = doc.replace('<w:t>PLACEHOLDER</w:t>', '<w:t>valor_final</w:t>')
```

**LD6 — Placeholders intermediários em substituições encadeadas (3+ elos):**
```python
# Passo 1: substituir origens por tokens unicos
doc = doc.replace('>Fevereiro/2026<', '>__MESA__<')
doc = doc.replace('>Marco/2026<',     '>__MESB__<')
# Passo 2: aplicar destinos sem conflito
doc = doc.replace('>Abril/2026<',     '>Maio/2026<')
# Passo 3: resolver tokens
doc = doc.replace('>__MESB__<',       '>Abril/2026<')
doc = doc.replace('>__MESA__<',       '>Marco/2026<')
```

Token padrao: `>__NOME_TOKEN__<` — underscores duplos + maiusculas = nao-colisao com XML valido.

## §4 — Estrutura obrigatória do documento

```
1.  Endereçamento
2.  Tribunal/localização (opcional)
3.  Caixa do processo (opcional)
4.  Qualificação da autora
5.  Nome da ação  ← estilo Ttulo1
6.  Subtítulo da ação (opcional)
7.  Qualificação do réu (opcional)
─────────────────────────────────────
8.  [OBRIGATÓRIO] I. PRELIMINARES E REQUISITOS PROCESSUAIS  ← Ttulo2
─────────────────────────────────────
9.  Seções de mérito (secoes[1..N])  ← estilo Ttulo2
10. DOS PEDIDOS
11. Valor da causa (opcional)
12. Fecho hardcoded
13. Data
14. Bloco de assinatura  ← "Almeida Marques Advocacia e Consultoria" (LD4)
```

PRELIMINARES devem ser declaradas como primeira entrada de `secoes[]`. Se ausentes, o script as insere automaticamente com conteúdo mínimo.

**Remissão probatória:** `(cf. **[nome do documento]**, doc. [N], [fl. X-Y] ou [p. X-Y do PDF])`

## §5 — Regras tipográficas críticas

Fonte única: Cambria em todos os níveis.

**Herança do estilo Normal (LD1):** firstLine=709, jc=both, sz=24 vêm do template. Parágrafos de corpo não repetem esses atributos. Script emite apenas `<w:spacing>` quando necessário.

Exceções que exigem atributos explícitos: tabelas, endereçamento (`jc=center`, `sz=28`), citação recuada.

**Estilos nativos obrigatórios:**
- `Ttulo1` → nome da ação
- `Ttulo2` → títulos de seção numerados
- `Ttulo3` → subseções
- `PargrafodaLista` → enumerações (LD3)
- `Normal` → corpo corrido

**Proibições absolutas:** sublinhado, travessão intercalador, bullets Unicode manuais, cores fora da paleta §2.

## §6 — Calibração

VERIFICAR VIGÊNCIA: SM 2026 = R$ 1.621,00.

VERIFICAR EXISTÊNCIA: `ASSETS/template_mod4.docx` acessível. `SCRIPTS/gerar_mod4_zipfile.py` presente. O script `gerar_mod4.py` está descontinuado — não usar mesmo que presente (L22).

VERIFICAR NOME DA FIRMA (LD4): "Almeida Marques Advocacia e Consultoria" no template. Divergência exige correção no arquivo físico, não no script.

VERIFICAR ESTILO NORMAL: `firstLine=709` no styles.xml do template. Divergência exige atualização do template.

## §7 — Auto-verificação

Última verificação: 2026-05-14 | Próxima: 2026-08-14

Checklist pós-geração (12 pontos):
- [ ] DOCX gravado e acessível (tamanho > 100KB)
- [ ] Cabeçalho VML visível em todas as páginas
- [ ] Assinatura cursiva presente e posicionada sobre nome/OAB
- [ ] Firma = "Almeida Marques Advocacia e Consultoria" (LD4)
- [ ] Rodapé ausente na 1ª página; N/T da 2ª em diante
- [ ] PRELIMINARES como primeira seção de mérito
- [ ] Títulos de seção com estilo Ttulo2 — nenhum bold/navy manual (LD1)
- [ ] Parágrafos de corpo sem firstLine, jc ou sz hardcoded (LD1)
- [ ] Enumerações com 3+ itens em PargrafodaLista, marcador numérico (LD3)
- [ ] Nenhuma cor fora da paleta §2
- [ ] Nenhum travessão intercalador, sublinhado ou bullet Unicode
- [ ] Acentuação completa — verificar visualmente antes de entregar

Checklist V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em <= 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §0-Autopercepção com 3 pontos bloqueantes
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA
- [x] Pipeline §3 com zipfile direto (L22, LD5)
- [x] §3-A com LD6 + LD7 documentados
- [x] §8 com LD5, LD6, LD7 (L22, L23, L24)
- [x] references/05-licoes-mod4.md declarada
- [x] Volume <= 500 linhas

## §8 — Lições incorporadas

L1 — Paths só são confiáveis em ambiente real. Aplico: `find` antes de cada geração.
L2 — Skill que mistura escopo infla. Aplico: §1 com FAÇO/NÃO FAÇO/DELEGO PARA.
L3 — Regras fortes são universais. Aplico: R1-R11 em §0 sem condicionais frágeis.
L5 — Andaime invisível. Aplico: nenhuma referência a método interno no output.
L6 — Versão instalada != entregue. Aplico: output sempre via `present_files`.
L7 — Encadeamento condicional sob comando. Aplico: `revisao-previa-mod4` é gate.
L8 — Skill ambiente-consciente. Aplico: script usa template como fonte única.
L9 — Python 3 é nativamente UTF-8. Aplico: nunca omitir acentos. Verificação visual obrigatória.

LD1 — Atributos de corpo herdados do Normal, nunca hardcodados. firstLine=709, jc=both, sz=24 vêm do template.
**Por quê:** MANDSEG v5 (12/05/2026) — hardcodar 720 sobrepõe o template.
**Como aplicar:** `bpara()` emite apenas `<w:spacing>`.

LD2 — Títulos de seção usam estilo nativo Ttulo2, nunca formatação manual.
**Por quê:** revisão da Raquel (12/05/2026) migrou todos os títulos para Ttulo2.
**Como aplicar:** `heading2()` usa `<w:pStyle w:val="Ttulo2"/>` sem atributos adicionais.

LD3 — Enumerações de 3+ itens usam PargrafodaLista com marcador numérico entre parênteses.
**Por quê:** revisão da Raquel (12/05/2026) converteu todos os blocos inline e extensos.
**Como aplicar:** `list_para()` usa `<w:pStyle w:val="PargrafodaLista"/>`.

LD4 — Nome comercial da firma é "Almeida Marques Advocacia e Consultoria".
**Por quê:** revisão da Raquel (12/05/2026) corrigiu "Sociedade Individual de Advocacia".
**Como aplicar:** verificar e corrigir no template físico.

LD5 — Zipfile direto sobre `template_mod4.docx` é o método padrão e permanente. Nunca usar `gerar_mod4.py`.
**Por quê:** L22 (14/05/2026) — redesprotocolamento Beatriz Rodrigues comprovou que zipfile direto preserva 100% dos elementos gráficos. Script intermediário é camada desnecessária com risco de perda de VML, imagens e estilos.
**Como aplicar:** copiar template → abrir zipfile → modificar apenas `word/document.xml` → remontar ZIP. Script: `SCRIPTS/gerar_mod4_zipfile.py`.

LD6 — Em substituições XML encadeadas (3+ elos), usar placeholders intermediários.
**Por quê:** L23 (14/05/2026) — `str.replace()` reprocessa textos recém-substituídos quando formam cadeia.
**Como aplicar:** tokens `>__TOKEN__<` na primeira passagem; resolver na segunda. Ver §3-A.

LD7 — Em toda substituição de conteúdo textual em `document.xml`, usar `>texto<` como padrão de busca.
**Por quê:** L24 (14/05/2026) — o Word gera `<w:t>X</w:t>` e `<w:t xml:space="preserve">X</w:t>`. Busca pela tag completa falha silenciosamente na segunda forma.
**Como aplicar:** `doc.replace('>TEXTO_ALVO<', '>TEXTO_NOVO<')` casa com ambas as formas. Ver §3-A.

## §9 — Pipeline pós-atualização (sincronização Git)

```powershell
$skill = "mod4"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$bk = "C:\RaquelSkills\_backups\$skill"
New-Item -ItemType Directory -Force -Path $bk | Out-Null
Copy-Item "C:\RaquelSkills\skills\$skill\SKILL.md" "$bk\SKILL-$ts.md" -ErrorAction SilentlyContinue

Expand-Archive -Path "$env:USERPROFILE\Downloads\mod4.skill" `
               -DestinationPath "C:\RaquelSkills\skills\" -Force

Set-Location C:\RaquelSkills
Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
git add "skills/mod4/"
git commit -m "feat(mod4): v4.3.0 — L22 zipfile direto, L23 placeholders, L24 >text< pattern"
git push
```
