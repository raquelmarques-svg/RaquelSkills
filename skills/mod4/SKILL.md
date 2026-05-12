---
name: mod4
description: |
  Ativa com o comando explícito "mod4". Nunca ativa por "petição", "manifestação", "recurso" ou "documento jurídico" sem o comando. Produz sempre .docx entregue via present_files — sem exceção, salvo comando explícito em contrário no mesmo turno.

  Gera documentos do escritório Almeida Marques em três camadas: (1) padrão gráfico — cabeçalho VML, Cambria, paleta navy/creme, assinatura cursiva, rodapé N/T; (2) estrutura obrigatória — seção "I. PRELIMINARES E REQUISITOS PROCESSUAIS" entre qualificação e fatos; (3) pipeline — script Python sobre template via zipfile, input por schema JSON.

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
    - SCRIPTS/gerar_mod4.py
    - SCRIPTS/validar_mod4.py
  schemas:
    - SCHEMAS/mod4_input.schema.json
  config:
    - CONFIG/tipografia.json
  references:
    - references/01-pipeline.md
    - references/02-template.md
    - references/03-tipografia.md
    - references/04-paleta-elementos.md
    - references/05-schema-input.md
licoes_aplicadas:
  - L1, L2, L3, L5, L6, L7, L8, L9, LD1, LD2, LD3, LD4
regras_aplicaveis:
  - R1, R2, R3, R6, R9, R10, R11
verificado_em: 2026-05-12
version: 4.2.0
---

# mod4 — Padrão gráfico e estrutural do escritório

## §0 — Ativação e gates

Comando único: `mod4`. Sem gatilho implícito — nunca ativa por "petição", "manifestação", "recurso" ou equivalente sem o comando.

Pré-requisito obrigatório: o input deve ser o output de `revisao-previa-mod4`, identificável pelo bloco `Status: PRONTO PARA mod4`. Se ausente, executar `revisao-previa-mod4` antes de prosseguir.

Regra de saída inflexível: toda invocação produz `.docx` em `/mnt/user-data/outputs/` entregue via `present_files`. Pedir "peça curta", "teste" ou "rascunho" não dispensa o `.docx`. Exceção exige verbalização explícita no mesmo turno.

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
- Executar validação via `validar_mod4.py` e reportar resultado
- Entregar via `present_files`
- Aplicar patch no schema e no script quando tipos proibidos forem detectados no input

NÃO FAÇO:
- Redigir conteúdo jurídico → delego para skills C5
- Revisar texto ou verificar honorários → delego para `revisao-previa-mod4`
- Gerar `.docx` do zero via python-docx ou qualquer serializador → apenas zipfile sobre template
- Incluir tutela de urgência → salvo pedido explícito no mesmo turno
- Usar caixas tipadas por função semântica (caixa_vicio, caixa_tese, caixa_advertencia, caixa_ressalva) → substituídas por `caixa_destaque` genérica

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

## §3 — Pipeline operacional

Sequência obrigatória em toda invocação:

```
1. Verificar §0-Autopercepção (3 pontos bloqueantes)
2. Construir /tmp/input.json conforme SCHEMAS/mod4_input.schema.json
3. Localizar template: find /mnt/skills -name "template_mod4.docx" 2>/dev/null
4. python3 SCRIPTS/gerar_mod4.py \
       --input /tmp/input.json \
       --output /tmp/output.docx \
       --template ASSETS/template_mod4.docx \
       --config CONFIG/tipografia.json
5. python3 SCRIPTS/validar_mod4.py /tmp/output.docx --json
6. Se status != "PRONTO": identificar causa, corrigir input, retornar ao passo 4
7. cp /tmp/output.docx /mnt/user-data/outputs/<nome-descritivo>.docx
8. present_files ["/mnt/user-data/outputs/<nome-descritivo>.docx"]
```

Proibido gerar o DOCX do zero via python-docx, docx-js ou qualquer serializador externo. O template contém cabeçalho VML e assinatura cursiva que não sobrevivem à serialização. Ver `references/01-pipeline.md` para detalhes técnicos completos.

## §4 — Estrutura obrigatória do documento

Ordem de montagem via `build_full_body` (hardcoded no script):

