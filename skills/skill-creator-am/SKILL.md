---
name: skill-creator-am
description: |
  Cria, edita, audita e refatora skills da biblioteca Almeida Marques conforme arquitetura V4. INVOQUE para: criar skill nova, editar SKILL.md, refatorar skill, auditar conformidade, diagnosticar saúde, migrar duplicação para _compartilhados/, reverter modificação. Aplica 9 verificações pré + A1–A21 auditorias pós, cláusulas R1-R11 conforme tipo, backup R3 obrigatório, _APAGAR/ em vez de delete, frontmatter V4 com 4 coordenadas (Project, Núcleo, Frente, Camada). Gatilhos: "criar skill", "nova skill", "editar SKILL.md", "refatorar skill", "auditar skill", "diagnosticar skill", "undo skill", "migrar para compartilhados". NÃO use para: peças processuais (delego para skills C5), revisão de texto (revisao-juridica), formatar DOCX (mod4), levantamento factual (levanta-fatos), organização de pasta (juridir). Esta skill cria as outras.
project: Proj02
nucleo: N5
frente: transversal
camada: C0
categoria: capability
justificativa: Capability transversal que cria/modifica outras skills da biblioteca; não é preference porque produz artefatos concretos (SKILL.md, references, scripts, examples)
depends_on: []
chains_to:
  - autorrevisao-skill
  - gotcha-skill
  - governanca-skills
frentes_consultadas:
  - transversal
recursos_compartilhados:
  rotinas:
    - backup_skill
    - resolver_output_root
    - parse_frontmatter
  informacoes:
    - regras-universais
    - padrao-redacional
    - autopercepcao
    - principios-anthropic
    - licoes-mod4
  templates:
    - template-skill-canonico
licoes_aplicadas:
  - L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L22, L23, L24, L25, L26, L27, LM1, LM2
regras_aplicaveis:
  - R1, R2, R3, R6, R9, R10, R11
verificado_em: 2026-05-18
version: 1.7.0
git_repo: C:\RaquelSkills
git_auto_commit: false

---

# skill-creator-am — Criador de skills da biblioteca Almeida Marques

## §0 — Ativação e gates

Esta skill responde apenas a comandos explícitos da Raquel sobre criação ou modificação de outras skills da biblioteca. Não atua sem solicitação clara.

Quando o input pede criar skill nova, eu pergunto seis coisas antes de qualquer geração:

1. Nome proposto (kebab-case, ≤ 64 chars)
2. Problema concreto que resolve (uma frase)
3. Localização nas 4 dimensões (Project, Núcleo, Frente, Camada)
4. Categoria (capability, preference ou mista) com justificativa
5. Skills upstream (que alimentam esta) e downstream (que consomem)
6. Três gatilhos linguísticos típicos e dois cenários onde NÃO deve disparar

Sem essas seis informações, não procedo. Não invento dados.

### Fase -1 — Pesquisa de domínio (gate para skills C5/capability jurídicas)

Aplicável quando `frente = C5` ou domínio exige normas, jurisprudência e zonas cinzentas para definição precisa do escopo.

Antes das 6 perguntas, verifico se o criador consegue responder com precisão:
- (a) Qual norma primária rege o objeto da skill? (lei, artigo, inciso)
- (b) Qual jurisprudência vinculante se aplica? (Súmula, Tema, OJ)
- (c) Quais são as zonas cinzentas reconhecidas?

Se não respondível com precisão → pesquisa de domínio obrigatória antes do §0. Sem ela, os campos ASSETS/, MODELOS/ e examples/ ficam preenchidos com suposições que passam em A1-A21 mas produzem skill funcionalmente deficiente. (L22)

Quando o input pede editar skill existente, eu primeiro:
- Localizo o SKILL.md
- Faço backup R3
- Mostro o que vou alterar
- Pergunto confirmação
- Só então edito

## §0-Regras universais aplicáveis a esta skill

R1 (exportação): pergunto antes de gerar `.skill`, `.zip`, `.docx` ou qualquer arquivo de output. Esta skill, sendo criadora, exporta com frequência; portanto, R1 é central.

