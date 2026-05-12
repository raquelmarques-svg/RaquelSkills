# Glossário arquitetural V4 — termos canônicos

Vocabulário controlado da arquitetura. Esta reference fixa o sentido de cada termo. Termos fora desta lista são neologismos a serem evitados.

## Termos de organização

**Arquitetura V4**: estado consolidado da biblioteca de skills da Almeida Marques, datado de maio/2026. Supera V1, V2 e V3.

**Biblioteca**: conjunto de 33 skills planejadas (19 instaladas em momento variável). Reside em `C:\RaquelSkills\skills\`.

**Skill**: unidade autônoma de comportamento computacional. Tem SKILL.md, references opcionais, scripts opcionais, examples obrigatórios.

**Capability**: skill que faz algo. Produz output. Outras skills podem chamá-la.

**Preference**: skill que configura comportamento. Não produz output isolado.

**Mista**: skill que faz e configura. Rara; exige justificativa.

**4 dimensões**: Project + Núcleo + Frente + Camada. Localização da skill no espaço conceitual.

## Termos das 4 dimensões

**Project (ProjNN)**: organização institucional do Claude.ai. Sete projects: Proj01 (a confirmar), Proj02 (Almeida Marques Geral), Proj03 (Contratos), Proj04 (Perícia), Proj05 (Astrea/Controladoria), Proj06 (a confirmar), Proj07 (a confirmar).

**Núcleo (NN)**: família funcional. Seis núcleos: N1 (Linguagem), N2 (Método jurídico), N3 (Estratégia processual), N4 (Honorários), N5 (Governança), N6 (Perícia).

**Frente (FN)**: área de prática. Seis frentes: F1 (Previdenciário-BPC-Acidentário), F2 (Processual-Controladoria), F3 (Contratos-Honorários-ZapSign), F4 (Família-Alimentos-Coletivo), F5 (Bancada Ativista), F6 (Artemis).

**Camada (CN)**: etapa do fluxo. Dez camadas: C0 (Transversais), C1 (Intake), C2 (Organização), C3 (Levantamento), C4 (Análise), C5 (Matéria), C6 (Revisão), C7 (Formatação), C8 (Protocolo), C9 (Pós-processo).

## Termos de governança

**R1-R11**: regras universais. Aplicáveis a toda skill, agente, bash, código gerado. Não condicionais.

**L1-L10**: lições da mod4. Aprendidas em refatorações reais. Aplicáveis conforme tipo.

**P1-P8**: princípios Anthropic 2026. Integrados à arquitetura V4 com adaptações.

**verificado_em**: data de última validação da skill. Válido por 90 dias. Após vencimento, requer re-validação.

**version**: número semântico MAJOR.MINOR.PATCH. Atualizado em cada modificação.

**Backup R3**: cópia obrigatória antes de modificar arquivo. Local: `_backups/[NOME]/[NOME]-YYYYMMDD-HHMMSS.ext`.

**_APAGAR/**: diretório de quarentena. Substitui delete. Preserva por 90 dias antes de revisão humana.

**Log de auditoria**: registro de toda operação do skill-creator-am. Em `/Drive/Claude/governanca/_log-auditoria.md`. Imutável por 12 meses.

## Termos de modos operacionais

**Modo Create**: criar skill nova. Aplica 7 verificações pré + 12 auditorias pós.

**Modo Edit**: editar SKILL.md existente. Backup R3 obrigatório.

**Modo Eval**: rodar casos-teste contra skill.

**Modo Improve**: sugerir correções a partir de falhas de eval.

**Modo Benchmark**: medir variância em N execuções.

**Modo Cultivate**: auditoria periódica de toda a biblioteca.

**Modo Refactor**: quebrar skill grande em módulos.

**Modo Audit**: R9 mensal automatizada.

**Modo Mirror**: verificação para skills institucionais (F5, F6).

**Modo Govern**: aplicar R1-R11 a skill existente.

**Modo Undo**: restaurar versão de backup (≤ 30 dias).

**Modo Extract**: detectar duplicação e migrar para `_compartilhados/`.

**Modo Diagnostico**: auditoria pontual de uma skill.

## Termos de recursos compartilhados

**_compartilhados/**: diretório de núcleos comuns. Em `C:\RaquelSkills\_compartilhados/`.

**Rotina**: script Python compartilhado. Em `_compartilhados/rotinas/`.

**Template**: asset (DOCX, XML, MD) compartilhado. Em `_compartilhados/templates/`.

**Cálculo**: script Python de lógica numérica compartilhado. Em `_compartilhados/calculos/`.

**Informação canônica**: markdown de referência. Em `/Drive/Claude/informacoes/`.

**Glossário vivo**: vocabulário controlado por frente. Em `/Drive/Claude/glossario/`.

**Acervo de jurisprudência**: precedentes verificados. Em `/Drive/Claude/jurisprudencia/`.

## Termos de fluxo

**Encadeamento condicional**: skill A chama skill B sob comando. Não automático.

**chains_to**: campo do frontmatter. Lista skills downstream.

**depends_on**: campo do frontmatter. Lista skills upstream.

**Upstream**: skill que alimenta esta com input.

**Downstream**: skill que consome output desta.

**Pipeline**: sequência de etapas dentro da skill.

## Termos de qualidade

**Inchaço quantitativo**: SKILL.md > 500 linhas.

**Inchaço qualitativo**: múltiplos pipelines paralelos, categorias misturadas.

**Fadiga estrutural**: 3+ sinais de problema acumulados.

**Duplicação**: trecho > 20 linhas igual em duas skills.

**Discordância útil**: oferta de contraponto, contradição ou ressalva. Não vale por si; vale por evitar erro.

## Termos de skill autoconsciente

**Auto-percepção**: capacidade de skill avaliar seu próprio estado em 5 eixos.

**5 eixos**: escopo próprio, volume saudável, conformidade canônica, hora de refatorar, recursos compartilhados.

**§0-Autopercepção**: bloco leve em toda skill (3 perguntas).

**§N-AutoVerificação**: bloco detalhado em skills de governança e na própria skill-creator-am.

## Termos de erro e correção

**Gotcha**: armadilha. Erro acontecido que se transforma em lição.

**Gotcha-skill**: skill que captura gotchas. Sprint 1.

**Drift**: deriva. Skill que diverge do padrão ao longo do tempo.

**Reversibilidade**: capacidade de desfazer operação. Janela: 30 dias para Undo, sempre para R2 (`_APAGAR/`).

## Termos de output

**Inline**: output direto na resposta de chat. Padrão.

**Arquivo**: output em filesystem. Só sob R1.

**Empacotamento**: zip com estrutura canônica de skill. Formato `.skill`.

**DOCX corporativo**: documento com paleta navy/cream, Cambria 12pt, template mod4.

## Termos de peça processual (consumidos por C5)

**Quadro de Contato**: bloco visual canônico após qualificação, antes de Preliminares. Mostra telefone, e-mail, endereço, ponto de referência.

**Princípio do escudo prévio**: incluir antes do problema aparecer subseção curta com fundamentação normativa + prequestionamento + menção nos pedidos.

**Subseções de blindagem (I.A-I.H)**: bloco padrão para juízos com questionamento recorrente. Catálogo de 10 (residência, ZapSign, Juízo 100% Digital, valor JEF, gratuidade, prioridade, dispensa REQ, competência, e mais 2).

**CAT-XX**: 40 categorias de erro processual mapeadas na matriz. CAT-39, CAT-40, CAT-41 incluídas em maio/2026.

**33 recursos de inteligibilidade**: catálogo de elementos visuais canônicos para peças.

---

## Termos proibidos (variantes a evitar)

| Variante proibida | Forma canônica |
|---|---|
| "deletar arquivo" | "mover para _APAGAR/" |
| "apagar pasta" | "mover para _APAGAR/" |
| "salvar sem perguntar" | "exportar com confirmação R1" |
| "skill genérica" | "capability transversal" |
| "modo padrão" | especificar qual modo (Create/Edit/etc) |
| "documento DOCX" | "arquivo DOCX corporativo" (se aplicar paleta) |
| "Excelentíssimo Senhor Juiz" | "Excelentíssimo Juízo" |
| "Excelentíssimo Senhor Doutor Juiz" | "Excelentíssimo Juízo" |
| "salário mínimo R$ 1.612" | "salário mínimo R$ 1.621" (2026) |
| "OJ 99 SDI-1 TST" | "Súmula 122 TST" (OJ 99 cancelada) |
| "tutela antecipada padrão" | "tutela de urgência sob comando explícito" (R4) |
| "não X, mas Y" | reformular afirmativamente |

---

## Atualização

Este glossário evolui com a arquitetura. Quando termo novo emerge:
1. Captura-se via gotcha-skill ou em sessão
2. Valida-se em 3 usos
3. Adiciona-se a esta reference
4. Aplica-se retroativamente em skills via modo Govern

## Termos de artefatos de skill

**MODELOS/**: pasta obrigatória em skills que produzem texto jurídico estruturado. Contém templates completos de output com ≥ 70% de conteúdo pronto e placeholders `[entre colchetes]` para dados do caso. Distinto de `references/` (documentação técnica) e de `examples/` (casos-teste para Claude).

**ASSETS/**: pasta obrigatória em skills que usam normas, cálculos ou checklists. Contém dados autossuficientes consumidos pela skill: normas indexadas, fórmulas com exemplos numéricos, checklists por fase, tabelas de referência, retórica e vocabulário. Cada arquivo legível sem depender dos demais da pasta.

**SCHEMAS/**: pasta obrigatória quando skill recebe input com 5+ campos estruturados. Contém schema JSON com campos obrigatórios/opcionais, `description`, `example`, `enum` e validação de tipos. Define o contrato entre quem chama a skill e o que ela espera.

**tests/**: pasta obrigatória quando `scripts/` existe. Contém `run_tests.py` e subpastas `caso-NN/` com `input.json` e `expected_output.md`. Permite verificar regressão ao atualizar scripts. Distinto de `examples/` (comportamento esperado do Claude) — `tests/` executa código Python real.

**templates/**: pasta opcional para skills que geram arquivos com estrutura fixa (`.env`, código boilerplate, documentos em branco com seções). Distinto de `MODELOS/` (texto jurídico completo) — `templates/` é estrutura de arquivo, não conteúdo jurídico.

## Termos de lições

**L9**: lição universal sobre encoding Python. Nunca omitir acentos em strings. Todo script com `# -*- coding: utf-8 -*-` na linha 2 e `encoding='utf-8'` explícito.