```
1.  Endereçamento
2.  Tribunal/localização (opcional)
3.  Caixa do processo (opcional)
4.  Qualificação da autora
5.  Nome da ação  ← estilo Ttulo1
6.  Subtítulo da ação (opcional)  ← LD2: seco, apenas o discriminante
7.  Qualificação do réu (opcional)
──────────────────────────────────────
8.  [OBRIGATÓRIO] I. PRELIMINARES E REQUISITOS PROCESSUAIS  ← estilo Ttulo2
──────────────────────────────────────
9.  Seções de mérito (secoes[1..N])  ← estilo Ttulo2 obrigatório (LD1)
10. DOS PEDIDOS
11. Valor da causa (opcional)
12. Fecho hardcoded
13. Data
14. Bloco de assinatura (copiado do template)  ← nome: "Almeida Marques Advocacia e Consultoria" (LD4)
```

**PRELIMINARES** devem ser declaradas como primeira entrada de `secoes[]` no JSON de input. Se ausentes, o script as insere automaticamente com conteúdo mínimo (representação, endereço para intimações, procuração). Se presentes mas fora de posição, o script corrige silenciosamente e reporta.

Conteúdo mínimo das PRELIMINARES: para ≤ 3 itens, parágrafos numerados. Para ≥ 4 itens, tabela de duas colunas (Item | Situação) com cabeçalho navy e zebra creme-claro.

**Epígrafe** (opcional): usar apenas quando contém resumo da lide, questão de fato ou questão de direito que agrega informação não coberta pela caixa_processo. Identificação pura de processo e partes — dispensar, pois a caixa_processo já a cobre. (LD2)

**Remissão probatória** — formato rígido em toda referência a documento:
`(cf. **[nome completo do documento]**, doc. [N], [fl. X–Y] ou [p. X–Y do PDF])`
Distinção: `fl.` para paginação do juízo pós-juntada; `p. do PDF` para paginação do arquivo pré-juntada.

## §5 — Regras tipográficas críticas

Fonte única: Cambria em todos os níveis. Ver tabela completa em `references/03-tipografia.md`.

**Herança do estilo Normal** (LD1): o template define o estilo Normal com `firstLine=709`, `jc=both`, `sz=24`. Parágrafos de corpo **não repetem** esses atributos no XML — herdam do Normal. O script deve emitir apenas `<w:spacing>` quando necessário. Hardcodar `firstLine`, `jc` ou `sz` em parágrafos de corpo sobrepõe o template e produz divergência visual.

Exceções que exigem atributos explícitos: tabelas e células (`firstLine=0`, `jc` conforme coluna), endereçamento (`jc=center`, `sz=28`), citação recuada (`w:ind w:left=720`, `firstLine=0`), rodapé.

**Estilos nativos obrigatórios** (LD1):
- `Ttulo1` → nome da ação (item 5 do §4)
- `Ttulo2` → títulos de seção numerados (I., II., III. etc.)
- `Ttulo3` → subseções quando necessário
- `PargrafodaLista` → toda enumeração de finalidades, fatos, dimensões jurídicas ou pedidos (LD3)
- `Normal` → corpo corrido

Nunca substituir esses estilos por formatação manual (bold + navy + sz=26 + jc=center). O estilo nativo carrega o espaçamento, a cor e a tipografia já calibrados no template.

**Enumerações** (LD3): qualquer sequência de itens com marcador — seja `(a)/(b)/(c)`, seja `(1)/(2)/(3)` — usa `PargrafodaLista`. O marcador usa número arábico entre parênteses, não extenso ("(1)", não "primeiro"). Inline com ponto e vírgula é proibido quando há três ou mais itens.

Proibições absolutas: sublinhado, travessão intercalador (—), bullets Unicode manuais (• ● ▪), cores fora da paleta §2. Negrito inline: máximo 2 ocorrências por página fora de títulos. Itálico: apenas termos estrangeiros, latinismos, títulos de obras, citações literais de documentos dos autos.

## §6 — Calibração

VERIFICAR VIGÊNCIA: SM 2026 = R$ 1.621,00. Teto RGPS e índices de correção: não hardcodar — verificar na data de referência do caso.

VERIFICAR EXISTÊNCIA: `ASSETS/template_mod4.docx` acessível. `SCRIPTS/gerar_mod4.py` e `validar_mod4.py` presentes. `CONFIG/tipografia.json` carregável. Se ausente qualquer um, abortar com sinalização clara.