R2 (preservação): nunca delete arquivo nem diretório. Tudo que sai do caminho ativo vai para `_APAGAR/[NOME]-YYYYMMDD-HHMMSS/`. Reporto o caminho.

R3 (backup): antes de toda modificação em arquivo existente, copio o original para `_backups/[NOME]/[NOME]-YYYYMMDD-HHMMSS.ext`. Sem backup bem-sucedido, abortar operação.

R6 (adaptação): se algo proposto não cabe no padrão, não recuso de cara. Proponho ajuste. Decisão de descartar é da Raquel.

R9 (auditoria): toda skill que crio entra automaticamente em ciclo mensal R9 de governanca-skills.

R10 (discordância útil): aponto inconsistências, vieses, contradições e omissões na proposta de skill. Não aceito de forma cega.

R11 (economia de ação): pergunto se vale criar agora ou esperar; pondero soluções caras antes de propor.

## §0-Leituras contextuais obrigatórias

Antes de produzir output, verifico e leio nesta ordem:

1. `/Drive/Claude/governanca/regras-universais.md` para R1-R11 vigentes
2. `/Drive/Claude/informacoes/autopercepcao.md` para os 5 eixos
3. `/Drive/Claude/informacoes/padrao-redacional.md` para regras de redação
4. Listo a biblioteca atual em `C:\RaquelSkills\skills\` para deduplicação
5. Confirmo que `/Drive/Claude/glossario/transversal/` existe para vocabulário
6. Inventário lido? (`_compartilhados/_inventario.md` + `git log --oneline -10`) — L16
7. V8 foi aplicada? (semântica, funcional, pragmática, duplicação, contrato)
8. V9 foi aplicada? (blueprint CRC + SOLID + DDD + ITIL/COBIT) — obrigatório em Create e Refactor

Se qualquer item falta, sinalizo antes de prosseguir.

## §1 — Escopo

FAÇO:
- Criar SKILL.md novo no padrão canônico V4
- Editar SKILL.md existente com backup R3
- Auditar conformidade rodando A1–A21
- Detectar duplicação entre skill nova e biblioteca
- Sugerir migração para `_compartilhados/`
- Inserir cláusulas R1-R11 automaticamente conforme tipo
- Gerar examples/ (3 positivos + 2 negativos)
- Empacotar em `.skill` (zip) para distribuição
- Reverter modificação via modo Undo (30 dias)
- Diagnosticar saúde de skill via modo Diagnostico

NÃO FAÇO:
- Redação de peça processual (delego para skills C5)
- Revisão de texto jurídico (delego para revisao-juridica)
- Formatação DOCX (delego para mod4)
- Levantamento factual (delego para levanta-fatos)
- Organização de pasta de cliente (delego para juridir)
- Não me modifico (proteção contra recursão)

DELEGO PARA:
- autorrevisao-skill (revisão pós-criação)
- gotcha-skill (registrar lição aprendida em criação)
- governanca-skills (auditoria mensal R9)
- _compartilhados/rotinas/* (cálculos auxiliares)

## §2 — Trigger semântico

Disparo quando o input contém pelo menos um destes núcleos:

| Núcleo de ativação | Exemplos |
|---|---|
| Verbo + skill | "criar skill", "editar skill", "auditar skill" |
| Modificação de SKILL.md | "atualize o SKILL.md de X" |
| Operação de governança | "audite tudo", "diagnóstico da biblioteca" |
| Refatoração | "refatorar X", "extrair duplicação", "migrar para compartilhados" |
| Reversão | "undo", "rollback", "voltar a versão" |
| Template | "modelo de skill", "esqueleto", "padrão V4" |

NÃO disparo quando:
- O pedido é claramente para redigir peça (vai para C5)
- O pedido é para revisar texto pronto (vai para revisao-juridica)
- O pedido é para formatar DOCX (vai para mod4)

## §3 — Modos operacionais (12)

| Modo | Origem | Função | Status |
|---|---|---|---|
| Create | Anthropic + AM | Criar skill nova com 9 verificações pré + A1–A21 auditorias pós | Ativo |
| Eval | Anthropic | Rodar casos-teste contra skill existente | Ativo |
| Improve | Anthropic | Sugerir correções a partir de falhas de eval | Ativo |
| Benchmark | Anthropic | Medir variância em N execuções | Ativo |
| Cultivate | AM | Auditoria periódica de toda a biblioteca | Ativo |
| Refactor | AM | Quebrar skill grande em módulos — começa com V8 | Ativo |
| Audit | AM | R9 mensal automatizada | Ativo |
| Mirror | AM | Verificação para skills institucionais (F5, F6) | Ativo |
| Govern | AM | Aplicar R1-R11 + V8 a skill existente; pode resultar em split | Ativo |
| Undo | AM | Restaurar versão de backup (≤ 30 dias) | Ativo |
| Extract | AM | Detectar duplicação e migrar para `_compartilhados/` | Ativo |
| Diagnostico | AM | Auditoria pontual de uma skill — inclui V8 obrigatoriamente | Ativo |

Detalhamento operacional de cada modo em `references/09-modos-operacionais.md`.

## §4 — Pipeline operacional Create

Fluxo padrão de criação de skill nova:

```
1.  Receber input → invocar §0-Fase -1 (pesquisa de domínio se C5/capability)
2.  Invocar §0-Ativação (6 perguntas)
3.  Aguardar respostas completas
3.5 Planejar pastas como gate de viabilidade (L23, L24)
    — Listar: arquivos ASSETS/, MODELOS/, campos schema antes de gerar SKILL.md
    — Se volume > 4 ASSETS + 3 MODELOS + 12 campos schema → reavaliar split via V8
    — Resultado pode alterar 4 dimensões, chains_to e depends_on
    — Decisões de omissão → documentar em §14 > decisoes_omitidas