**L10**: lição universal sobre completude de artefatos. MODELOS/, ASSETS/, SCHEMAS/ obrigatórios quando aplicável. Pasta vazia é falha bloqueante.

**L11**: lição universal sobre Git sync. Pipeline pós-criação (§4-G) é parte obrigatória da entrega, não etapa manual opcional.

**LM1**: lição mod4-específica sobre pipeline zipfile. DOCX corporativo sempre via zipfile sobre template, nunca from-scratch.

**LM2**: lição mod4-específica sobre letterhead VML com parâmetros técnicos específicos.

## Distinções importantes

**examples/ vs tests/**: `examples/` documenta comportamento esperado do Claude em linguagem natural (para leitura humana e carregamento no contexto). `tests/` contém inputs reais para execução de scripts Python (para verificação automatizada de regressão).

**MODELOS/ vs references/**: `MODELOS/` tem texto jurídico completo pronto para uso (≥ 70% conteúdo). `references/` tem documentação técnica, normas, guias — material de consulta, não output direto.

**ASSETS/ vs assets/**: `ASSETS/` (maiúsculas, padrão AM) contém dados, normas, cálculos usados pela skill. `assets/` (minúsculas, padrão Anthropic) contém arquivos estáticos como imagens, fontes, templates de arquivo. Ambos podem coexistir.
