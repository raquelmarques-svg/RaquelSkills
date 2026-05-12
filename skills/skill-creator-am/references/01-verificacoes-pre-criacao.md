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
```

Se todos OK, prosseguir. Senão, devolver alertas e pedir ajuste.