VERIFICAR NOME DA FIRMA (LD4): o bloco de assinatura deve conter "Almeida Marques Advocacia e Consultoria". Se o template tiver "Sociedade Individual de Advocacia", corrigir no `ASSETS/template_mod4.docx` antes de qualquer geração — a correção pertence ao arquivo físico, não ao script.

VERIFICAR ESTILO NORMAL NO TEMPLATE: confirmar que `template_mod4.docx` tem `firstLine=709` no estilo Normal antes de qualquer alteração tipográfica. Valor divergente exige atualização do template, não do script.

DADO NECESSÁRIO: campos obrigatórios do schema + `data` para o bloco de assinatura. Sem `data`, o bloco de assinatura fica com `{{DATA}}` não substituído — reportar antes de gerar.

VERIFICAR NO tipografia.json: nunca alterar valores tipográficos diretamente no script. Editar apenas `CONFIG/tipografia.json` e regenerar. Protocolo: (1) identificar impacto, (2) backup R3 do JSON, (3) editar, (4) gerar, (5) validar.

## §7 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist pós-geração:
- [ ] `status == "PRONTO"` no output do validador
- [ ] Cabeçalho VML visível em todas as páginas
- [ ] Assinatura cursiva presente e posicionada sobre nome/OAB
- [ ] Firma = "Almeida Marques Advocacia e Consultoria" (LD4)
- [ ] Rodapé ausente na 1ª página; N/T da 2ª em diante
- [ ] PRELIMINARES como primeira seção de mérito
- [ ] Títulos de seção com estilo Ttulo2 — nenhum bold/navy manual (LD1)
- [ ] Parágrafos de corpo sem `firstLine`, `jc` ou `sz` hardcoded (LD1)
- [ ] Enumerações com 3+ itens em PargrafodaLista, marcador numérico (LD3)
- [ ] Nenhuma cor fora da paleta §2
- [ ] Nenhum travessão intercalador, sublinhado ou bullet Unicode no corpo
- [ ] Acentuação completa em todo o texto (ã, é, ç, ó, â, etc.) — abrir o DOCX e verificar visualmente antes de entregar

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §0-Autopercepção presente (3 pontos bloqueantes)
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] Paleta consolidada em §2 sem caixas tipadas
- [x] PRELIMINARES obrigatórias documentadas em §4
- [x] Pipeline operacional em §3 com sequência numerada
- [x] Herança do Normal documentada em §5 (LD1)
- [x] SM 2026 na Calibração §6
- [x] references/ declaradas no frontmatter
- [x] examples/ a gerar (3 positivos + 2 negativos)
- [x] Volume ≤ 500 linhas

## §8 — Lições incorporadas

L1 — Paths só são confiáveis em ambiente real. Aplico: `find /mnt/skills -name "template_mod4.docx"` antes de cada geração; nunca hardcodar path absoluto.

L2 — Skill que mistura escopo infla. Aplico: §1 com FAÇO/NÃO FAÇO/DELEGO PARA; conteúdo jurídico fora.

L3 — Regras fortes são universais. Aplico: R1-R11 em §0 sem condicionais frágeis.

L5 — Andaime invisível. Aplico: nenhuma referência a método interno na superfície do documento gerado.

L6 — Versão instalada ≠ entregue. Aplico: output sempre via `present_files`; nunca assumir que o arquivo chegou ao usuário sem a chamada.

L7 — Encadeamento condicional sob comando. Aplico: `chains_to` declarado; execução de `revisao-previa-mod4` é gate, não sugestão.

L8 — Skill ambiente-consciente. Aplico: script usa `CONFIG/tipografia.json` como fonte única; nenhum valor tipográfico hardcodado no SKILL.md ou no script.

L9 — Python 3 é nativamente UTF-8. Aplico: nunca omitir acentos em strings por precaução. O script declara `# -*- coding: utf-8 -*-` e lê/grava tudo com `encoding='utf-8'` explícito. Strings sem acento no JSON de input produzem DOCX errado. O JSON de input deve sempre usar acentuação completa (ã, é, ç, ó, â, etc.). Verificação visual pós-geração é obrigatória — abrir o DOCX no Word antes de entregar.