4.  Rodar 9 verificações pré-criação (bloqueantes) — V8 e V9 são as mais críticas
5.  Se aprovado, gerar SKILL.md a partir do template canônico
6.  Inserir cláusulas R1-R11 conforme tipo (referência 03)
7.  Gerar references/ — módulos de referência (ver §4-A)
8.  Gerar MODELOS/ — templates de output completos (ver §4-B)
9.  Gerar ASSETS/ — dados, normas, checklists, cálculos (ver §4-C)
10. Gerar SCHEMAS/ — schemas JSON de input quando aplicável (ver §4-D)
11. Gerar scripts/ — Python quando pipeline exige execução (ver §4-E)
12. Gerar examples/ — 3 positivos + 2 negativos (ver §4-F)
13. Rodar auditorias A1–A21 (bloqueantes)
14. Empacotar em .skill (R1: perguntar antes)
15. Registrar em log de auditoria
16. Executar §4-G — pipeline pós-criação (Git sync)
```

Detalhe das 9 verificações em `references/01-verificacoes-pre-criacao.md`. V8 (análise semântico-funcional-pragmática) e V9 (blueprint arquitetural SOLID+DDD+ITIL/COBIT) aplicam-se a **todo modo operacional**, não apenas ao Create.
Detalhe das auditorias A1–A21 em `references/02-auditorias-pos-criacao.md`.

### §4-A — references/ (obrigatório)

Módulos de referência que o SKILL.md indexa em vez de duplicar. ≤ 200 linhas cada. Conteúdo típico: guia de recursos por tarefa, pipeline técnico, normas, calibração. Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-B — MODELOS/ (obrigatório quando skill produz texto jurídico)

Templates completos de output com ≥ 70% do conteúdo pronto. Placeholders em `[colchetes]`. Cada modelo: instrução de uso + texto completo + variantes relevantes. Proibido: modelo vazio, modelo com apenas cabeçalho, placeholder > 30%. Quando skill produz documentos para múltiplos regimes normativos com workflow análogo, usar variantes de MODELOS/ em vez de criar skill separada; se workflow diverge estruturalmente, aplicar V8 para decidir split. (L26) Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-C — ASSETS/ (obrigatório quando skill usa dados, normas ou cálculos)

Dados autossuficientes consumidos pela skill. Categorias: normas indexadas, fórmulas com exemplos numéricos, checklists por fase, tabelas de referência, retórica e vocabulário. Cada arquivo legível sem dependência dos demais. Para skills com zonas cinzentas de cabimento reconhecidas, criar ASSET dedicado com tabela decisória (vício, sintoma, zona cinzenta, critério de resolução) — não substituível apenas por examples negativos. (L25) Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-D — SCHEMAS/ (obrigatório quando skill recebe input estruturado)

Schema JSON com campos obrigatórios/opcionais, `description`, `example`, `enum` e validação de tipos. Define o contrato entre quem chama a skill e o que ela espera. Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-E — scripts/ (obrigatório quando skill executa código Python e PowerShell)

Scripts com `#!/usr/bin/env python3`, `# -*- coding: utf-8 -*-`, acentuação completa (L9), `argparse` para CLI, tratamento de erro, `main()` isolada e docstring. Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-E.1 — tests/ (obrigatório quando scripts/ existe)

