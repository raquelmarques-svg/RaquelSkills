# Template canônico V4 — esqueleto de SKILL.md

Este é o template usado pelo modo Create. Toda skill nova nasce desta estrutura.

## Frontmatter

```yaml
---
name: [kebab-case, ≤ 64 chars, minúsculas]
description: |
  [VERBO IMPERATIVO frase 1]. [QUANDO usar — 1-2 frases]. [GATILHOS linguísticos — 3-7 palavras-chave]. [PROIBIÇÃO INVERSA — quando NÃO usar].
project: ProjNN
nucleo: NN
frente: FN  # ou "transversal"
camada: CN
categoria: capability  # capability | preference | mista
justificativa: [1 linha sobre por que esta categoria]
depends_on:
  - skill-upstream-1
  - skill-upstream-2
chains_to:
  - skill-downstream-1
frentes_consultadas:
  - transversal
  - FN-frente
recursos_compartilhados:
  rotinas:
    - nome_rotina
  informacoes:
    - nome-informacao
  templates:
    - nome_template
  calculos:
    - nome_calculo
licoes_aplicadas: [L1, L3, L7]
regras_aplicaveis: [R1, R3, R10]
verificado_em: YYYY-MM-DD
version: 1.0.0
---
```

## Corpo

```markdown
# [nome-skill] — [descrição curta de 1 linha]

## §0 — Ativação e gates

[Quando esta skill responde, quando não responde. Se faz pergunta antes de proceder, listar as perguntas aqui.]

## §0-Regras universais aplicáveis a esta skill

[Cláusulas R1-R11 detectadas automaticamente. Ver reference 03.]

## §0-Leituras contextuais obrigatórias

Antes de produzir output, leio nesta ordem:
1. [Arquivo de configuração 1]
2. [Arquivo de glossário relevante]
3. [Dossiê de caso ativo, se aplicável]
4. [Matriz CAT-XX, se aplicável]

## §1 — Escopo

FAÇO:
- [Função 1]
- [Função 2]

NÃO FAÇO:
- [Exclusão 1]
- [Exclusão 2]

DELEGO PARA:
- [skill X (função X)]
- [skill Y (função Y)]

## §2 — Trigger semântico

Disparo quando o input contém:
| Núcleo | Exemplos |
|---|---|
| [tipo 1] | [exemplo] |
| [tipo 2] | [exemplo] |

Não disparo quando:
- [Cenário 1]
- [Cenário 2]

## §3 — Pipeline operacional

```
1. [Etapa 1]
2. [Etapa 2]
3. [Etapa 3]
...
N. [Output]
```

## §4 — Output canônico

[Descrever formato esperado de saída. Inline por padrão. DOCX/PDF apenas sob comando.]

## §5 — Casos-teste

Resumo dos 5 casos em `examples/`:

Positivos:
1. [Descrição do caso 1]
2. [Descrição do caso 2]
3. [Descrição do caso 3]

Negativos:
1. [Descrição do caso negativo 1]
2. [Descrição do caso negativo 2]

## §0 — Autopercepção (verificação leve pré-output)

Antes de produzir output, verifico:
1. O escopo do pedido cabe em §1 (FAÇO)?
2. Os dados mínimos estão disponíveis (DADO NECESSÁRIO)?
3. Estou dentro do limite de volume (≤ 500 linhas)?

Se 2+ pontos falham, sinalizo e aguardo antes de prosseguir.

## §6 — Calibração

VERIFICAR VIGÊNCIA: [normas com data — ex: SM 2026 = R$ 1.621,00]
VERIFICAR EXISTÊNCIA: [arquivos/dados necessários — ex: template, schema]
DADO NECESSÁRIO: [input mínimo obrigatório para esta skill funcionar]

## §7 — Auto-verificação

Última verificação: YYYY-MM-DD
Próxima verificação: YYYY-MM-DD (vencimento)

Checklist:
- [ ] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [ ] verificado_em ≤ 90 dias
- [ ] R1-R11 aplicáveis declaradas em §0-Regras
- [ ] §0-Autopercepção presente
- [ ] §1 com FAÇO/NÃO FAÇO/DELEGO PARA
- [ ] Calibração com VERIFICAR VIGÊNCIA/EXISTÊNCIA/DADO NECESSÁRIO
- [ ] 5 casos-teste em examples/ (3 positivos + 2 negativos)
- [ ] MODELOS/ com ≥ 70% conteúdo pronto (se skill produz texto jurídico)
- [ ] ASSETS/ autossuficientes (se skill usa normas/cálculos)
- [ ] SCHEMAS/ com description em campos (se input estruturado)
- [ ] tests/ com run_tests.py (se scripts/ existe)
- [ ] Tamanho dentro do limite (≤ 500 linhas SKILL.md)
- [ ] Vocabulário canônico respeitado

## §8 — Lições incorporadas

[L1, L3, L7 — citar cada uma e como aplica nesta skill]
```

