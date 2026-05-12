# Caso positivo 4 — Criar skill `alimentos` com MODELOS/ e ASSETS/ completos

## Input

Raquel: "criar skill alimentos para calcular base alimentar e redigir petições de alimentos (fixação, revisão, execução). Precisa cobrir: binômio necessidade-possibilidade, cálculo de 1/3 da renda, tabela de despesas, pedido liminar de alimentos provisórios."

## Comportamento esperado

A skill-creator-am aplica §0-Ativação, 7 verificações pré, e na geração (§4), cria obrigatoriamente MODELOS/ e ASSETS/ além de SKILL.md e examples/.

### Fluxo detalhado

**§0-Ativação — 6 perguntas:**
- Nome: `alimentos` (kebab-case ✓)
- Problema: redigir petições de alimentos e calcular base alimentar
- Coordenadas: Proj02 / N3 / F4 / C5
- Categoria: capability (produz peça processual)
- depends_on: dossie-caso, levanta-fatos
- chains_to: revisao-juridica, mod4
- Gatilhos: "alimentos", "fixar alimentos", "revisar alimentos", "execução de alimentos", "binômio", "1/3 da renda"
- Não-disparo: guarda e visitação (skill separada), inventário (outro escopo)

**7 verificações:** todas verdes (skill existente na biblioteca tem escopo diferente — verificar_duplicacao.py confirma < 40% similaridade).

**§4-B — MODELOS/ gerados:**

| Arquivo | Conteúdo |
|---|---|
| `secao_necessidade.md` | Texto completo da seção "DAS NECESSIDADES DA ALIMENTANDA" com placeholders para valores de despesas por categoria |
| `secao_possibilidade.md` | Texto completo "DA POSSIBILIDADE DO ALIMENTANTE" com placeholders para renda e deduções |
| `pedido_liminar.md` | Seção de tutela de urgência (não incluída por padrão — R4 — disponível sob comando) |
| `pedidos_definitivos.md` | Lista de pedidos com alíneas a-g, 70% preenchidas |
| `calculo_base.md` | Memória de cálculo com fórmula + exemplo numérico preenchido |

**§4-C — ASSETS/ gerados:**

| Arquivo | Conteúdo |
|---|---|
| `normas_alimentos.md` | CC arts. 1.694-1.710, CPC arts. 528-533, Lei 5.478/68, jurisprudência STJ indexada por tema |
| `tabela_despesas.md` | Categorias de despesas reconhecidas (moradia, alimentação, saúde, educação, transporte, lazer) com valores de referência |
| `calculos_alimentos.md` | Fórmulas: 1/3 da renda líquida, percentual sobre salário bruto, dedução de encargos obrigatórios; 3 exemplos numéricos completos |
| `checklist_documentos.md` | Lista de documentos por tipo de ação (fixação, revisão, execução) |

**§4-D — SCHEMAS/:**
- `alimentos_input.schema.json` com campos: partes, renda_alimentante, despesas_alimentanda, tipo_acao, pedido_liminar

**§4-F — examples/:** 5 casos (fixação inicial, revisão majoração, revisão redução, execução, caso negativo sem renda comprovada)

**12 auditorias pós-criação:**
- A13 (artefatos): MODELOS/ com 5 arquivos, cada um ≥ 70% conteúdo pronto ✓
- A14 (tests): scripts/ tem `calcular_base.py` → tests/ tem run_tests.py + 2 casos ✓
- Demais: todas verdes

**§4-G — Git sync:**
```
feat(alimentos): v1.0.0 — V4 completa, MODELOS+ASSETS+SCHEMAS+tests
```

## Output esperado

```
✅ Skill alimentos criada — v1.0.0
   Estrutura:
   alimentos/
   ├── SKILL.md (298 linhas)
   ├── MODELOS/ (5 arquivos, todos ≥ 70% conteúdo)
   ├── ASSETS/ (4 arquivos, autossuficientes)
   ├── SCHEMAS/ (1 schema com campos obrigatórios)
   ├── scripts/ (calcular_base.py)
   ├── tests/ (run_tests.py + 2 casos)
   ├── references/ (01-guia-recursos.md)
   └── examples/ (5 casos)

   Auditorias: 14/14 aprovadas
   Git: feat(alimentos): v1.0.0 — commitado (hash: xxxxxxx)
```

## Critério de aprovação

- MODELOS/ criados com conteúdo real (não apenas cabeçalhos)
- Cada modelo com instrução de uso + texto completo + variantes
- ASSETS/ autossuficientes por arquivo
- SCHEMAS/ com `description` em cada campo
- tests/ com run_tests.py e ≥ 2 casos
- Auditoria A13 aprovada sem falhas
- Git sync executado (§4-G)

## Erros que invalidariam o teste

- MODELOS/ criados apenas com cabeçalhos e placeholders (< 70% conteúdo)
- ASSETS/ ausentes ou com apenas lista de tópicos
- SCHEMAS/ ausente quando input tem 5+ campos
- Auditoria A13 não executada
- Git sync omitido (L11 violada)