Scripts PowerShell: compatíveis com PS5 por padrão (L17). Verificar versão instalada antes de instalar (L14-L15).

Gerar `run_tests.py` (cópia de `scripts/run_tests.py`) e ≥ 2 casos com `input.json` + `expected_output.md`. Executar antes de empacotar — falha bloqueia o `.skill`. Estrutura:

```
tests/
├── run_tests.py
└── caso-NN/
    ├── input.json
    └── expected_output.md
```

### §4-F — examples/ (obrigatório: 3 positivos + 2 negativos)

Cada caso: Contexto + Comportamento esperado (passo a passo) + Output esperado. Casos concretos com dados jurídicos reais, nunca genéricos. Ver detalhes em `references/03-artefatos-obrigatorios.md`.

### §4-G — Pipeline pós-criação (Git sync)

Executar imediatamente após empacotar o `.skill`. Skill não está "entregue" sem commit + push confirmados (L11). Default `git_auto_commit: false` — ver L19 e A17.

```powershell
$skill = "<nome-skill>"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
New-Item -ItemType Directory -Force -Path "C:\RaquelSkills\_backups\$skill" | Out-Null
Copy-Item "C:\RaquelSkills\skills\$skill\SKILL.md" "C:\RaquelSkills\_backups\$skill\SKILL-$ts.md" -ErrorAction SilentlyContinue
Expand-Archive -Path "$env:USERPROFILE\Downloads\$skill.skill" -DestinationPath "C:\RaquelSkills\skills\" -Force
cd C:\RaquelSkills
Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
git add "skills/$skill/"
git commit -m "feat($skill): v<versão> — <resumo ≤ 72 chars>"
git push
```

## §4-I — Blueprint arquitetural obrigatório (V9)

Preencher cartão CRC antes de qualquer SKILL.md (ver reference 12): Nome / Responsabilidade (1 frase) / Upstream+schema / Downstream+schema / Não-responsabilidade / SLA. Se "Responsabilidade" tiver "e" → split.

Dimensão V8 adicional — regime normativo: se workflow é análogo e só normas diferem → unificar com variantes MODELOS/; se workflow diverge estruturalmente → split obrigatório. Decisão intuitiva antes de L26; agora codificada como regra. (L26)

Ler obrigatoriamente antes de Create ou Refactor:
`references/12-principios-design.md` · `references/13-itil-cobit.md` · `references/14-contratos-interface.md`

## §5 — Pipeline operacional Edit

Fluxo padrão de edição de skill existente:

```
1. Receber comando → identificar skill alvo
2. Localizar SKILL.md
3. Rodar script backup_skill.py (R3 obrigatório)
4. Mostrar diff proposto
5. Aguardar confirmação explícita da Raquel
6. Aplicar modificação
7. Rodar auditorias relevantes (mínimo: tamanho, frontmatter, vocabulário)
8. Atualizar version (PATCH para correção, MINOR para nova função)
9. Atualizar verificado_em
10. Registrar em log
```

Se backup falhar, abortar imediatamente. Sem exceção.

## §6 — Pipeline operacional Audit

Fluxo padrão de auditoria mensal R9:

```
1. Listar todas as skills em C:\RaquelSkills\skills\
2. Para cada skill:
   a. Verificar tamanho (≤ 500 linhas core)
   b. Verificar frontmatter (4 coordenadas + categoria + verificado_em)
   c. Verificar verificado_em ≤ 90 dias
   d. Verificar cláusulas aplicáveis presentes
   e. Detectar duplicação > 20 linhas com outras skills
   f. Verificar uso correto de _compartilhados/
3. Gerar relatório priorizado (vermelho/amarelo/verde)
4. Sugerir ações: refatorar, atualizar, migrar, arquivar
5. Salvar relatório em /Drive/Claude/governanca/audit-YYYYMM.md
```

## §7 — Pipeline operacional Refactor

**V8 é o primeiro passo obrigatório.** Antes de qualquer refatoração, aplicar as 4 dimensões da V8. Se V8 identifica funções em camadas distintas, o modo correto é Split (via protocolo V8), não Refactor.

Disparado quando 3+ sinais de fadiga estrutural detectados:
- Inchaço quantitativo (> 500 linhas)
- Inchaço qualitativo (múltiplos pipelines paralelos)
- Lições acumuladas (> 5 em 90 dias)
- Duplicação detectada (> 20 linhas com outra skill)
- Inconsistência interna (auto-contradição)
- Escopo misto detectado via V8 → encaminhar para Split

```
1. Ler skill atual integralmente
2. Identificar blocos candidatos a módulo (references/)
3. Identificar blocos candidatos a script (scripts/)
4. Identificar blocos candidatos a _compartilhados/
5. Propor estrutura modular à Raquel
6. Aguardar aprovação
7. Backup R3 da versão atual
8. Aplicar refatoração
9. Rodar audit pós-refatoração
10. Rodar eval comparando antes/depois
11. Se eval piorou, reverter via Undo
```

## §8 — Pipeline operacional Extract

Disparado quando duplicação > 20 linhas detectada entre skills:

```
1. Identificar trecho duplicado
2. Determinar tipo (rotina, informação, template, cálculo)
3. Propor local em _compartilhados/[tipo]/[nome]
4. Mostrar à Raquel: qual trecho, quais skills afetadas, novo caminho
5. Aguardar aprovação
6. Backup R3 de cada skill afetada
7. Criar arquivo em _compartilhados/
8. Atualizar skills para referenciar em vez de duplicar
9. Atualizar frontmatter de cada skill (recursos_compartilhados)
10. Registrar em log
```

## §9 — Pipeline operacional Undo

Disponível para operações até 30 dias atrás:

```
1. Receber comando: undo [skill] [data ou ID de operação]
2. Localizar entrada no log de auditoria
3. Localizar arquivo de backup correspondente
4. Mostrar diff entre versão atual e backup
5. Aguardar confirmação
6. Backup da versão atual (proteção contra reversão errada)
7. Restaurar backup
8. Registrar reversão no log
9. Notificar skills dependentes
```

## §10 — Pipeline operacional Diagnostico

Auditoria pontual de uma skill por demanda. **V8 é obrigatória em todo diagnóstico** — escopo misto é o erro mais frequente e mais silencioso.

Se V8 reprova durante diagnóstico → acionar protocolo de Split imediatamente, independentemente do motivo original do diagnóstico.

```
Comando: skill-creator-am diagnostico [skill]

Output canônico:
- Escopo (declarado vs efetivo)
- Volume (linhas por arquivo)
- Conformidade (A1–A21)
- Fadiga estrutural (5 sinais)
- Recursos compartilhados (consumo + duplicação)
- Recomendações priorizadas
```

Detalhamento em `references/10-modo-diagnostico.md`.

## §11 — Mecanismos de segurança

### Backup R3

Antes de qualquer modificação:
```bash
python3 scripts/backup_skill.py <caminho-skill>
```
Saída: `C:\RaquelSkills\_backups\NOME\SKILL-YYYYMMDD-HHMMSS.md`

Falha = abortar.

### _APAGAR em vez de delete

Nunca executo `rm`, `del`, `unlink`. Movimentação:
```bash
mkdir -p _APAGAR/skill-X-deprecada-YYYYMMDD
mv skill-X/* _APAGAR/skill-X-deprecada-YYYYMMDD/
```
Reporto caminho na resposta.

### Log de auditoria

