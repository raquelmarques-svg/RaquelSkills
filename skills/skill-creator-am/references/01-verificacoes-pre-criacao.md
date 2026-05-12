# 7 Verificações pré-criação — detalhamento operacional

Cada verificação é bloqueante. Se falha, criação não procede até resolução.

## Verificação 1 — Duplicidade na biblioteca

Objetivo: evitar criar skill que sobrepõe função já existente.

### Procedimento

1. Listar todas as skills em `C:\RaquelSkills\skills\`
2. Para cada skill existente, ler:
   - `description` (campo do frontmatter)
   - `name` (nome canônico)
3. Comparar com nome e descrição da skill proposta
4. Calcular similaridade textual em duas dimensões:
   - Nome: distância de Levenshtein
   - Descrição: similaridade fuzzy de palavras-chave

### Critérios de bloqueio

- Nome idêntico: bloqueio absoluto
- Nome com Levenshtein ≤ 3: alerta amarelo, pergunta confirmação
- Descrição com similaridade > 60%: alerta vermelho, bloqueio
- Gatilhos linguísticos sobrepostos a outra skill: alerta vermelho

### Critérios de aprovação

- Nome único na biblioteca
- Descrição com similaridade < 40% com todas as existentes
- Gatilhos linguísticos exclusivos

### Caso de exceção: skill split

Se a skill nova for resultado de split de skill existente (ex.: `replica` → `replica-analise` + `replica-redacao`), informar a origem no campo `depends_on` ou em comentário, e a verificação não bloqueia.

## Verificação 2 — Coordenadas declaradas

Objetivo: garantir que a skill tem localização inequívoca nas 4 dimensões.

### Procedimento

Confirmar presença obrigatória de:
- `project: ProjNN` (1-7, conforme arquitetura V4)
- `nucleo: NN` (N1-N6)
- `frente: FN` (F1-F6 ou "transversal")
- `camada: CN` (C0-C9)

### Critérios de bloqueio

- Qualquer coordenada ausente: bloqueio
- Project não confirmado (Proj01, Proj06, Proj07 estão pendentes): alerta amarelo
- Camada incoerente com função (ex.: skill que produz peça em C2): bloqueio

### Validação cruzada

- C5 (matéria) deve ser F1-F4 (frentes de prática)
- C0 (transversal) deve ser frente "transversal"
- C8 (protocolo) tipicamente Proj05 (Astrea/Controladoria)

## Verificação 3 — Categoria declarada

Objetivo: classificar skill como capability, preference ou mista.

### Definições

- **Capability**: skill que faz algo. Produz output concreto. Outras skills podem chamá-la.
- **Preference**: skill que configura comportamento. Não produz output isolado. Ajusta como outras operam.
- **Mista**: faz e configura. Raras; exigir justificativa robusta.

### Procedimento

Pedir explicitamente:
- `categoria: capability|preference|mista`
- `justificativa: [1 linha]`

### Critérios de bloqueio

- Categoria ausente: bloqueio
- "Mista" sem justificativa robusta: bloqueio
- Categoria incoerente com escopo declarado: alerta vermelho

### Exemplos canônicos

- `mod4`: capability (formata DOCX)
- `padrao-redacional`: preference (configura redação)
- `dossie-caso`: capability (gera RESUMO-DO-CASO)
- `governanca-skills`: mista (audita + configura ciclos)

## Verificação 4 — Trigger único

Objetivo: descrição com gatilhos linguísticos que não sobrepõem a outras skills.

### Procedimento

1. Extrair gatilhos da descrição proposta (palavras-chave de ativação)
2. Comparar com gatilhos de todas as skills existentes
3. Calcular sobreposição

### Critérios de bloqueio

- Mais de 50% dos gatilhos sobrepõem a outra skill: bloqueio
- 30-50% de sobreposição: alerta amarelo, pede ajuste
- Verbos genéricos sem objeto ("analisar", "verificar"): bloqueio até especificar

### Princípio

70% da performance da skill mora na descrição. Gatilhos devem ser:
- Específicos (não "criar arquivo" mas "criar SKILL.md")
- Diretos (verbo + objeto)
- Coletados (3-7 variações que disparam)
- Exclusivos (não duplicar outros)

## Verificação 5 — Tamanho estimado

Objetivo: prever se skill nascerá dentro do limite saudável.

### Procedimento

A partir do escopo declarado, estimar:
- Linhas de SKILL.md core
- Quantidade de seções (§0-§N)
- Quantidade de references previstas
- Quantidade de scripts previstos

### Critérios de bloqueio

- Estimativa de SKILL.md > 500 linhas sem plano de modularização: bloqueio
- Mais de 8 references sem justificativa: alerta amarelo
- Mais de 5 scripts sem plano: alerta amarelo
- Lógica condicional excessiva (>10 if/then) sem tabela de decisão: alerta amarelo

### Aprovação condicional

Se estimativa > 500 linhas mas com plano explícito de:
- Modularização em N references
- Distribuição de lógica em scripts
- Tabelas de decisão em vez de if/then

Aprovado com avaliação na auditoria pós-criação.

## Verificação 6 — Dependências mapeadas

Objetivo: garantir que upstream/downstream da skill estão declarados.

### Procedimento

Pedir explicitamente:
- `depends_on: [lista de skills que alimentam esta]`
- `chains_to: [lista de skills que esta alimenta]`

### Critérios de bloqueio

- Ambos campos vazios sem justificativa: bloqueio (skill isolada é suspeita)
- Dependência apontando para skill inexistente: bloqueio
- Cadeia circular detectada (A→B→A): bloqueio

### Validação cruzada

Verificar nas skills apontadas:
- A skill upstream declara esta no seu `chains_to`?
- A skill downstream declara esta no seu `depends_on`?

Inconsistência: alerta amarelo, sugerir ajuste em ambas.

## Verificação 7 — Casos-teste definidos

Objetivo: garantir que skill nasce testável.

### Procedimento

Pedir 5 casos:
- 3 positivos: input típico que deve funcionar
- 2 negativos: input que deve ser recusado ou alertado

### Critérios de bloqueio

- Menos de 5 casos: bloqueio
- Casos vagos ("funciona com qualquer input"): bloqueio
- Casos negativos ausentes ou triviais: bloqueio

### Formato canônico

Cada caso em `examples/`:

```markdown
# Caso [positivo|negativo] N