## Estrutura de pastas

```
[nome-skill]/
├── SKILL.md                      ← obrigatório
├── references/                   ← obrigatório (≥ 1 arquivo)
│   └── 01-guia-recursos.md
├── MODELOS/                      ← obrigatório se produz texto jurídico
│   └── [secao_X.md]              ← ≥ 70% conteúdo pronto
├── ASSETS/                       ← obrigatório se usa normas/cálculos
│   └── [normas.md, calculos.md]  ← arquivos autossuficientes
├── SCHEMAS/                      ← obrigatório se input estruturado com 5+ campos
│   └── [nome]_input.schema.json
├── scripts/                      ← obrigatório se executa código Python
│   ├── funcao_1.py               ← L9: utf-8, acentos, argparse, main()
│   └── funcao_2.py
├── tests/                        ← obrigatório quando scripts/ existe
│   ├── run_tests.py
│   └── caso-01/
│       ├── input.json
│       └── expected_output.md
├── examples/                     ← obrigatório: 3 positivos + 2 negativos
│   ├── caso-positivo-1.md
│   ├── caso-positivo-2.md
│   ├── caso-positivo-3.md
│   ├── caso-negativo-1.md
│   └── caso-negativo-2.md
└── _backups/                     ← vazio inicialmente, preenchido por R3
```

## Convenções de nomeação

- Skill: `kebab-case` em minúsculas
- Reference: `NN-descritivo.md` (NN = ordem)
- Script: `verbo_objeto.py` (snake_case)
- Asset: `template_NOME.docx` ou `paleta_NOME.png`
- Example: `caso-[positivo|negativo]-N.md`

## Convenções de tamanho

| Arquivo | Ideal | Máximo |
|---|---|---|
| SKILL.md core | 300 linhas | 500 linhas |
| Frontmatter | 25 linhas | 40 linhas |
| §0 (ativação) | 30 linhas | 60 linhas |
| Reference | 150 linhas | 200 linhas |
| Modelo (MODELOS/) | 100 linhas | 200 linhas |
| Asset (ASSETS/) | 100 linhas | 200 linhas |
| Schema (SCHEMAS/) | 50 linhas | 150 linhas |
| Script | 200 linhas | 500 linhas |
| Caso-teste (examples/) | 40 linhas | 80 linhas |

## Convenções de description

Estrutura obrigatória em três componentes:

**Componente 1 — Verbo de ativação.**
Primeira palavra é verbo imperativo: Crie, Gere, Audite, Organize, Calcule, Monitor, etc.

**Componente 2 — Contexto.**
"INVOQUE quando..." + 1-2 frases descrevendo situação típica.

**Componente 3 — Gatilhos linguísticos.**
3-7 palavras-chave que disparam a skill.

**Componente 4 — Proibição inversa.**
"NÃO use para..." + 2-3 cenários onde a skill não deve disparar.

Exemplo canônico:

```yaml
description: |
  Crie petição inicial de mandado de segurança contra ato de autoridade
  pública federal ou estadual. INVOQUE quando Raquel pedir redigir MS,
  preparar writ, contestar ato coator, ou impetrar segurança. Gatilhos:
  "mandado de segurança", "MS", "writ", "ato coator", "autoridade",
  "ilegalidade ou abuso". NÃO use para: ações ordinárias (delego para
  C5 específica), recursos (C5 recursos), tutela cautelar (skill
  específica), nem para análise de cabimento (analise-precedente).
```