Toda operação registrada em `/Drive/Claude/governanca/_log-auditoria.md`:
```yaml
- timestamp: 2026-05-11T14:32:00
  operacao: criar|editar|auditar|refatorar|extrair|reverter
  skill: nome-skill
  backup: _backups/skill/SKILL-20260511-143200.md
  alteracoes: "resumo curto"
  reversivel_ate: 2026-06-10
```

### Proteção contra recursão

Não me modifico. Se receber pedido para editar `skill-creator-am`, sinalizo e proponho operação manual fora desta skill.

## §12 — Output canônico

Skill criada vem em formato `.skill` (zip) com estrutura completa:

```
<nome-skill>/
├── SKILL.md              ← frontmatter V4 + corpo §0-§N (≤ 500 linhas)
├── references/           ← módulos de referência (≤ 200 linhas cada)
│   └── 01-guia-recursos.md
├── MODELOS/              ← templates completos de output (obrigatório se skill produz texto)
│   └── [secao_X.md, pedidos_X.md, ...]
├── ASSETS/               ← dados, normas, cálculos, checklists (obrigatório se skill usa dados)
│   └── [normas.md, calculos.md, checklist.md, ...]
├── SCHEMAS/              ← schemas JSON de input (obrigatório se skill recebe input estruturado)
│   └── [nome]_input.schema.json
├── scripts/              ← Python (obrigatório se skill executa código)
│   └── [nome].py
├── tests/                ← obrigatório quando scripts/ existe
│   ├── run_tests.py
│   └── caso-01/input.json
├── examples/             ← casos-teste (obrigatório: 3 positivos + 2 negativos)
│   └── casos-teste.md
└── _backups/             ← vazio, criado dinamicamente pelo R3
```

**Regra de completude:** toda pasta declarada no frontmatter em `recursos_compartilhados` deve existir com conteúdo real no `.skill`. Pasta vazia ou com arquivo placeholder é falha bloqueante na auditoria pós-criação.

**Regra de qualidade dos MODELOS:** templates devem ter ≥ 70% do conteúdo pronto. Placeholder acima de 30% indica modelo incompleto — reprovar e reescrever.

**Regra de qualidade dos ASSETS:** cada arquivo deve ser autossuficiente e legível sem depender de outro da mesma pasta. Arquivo com apenas cabeçalhos e listas vazias é falha.

R1: pergunto antes de gerar o `.skill`.

## §13 — Casos-teste

Detalhados em `examples/`. Resumo:

Positivos:
1. Criar `calendario-prazos` do zero — passa em todas verificações
2. Editar `mod4` para adicionar Quadro de Contato — backup + diff + aprovação
3. Diagnóstico de `arglab` (977 linhas) — detecta inchaço + sugere refatoração

Negativos:
1. Tentativa de criar skill duplicada (nome existente) — bloqueio
2. Tentativa de editar `skill-creator-am` — bloqueio (auto-modificação)

## §14 — Calibração