## Input
[descrição do input]

## Comportamento esperado
[o que a skill deve fazer]

## Output esperado
[trecho exemplo do output ou indicação clara]

## Critério de aprovação
[como verificar que passou]
```

## Verificação 8 — Análise semântico-funcional-pragmática (decomposição de escopo)

**Aplica em:** Create, Edit, Govern, Refactor, Diagnóstico — toda operação que toca o escopo de uma skill.

Objetivo: garantir que a skill faz uma coisa só, que seus gatilhos ativam apenas quando deveriam, e que nenhuma função declarada pertence a outra camada ou já existe na biblioteca.

Esta verificação é a mais importante do conjunto. Uma skill com escopo múltiplo corrompido não falha ruidosamente — falha silenciosamente: ativa quando não deveria, produz output inconsistente, e resiste a refatoração futura.

---

### Dimensão 1 — Análise semântica dos gatilhos

Pergunta: **Os gatilhos desta skill são exclusivos desta skill, ou poderiam ativar outras skills ou outros contextos?**

Procedimento:
1. Listar todos os gatilhos declarados na `description` (explícitos) e no §0 (implícitos)
2. Para cada gatilho, testar mentalmente em 5 contextos distintos:
   - Contexto A: BPC/LOAS
   - Contexto B: benefício previdenciário B31/B87/B91
   - Contexto C: ação trabalhista
   - Contexto D: ação cível/família
   - Contexto E: processo administrativo não-previdenciário
3. Se o gatilho dispara em mais de 2 contextos distintos → gatilho ambíguo

Critérios de bloqueio:
- Gatilho que dispara em ≥ 3 contextos sem discriminador: **bloqueio vermelho**
- Mais de 50% dos gatilhos ambíguos: **bloqueio absoluto**
- Gatilho usando verbo genérico sem objeto específico ("analisar", "verificar", "mapear"): **alerta vermelho**

Exemplos de gatilhos problemáticos:
- "o que entrou no cálculo" → ativa para BPC, B31, alimentos, liquidação — ambíguo
- "de onde veio esse valor" → idem
- "qual documento prova isso" → qualquer processo jurídico
- "erro no cálculo" → qualquer cálculo contestado

Exemplos de gatilhos corretos:
- "renda per capita BPC" → específico
- "Detalhe da Análise INSS" → específico (seção de documento do processo BPC)
- "SM usado pelo INSS no indeferimento" → específico
- "CadÚnico desatualizado" → específico (instrumento BPC/LOAS)

Discriminadores que resolvem ambiguidade:
- Objeto específico: "cálculo de renda per capita" em vez de "cálculo"
- Instrumento específico: "CadÚnico", "Detalhe da Análise", "NB BPC"
- Norma específica: "art. 20 LOAS", "Decreto 12.534/2025"
- Processo específico: "indeferimento por renda BPC"

---

### Dimensão 2 — Análise funcional das responsabilidades

Pergunta: **Cada função declarada no §1 (FAÇO) pertence à mesma camada e ao mesmo núcleo?**

Procedimento:
1. Listar cada função do FAÇO
2. Para cada função, atribuir: camada (C0-C9) + núcleo (N1-N6)
3. Se há funções em camadas diferentes → candidato a split

Mapeamento camada × função típica:
| Camada | Função típica |
|---|---|
| C0 | Formatação gráfica, output visual, templates transversais |
| C1 | Intake, triagem, onboarding de caso |
| C2 | Organização de pastas, renomeação, arquivamento |
| C3 | Levantamento factual, extração de dados de documentos |
| C4 | Análise jurídica, classificação de vícios, comparação normativa |
| C5 | Redação de peça processual, argumentação, petição |
| C6 | Revisão de texto, checagem de conformidade |
| C7 | Formatação de documento final (DOCX corporativo) |
| C8 | Protocolo, prazos, controle de fluxo processual |
| C9 | Pós-processo, execução, cumprimento |

Critérios de bloqueio:
- Funções em ≥ 3 camadas distintas: **bloqueio absoluto**
- Funções em 2 camadas distintas: **bloqueio vermelho** salvo justificativa explícita de que são inseparáveis
- Função de C0 (visual/gráfico) misturada com C4 (análise): **bloqueio absoluto** — sempre separáveis
- Função de C3 (extração) misturada com C5 (redação): **bloqueio absoluto**

Perguntas de diagnóstico:
- "Se eu remover a geração de PNG desta skill, o cálculo ainda funciona?" → Se sim, o PNG pertence a outra skill
- "Se eu remover a análise jurídica desta skill, o recorte de PDF ainda funciona?" → Se sim, o recorte pertence a outra skill
- "Esta função seria útil em outros processos além dos desta skill?" → Se sim, é candidata a skill transversal

---

### Dimensão 3 — Análise pragmática do uso real

Pergunta: **Em uso real, quem chama esta skill e para quê? O escopo reflete isso?**

Procedimento:
1. Descrever o usuário típico no momento da invocação (Raquel, no meio de uma sessão de trabalho)
2. Descrever o que ela tem em mãos (documentos, dados, contexto)
3. Descrever o que ela precisa como output imediato
4. Verificar se a skill entrega exatamente isso — nem mais, nem menos

Perguntas de diagnóstico pragmático:
- "Raquel pediria análise de cálculo E geração de PNG na mesma invocação, sempre?" → Se não, são invocações separadas → skills separadas
- "O output desta skill é consumido por quem? Em que momento?" → Identifica o `chains_to` correto
- "Esta skill seria invocada no meio da redação de uma petição, ou antes de começar?" → Define a camada
- "Há contexto que a skill precisa mas que não foi informado explicitamente?" → Identifica gate de entrada faltante

Critérios de bloqueio:
- Skill cujo output parcial (ex: só a análise textual) é o uso real mais frequente, mas o pipeline sempre executa o todo: **alerta vermelho** (ineficiência estrutural)
- Skill que precisa de confirmação R1 no meio do pipeline: sintoma de que a parte pesada é uma skill separada
- Skill que tem "modo lite" e "modo completo": são duas skills

---

### Dimensão 4 — Verificação de duplicação funcional na biblioteca

Pergunta: **Alguma função desta skill já existe, total ou parcialmente, em outra skill instalada?**

Vai além da V1 (duplicidade de nome/descrição): verifica sobreposição funcional mesmo quando os nomes são distintos.

Procedimento:
1. Para cada função do FAÇO, buscar na biblioteca: qual skill poderia fazer isso?
2. Se skill existente cobre ≥ 50% da função: candidata a delegação via `depends_on` ou `chains_to`
3. Se script ou asset é genérico (funciona para qualquer processo): candidato a `_compartilhados/`

Critérios de bloqueio:
- Função já coberta por skill existente sem diferenciação clara: **bloqueio vermelho**
- Script genérico hardcoded nesta skill em vez de `_compartilhados/`: **alerta amarelo**
- Asset (sm_historico.md, normas.md) que outras skills também usariam: **alerta amarelo** → mover para `_compartilhados/`

---

### Síntese — checklist V8

```
Dimensão 1 — Semântica dos gatilhos:
[ ] D1.1: Cada gatilho dispara em ≤ 2 contextos distintos
[ ] D1.2: < 50% dos gatilhos são ambíguos
[ ] D1.3: Nenhum gatilho com verbo genérico sem objeto específico
[ ] D1.4: Discriminadores de contexto presentes nos gatilhos ambíguos

