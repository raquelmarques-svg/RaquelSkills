# Decisões Arquiteturais — Biblioteca Almeida Marques

Formato: ADR-NN · data · decisão · motivação · consequência
Lido por: skill-creator-am (antes de Create/Edit — enforçar nas skills novas)
Atualizado por: skill-creator-am modo Edit após decisão aprovada por Raquel

---

## ADR-01 · mai/2026 · Taxonomia de 9 tipos de componente

**Decisão:** a biblioteca é composta por exatamente 9 tipos de componente com responsabilidade distinta:
1. **SKILL.md** — contrato de ativação e pipeline de orquestração (≤200 linhas)
2. **_compartilhados/** — bibliotecas transversais consumidas por 3+ skills via depends_on
3. **ASSETS/** — base de conhecimento por skill; lazy loading por etapa de pipeline (≤300l/arquivo)
4. **SCHEMAS/** — contratos de dados JSON Schema; validam input/output de scripts e skills
5. **scripts/** — código Python/Bash executável via bash; nunca carregado como contexto LLM
6. **examples/** — pares input.json + expected_output.md para autorrevisao-skill
7. **tests/** — testes de conformidade automáticos para governanca-skills
8. **manifests/** — declarações de estado esperado (biblioteca.manifest.yaml)
9. **plugin (.skill)** — artefato de deploy; zip com todos os componentes acima

**Motivação:** misturar tipos em um único arquivo (SKILL.md gigante) degrada qualidade de raciocínio e impede reuso.
**Consequência:** toda skill nova criada via skill-creator-am deve declarar explicitamente quais tipos de componente usa e em quais etapas do pipeline.

---

## ADR-02 · mai/2026 · Budget de linhas por tipo

**Decisão:**
- SKILL.md: máximo 200 linhas
- ASSETS/ por arquivo: máximo 300 linhas
- _compartilhados/ por arquivo: máximo 150 linhas
- schemas JSON: sem limite rígido (geralmente 30–80 linhas)

**Motivação:** acima de 200 linhas no SKILL.md, o LLM ignora seções finais em sessões longas. Budget de ASSETS/ é maior porque são carregados isoladamente.
**Consequência:** skill com SKILL.md > 200 linhas está violando ADR-02. skill-creator-am deve sinalizar e sugerir migração de conteúdo para ASSETS/.

---

## ADR-03 · mai/2026 · Regras G1–G6 de granularidade

**G1 — Co-ocorrência:** conteúdos sempre consultados juntos ficam no mesmo arquivo. Raramente co-ocorrem → arquivos separados.
**G2 — Frequência de atualização:** dados que mudam juntos ficam juntos (ex: tabela OAB muda anualmente; cláusulas de contrato mudam por decisão do escritório → arquivos separados).
**G3 — Budget por sessão:** total carregado (SKILL.md + _compartilhados/ + ASSETS/ da etapa atual) ≤ 600 linhas.
**G4 — Scripts não são contexto:** cálculo determinístico vai em Python, não em ASSETS/. LLM recebe o resultado, não tenta calcular.
**G5 — Schemas são âncoras:** toda skill com output estruturado repetível tem schema correspondente. LLM valida seu próprio output contra o schema.
**G6 — _compartilhados/ sem pipeline:** arquivos em _compartilhados/ são referências passivas. Pipeline só existe em SKILL.md.

**Motivação:** granularidade errada desperdiça tokens ou degrada reuso.

---

## ADR-04 · mai/2026 · Lazy loading de ASSETS/

**Decisão:** ASSETS/ não são carregados na ativação da skill. Cada ASSET é carregado explicitamente pelo pipeline na etapa que o usa. O SKILL.md declara no §2 Pipeline qual ASSET carrega em qual etapa.

**Exemplo:** honorarios carrega tabela-oab-2026.md apenas em P2 (cálculo), não em P1 (levantamento factual).

**Motivação:** carregar todos os ASSETS na ativação excede o budget de sessão sem necessidade.
**Consequência:** §2 Pipeline deve nomear explicitamente os ASSETS com "→ carregar ASSETS/nome.md".

---

## ADR-05 · mai/2026 · _compartilhados/ — 7 bibliotecas + 5 schemas

**Conteúdo canônico aprovado:**

Bibliotecas (informacoes/):
- padrao-redacional.md — R1–R12 de redação jurídica
- comportamento-base.md — leitura de contexto + output inline + atualização de dossiê
- cnj-ia-154.md — protocolo de comunicação com IA judicial (Rec. CNJ 154/2024)
- formulas-enderecamento.md — fórmulas por foro (TJSP, JEF, TRT, STJ, STF, Núcleo 4.0)
- vocabulario-vedacoes.md — verbos proibidos, travessão, "não X mas Y"
- qualificacao-advogada.md — dados fixos da advogada (nome, OAB, email AM, telefone)
- licoes-aprendidas.md — log L[N] gerenciado por gotcha-skill

Schemas (SCHEMAS/):
- input/status-pre-mod4.v1.json — contrato de input da revisao-previa-mod4
- output/fatos-estruturados.v1.json — contrato de output do levanta-fatos
- output/dossie-caso.v1.json — contrato de output do dossie-caso
- output/resumo-do-caso.v1.json — schema canônico das 7 seções + extensões por área
- output/qualificacao-parte.v1.json — estrutura de qualificação de pessoa física e jurídica

**Motivação:** sem _compartilhados/, 650+ linhas de conteúdo idêntico são duplicadas entre skills.

---

## ADR-06 · mai/2026 · Plano de 4 fases de refatoração

**Decisão:** refatoração segue sequência obrigatória de dependências:
- Fase 0: broken references (urgência — falhas silenciosas em produção hoje)
- Fase 1: _compartilhados/ completo (pré-requisito de skills novas)
- Fase 2: edições em skills ativas (conformidade + ASSETS)
- Fase 3: 9 skills novas criadas
- Fase 4: deprecações + governança

**Motivação:** criar skills novas antes de _compartilhados/ garante nova rodada de duplicação.
**Consequência:** nenhuma skill nova é criada antes da Fase 1 estar completa.

---

## ADR-07 · mai/2026 · Mapa de 12 skills ausentes do Cowork

**9 a criar (skills novas):**
honorarios, alimentos, ms, revisao-juridica, arglab, probat, prod-antecipada-prova, check-audiencia-trabalhista, organizar-pasta-cliente

**1 a incorporar em skill existente:**
monitor-publicacoes → conteúdo vai para check-protocolo/ASSETS/ (BLOCOs A, F, G)

**1 a converter para _compartilhados/:**
padrao-redacional → _compartilhados/informacoes/padrao-redacional.md (não é skill)

**1 a descartar:**
skill-creator (Anthropic generic) → _APAGAR/ (coberta por skill-creator-am)

**Motivação:** 12 lacunas mapeadas com precisão evitam criação duplicada ou esquecimento.