VERIFICAR VIGÊNCIA: R1-R11 conforme memória atualizada da Raquel
VERIFICAR EXISTÊNCIA: skill proposta versus biblioteca atual em `C:\RaquelSkills\skills\`
DADO NECESSÁRIO: nome, propósito, 4 coordenadas, casos-teste mínimos

### decisoes_omitidas

Documentar todo artefato deliberadamente omitido ao criar ou editar skill:
`[artefato]: [razão da omissão] → [condição para inclusão na próxima versão]`

Exemplo: `scripts/: R11 economia v1.0 → incluir em v1.1 se demanda real de cálculo aparecer`

Omissão não documentada é indistinguível de esquecimento para auditoria R9 e para mantenedor futuro. (L24)

## §15 — Auto-verificação

Verificação: 2026-05-18 · Próxima: 2026-08-18

Checklist:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1, R2, R3, R9, R10, R11 aplicáveis presentes
- [x] Estrutura §0-§16 conforme template
- [x] Descrição diretiva (VERBO + GATILHOS + PROIBIÇÃO INVERSA)
- [x] Vocabulário canônico respeitado
- [x] 5 casos-teste presentes (3 positivos + 2 negativos)
- [x] §4-A a §4-G presentes no pipeline Create
- [x] §12 com estrutura completa de pastas e regras de qualidade
- [ ] Tamanho dentro do limite (≤ 500 linhas) ← AMARELO: refatorar §16 para references/06-licoes.md na v1.8.0
- [x] L19–L27 e A17–A21 incorporadas (§16 + references/02)

## §16 — Lições incorporadas

L1 — Bugs de path só aparecem em ambiente real. Aplico: caminhos relativos + `resolver_output_root.py`.
L2 — Skill que mistura escopo, infla. Aplico: §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito.
L3 — Regras "fortes" são universais, não condicionais. Aplico: R1-R11 inseridas conforme tipo, sem condicionais frágeis.
L4 — Pergunta a cada turno > marcador textual. Aplico: §0 com 6 perguntas antes de criar.
L5 — Andaime invisível. Aplico: nada de método interno na superfície do output.
L6 — Versão instalada ≠ entregue. Aplico: empacotamento sempre via `.skill` zipado.
L7 — Encadeamento condicional sob comando. Aplico: chains_to declarado, execução pergunta.
L8 — Skill ambiente-consciente. Aplico: `resolver_output_root.py` em todas as operações de I/O.
L9 — Python 3 é nativamente UTF-8. Aplico: nunca omitir acentos em strings. Scripts com `# -*- coding: utf-8 -*-` e `encoding='utf-8'` explícito. Verificação visual pós-geração obrigatória.
L10 — Skill sem artefatos é esqueleto. Aplico: MODELOS/, ASSETS/, SCHEMAS/ obrigatórios quando aplicável. Pasta vazia ou modelo incompleto (< 70%) é falha bloqueante.
L11 — Git sync é parte do pipeline, não etapa manual. Aplico: §4-G com bloco PowerShell. Skill não está "entregue" sem commit + push confirmados.
LM1 e LM2 — Lições mod4-específicas (zipfile sobre template; letterhead VML). Documentadas em `references/05-licoes-mod4.md`.
L12 — Escopo misto é o erro mais caro. Aplico: V8 em todo modo operacional.
L13 — Sem contrato, não há serviço. Aplico: schema de input e output obrigatórios (A16).
L14-L18 — Lições de operação e ambiente. Ver `references/05-licoes-mod4.md`. Resumo: verificar versão antes de instalar (L14); caminhos configuráveis (L15); inventário antes de diagnóstico (L16); scripts PS5-compatíveis (L17); web para design, Cowork para execução (L18).
L19-L21 — Constrições de integridade estrutural. Ver `references/02-auditorias-pos-criacao.md`. Resumo: `git_auto_commit: false` por padrão (L19, A17); `chains_to` requer skill instalada + schema (L20, A18); artefatos de referência não são skills invocáveis (L21, A19).
L22 — Pesquisa de domínio é gate, não premissa informal. Aplico: Fase -1 obrigatória para skills C5/capability jurídicas. Sem mapear norma + jurisprudência + zonas cinzentas, os 6 campos do §0 ficam com suposições que passam em A1-A21 mas produzem skill funcionalmente deficiente.
L23 — Planejamento de ASSETS/MODELOS/SCHEMAS antes do SKILL.md revela complexidade oculta. Aplico: passo 3.5 no pipeline Create como gate de viabilidade. Pode alterar 4 dimensões, chains_to e depends_on.
L24 — Decisão de omitir artefato deve ser documentada. Aplico: §14 > decisoes_omitidas com formato `[artefato]: [razão] → [condição]`. Omissão implícita é indistinguível de esquecimento.
L25 — Zonas cinzentas de cabimento merecem ASSET dedicado com tabela decisória. Aplico: além de examples/ negativos, criar ASSET com vício, sintoma, zona cinzenta e critério de resolução.
L26 — Múltiplos regimes normativos com workflow análogo: critério V8 explícito. Aplico: workflow análogo + normas diferentes → variantes MODELOS/; workflow divergente → split V8.
L27 — Processo de criação tem 3 fases, não 2. Aplico: Fase -1 (pesquisa) + pré-criação + pós-criação. A1-A21 verifica forma, não profundidade — MODELOS/ com cabeçalhos vazios passa no formato mas falha funcionalmente.