Dimensão 2 — Funcional (camadas):
[ ] D2.1: Todas as funções do FAÇO são da mesma camada (ou adjacentes com justificativa)
[ ] D2.2: Nenhuma função de C0 (visual) misturada com C4+ (análise/redação)
[ ] D2.3: Nenhuma função de C3 (extração) misturada com C5 (redação)
[ ] D2.4: Se funções em 2 camadas: justificativa de inseparabilidade explícita

Dimensão 3 — Pragmática:
[ ] D3.1: O escopo reflete o uso real mais frequente (não o mais completo)
[ ] D3.2: Não há "modo lite vs. completo" — são skills distintas
[ ] D3.3: R1 não ocorre no meio do pipeline (sintoma de skill composta)
[ ] D3.4: Output é atomicamente útil (não requer a skill inteira para ter valor)

Dimensão 4 — Duplicação funcional:
[ ] D4.1: Nenhuma função já coberta por skill existente
[ ] D4.2: Scripts genéricos estão em _compartilhados/, não aqui
[ ] D4.3: Assets compartilháveis estão em _compartilhados/

Dimensão 5 — Contrato de interface (SRP + DIP):
[ ] D5.1: Schema de input declarado ou planejado
[ ] D5.2: Schema de output declarado ou planejado
[ ] D5.3: produced_by e consumed_by identificados
[ ] D5.4: SLA declarável (tempo, output garantido, condições de falha)
[ ] D5.5: Skill é substituível por outra com mesmo schema? (Liskov)