LD1 — Atributos de corpo herdados do Normal, nunca hardcodados. O estilo Normal do template define firstLine=709, jc=both, sz=24. Parágrafos de corpo que repetem esses valores no XML sobrepõem o template e produzem divergência visual quando o template for atualizado. O script deve emitir apenas `<w:spacing>` em parágrafos de corpo; os demais atributos são omitidos.
**Por quê:** verificado empiricamente no MANDSEG v5 (12/05/2026): Normal tem firstLine=709 no styles.xml. O §5 anterior hardcodava 720 — valor divergente que sobrepunha o template.
**Como aplicar:** em `gerar_mod4.py`, função `bpara()` emite apenas spacing; `run()` de corpo omite sz e color.

LD2 — Títulos de seção usam estilo nativo Ttulo2, nunca formatação manual. Bold+navy+sz+jc hardcoded em heading produz documento que quebrará visualmente se o template for atualizado. O estilo Ttulo2 já carrega espaçamento, cor e tipografia calibrados.
**Por quê:** comparação entre peça gerada e peça editada pela Raquel (12/05/2026) revelou que todos os títulos de seção foram migrados para Ttulo2.
**Como aplicar:** função `heading2()` usa `<w:pStyle w:val="Ttulo2"/>` sem nenhum atributo adicional; função `center_bold()` não deve ser usada para seções.

LD3 — Enumerações de três ou mais itens usam PargrafodaLista com marcador numérico entre parênteses. Inline com ponto e vírgula impede leitura rápida e não reflete a estrutura lógica da enumeração. Marcador extenso ("primeiro", "segundo") é redundante quando o número já ordena.
**Por quê:** revisão da Raquel (12/05/2026) converteu todos os blocos "primeiro/segundo/terceiro/quarto" e "(a)/(b)/(c)" em PargrafodaLista com "(1)/(2)/(3)".
**Como aplicar:** função `list_para()` usa `<w:pStyle w:val="PargrafodaLista"/>`. Schema: novo tipo `{"tipo": "lista", "items": [...]}`.

LD4 — Nome comercial da firma é "Almeida Marques Advocacia e Consultoria". "Sociedade Individual de Advocacia" é a razão social formal; o nome comercial abreviado é o padrão em assinaturas e qualificações.
**Por quê:** revisão da Raquel (12/05/2026) corrigiu a assinatura de "Sociedade Individual de Advocacia" para "Advocacia e Consultoria".
**Como aplicar:** verificar no `template_mod4.docx`; se divergente, corrigir o template. A constante no script deve ser `"Almeida Marques Advocacia e Consultoria"`.

## §9 — Pipeline pós-criação (sincronização Git)

Aplica-se a toda geração de `.skill` ou modificação de SKILL.md, tanto na interface web quanto no Cowork. Garante que web, Cowork e GitHub estejam sempre sincronizados.

### No Cowork (automático após empacotamento)

```powershell
# 1. Backup R3 da versão anterior (se existir)
$skill = "mod4"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$bk = "C:\RaquelSkills\_backups\$skill"
New-Item -ItemType Directory -Force -Path $bk | Out-Null
Copy-Item "C:\RaquelSkills\skills\$skill\SKILL.md" "$bk\SKILL-$ts.md" -ErrorAction SilentlyContinue

# 2. Extrair .skill para o repositório
Expand-Archive -Path "$env:USERPROFILE\Downloads\$skill.skill" `
               -DestinationPath "C:\RaquelSkills\skills\" -Force

# 3. Commit com mensagem canônica
cd C:\RaquelSkills
git add "skills/$skill/"
git commit -m "feat(mod4): v4.2.0 — LD1 herança Normal, LD2 Ttulo2, LD3 PargrafodaLista, LD4 firma"

# 4. Publicar
git push
```

### Na interface web (manual após download)

O `.skill` gerado aqui não acessa o Git diretamente. Fluxo:

```
1. Baixar o .skill via present_files
2. Executar o bloco PowerShell acima no terminal Windows
3. Confirmar hash do commit no terminal
```

### Verificação de sincronização

Após o push, confirmar que os três ambientes estão alinhados:

```powershell
cd C:\RaquelSkills
git log --oneline -5        # ver commits locais
git status                  # sem arquivos staged ou modified
git push                    # sem "ahead of origin" — se houver, rodar push
```