V8 aprovada: todos os itens verdes.
V8 reprovada: qualquer vermelho → bloquear e propor split antes de prosseguir.
```

---

### Protocolo de split (quando V8 reprova)

Quando V8 identifica funções em camadas diferentes:

1. **Nomear** cada skill candidata com escopo preciso
2. **Mapear** qual função do FAÇO vai para qual skill
3. **Identificar** scripts e assets compartilhados → mover para `_compartilhados/`
4. **Declarar** `chains_to` e `depends_on` entre as skills resultantes
5. **Recriar** cada skill via Create com V1-V8 aplicadas individualmente
6. **Arquivar** a skill original em `_APAGAR/` com nota de split

Nunca criar skill nova sem resolver o split primeiro. Split pendente é bloqueio.

## Verificação 9 — Blueprint arquitetural (SOLID + DDD + ITIL/COBIT)

**Aplica em:** Create, Refactor — toda operação que gera SKILL.md novo.

Objetivo: garantir que a skill está corretamente desenhada antes de ser codificada. Um SKILL.md escrito sem blueprint é como uma petição sem análise prévia do caso.

### Passo 1 — Cartão CRC (Class-Responsibility-Collaboration)

Preencher obrigatoriamente antes de gerar qualquer arquivo:

| Campo | Conteúdo |
|---|---|
| Nome | `[kebab-case]` |
| Responsabilidade | `[uma frase: verbo + objeto + contexto]` |
| Upstream (quem me alimenta) | `[skill + schema]` |
| Downstream (quem me consome) | `[skill + schema]` |
| Não-responsabilidade explícita | `[o que esta skill NÃO faz]` |

Se a "Responsabilidade" precisar de "e" para ser completa → SRP violado → split antes de prosseguir.

### Passo 2 — Verificação SOLID

| Princípio | Pergunta | Critério |
|---|---|---|
| SRP | A skill faz uma coisa? | "Responsabilidade" tem no máximo um verbo |
| OCP | O schema é extensível sem quebrar? | Campos novos são opcionais |
| LSP | É substituível por skill do mesmo tipo? | Mesmo schema de input/output |
| ISP | O schema tem apenas o necessário? | < 10 campos obrigatórios |
| DIP | Depende de schemas, não de skills concretas? | `depends_on` aponta para schemas, não implementações |

### Passo 3 — Bounded Context

- A skill pertence a um único bounded context (frente F1-F6 ou transversal)?
- Termos do domínio estão no glossário (reference 08)?
- O aggregate root do fluxo está identificado?

### Passo 4 — ITIL Value Check

- O valor entregue é mensurável? ("economiza X minutos em caso tipo Y")
- A skill tem escopo mínimo viável ou está tentando cobrir tudo?
- O SLA é declarável?

### Passo 5 — COBIT CI Check

- O CI (skill) está planejado para entrar no `_inventario.md`?
- O impacto em skills downstream foi analisado?
- A versão inicial é `1.0.0` com plano de extensão futuro documentado?

### Critérios de bloqueio V9

- Cartão CRC não preenchido: **bloqueio absoluto**
- SRP violado (responsabilidade com "e"): **bloqueio absoluto** → split
- Schema de input não planejado para skill com 5+ campos de entrada: **bloqueio vermelho**
- Bounded context não identificado: **bloqueio vermelho**
- SLA não declarável: **alerta amarelo**


---

## Síntese — checklist operacional

Antes de gerar SKILL.md:

```
[ ] V1: Não há duplicação com biblioteca atual
[ ] V2: 4 coordenadas declaradas
[ ] V3: Categoria + justificativa
[ ] V4: Gatilhos linguísticos exclusivos
[ ] V5: Tamanho estimado dentro do limite (ou plano de modularização)
[ ] V6: depends_on + chains_to mapeados
[ ] V7: 5 casos-teste definidos (3 positivos + 2 negativos)
[ ] V8: Análise semântico-funcional-pragmática aprovada (5 dimensões)
[ ] V9: Blueprint arquitetural aprovado (CRC + SOLID + DDD + ITIL/COBIT)
```

Se todos OK, prosseguir. Senão, devolver alertas e pedir ajuste.
