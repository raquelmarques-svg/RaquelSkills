# skill-creator-am / reference 03 — Artefatos obrigatórios por tipo de skill

Esta reference detalha o que vai em cada pasta além do SKILL.md. O §4 do SKILL.md contém o sumário; este arquivo contém o detalhe operacional.

## references/ — módulos de referência

Cada arquivo ≤ 200 linhas. O SKILL.md é o índice; as references/ são o conteúdo técnico denso.

Arquivos típicos:

| Arquivo | Conteúdo |
|---|---|
| `01-guia-recursos.md` | Mapa de recursos por tarefa + ordem de leitura obrigatória + o que a skill NÃO cobre |
| `02-pipeline-tecnico.md` | Fluxo de execução detalhado com exemplos de código (para skills com scripts) |
| `03-normas.md` | Base normativa indexada por tema: lei, artigo, ementa, aplicação ao caso |
| `04-calibracao.md` | Valores variáveis com data de referência (SM, tetos, índices, prazos) |

Regra: se o SKILL.md tem mais de 30% do conteúdo de uma seção copiado de outro arquivo da biblioteca, mover para references/.

## MODELOS/ — templates de output

### Critério de obrigatoriedade

Obrigatório quando a skill produz qualquer texto jurídico estruturado: petição, seção de peça, manifestação, quesitação, análise, relatório.

### Padrão de qualidade

Cada modelo deve ter ≥ 70% do conteúdo pronto. Placeholder `[entre colchetes]` para dados do caso concreto. Placeholder > 30% = modelo incompleto = falha bloqueante.

### Estrutura interna obrigatória de cada modelo

```markdown
# Modelo — [Nome da seção/peça]

## Quando usar
[Condição exata que dispara este modelo. Ex: "Quando o INSS não impugnou fato específico"]

## Estrutura
[Texto completo pronto, com placeholders apenas onde o dado do caso entra]

## Instruções de preenchimento
[O que substituir, como identificar o dado, armadilhas a evitar]

## Variantes
[Versões alternativas para cenários diferentes do caso padrão]
```

### Exemplos por tipo de skill

| Skill | MODELOS/ esperados |
|---|---|
| replica | secao_admissao_ficta, secao_ntep (3 variantes), secao_vicio_especie (2 variantes), secao_impugnacao_laudo (Tipo B e C), pedidos_replica |
| ms | qualificacao_autoridade, fumus_boni_iuris, periculum_in_mora, pedido_liminar, pedidos_definitivos |
| pericia-acidentaria | quesitacao_inicial, quesitacao_complementar, impugnacao_laudo, manifestacao_pos_laudo |
| alimentos | calculo_base_alimentar, secao_necessidade, pedido_provisorio, pedido_definitivo |
| revisao-juridica | checklist_peticao_inicial, checklist_recurso, checklist_manifestacao |

## ASSETS/ — dados, normas, cálculos

### Critério de obrigatoriedade

Obrigatório quando a skill: (a) aplica normas específicas, (b) realiza cálculos, (c) usa checklists de verificação, (d) opera com vocabulário controlado ou retórica específica.

### Categorias e conteúdo esperado

**Normas** (`normas_X.md`):
- Artigos relevantes com texto integral ou resumo preciso
- Jurisprudência indexada por tema com referência completa (tribunal, número, relator, data, ementa)
- Distinção clara entre norma vigente e norma revogada

**Cálculos** (`calculos_X.md`):
- Fórmula explícita com cada variável definida
- Exemplo numérico completo com valores preenchidos
- Casos de borda e exceções
- Referência normativa para cada componente do cálculo

**Checklists** (`checklist_X.md`):
- Organizado em blocos por fase ou tema
- Cada item binário (sim/não) ou com opções fechadas
- Instrução de uso acima de cada bloco
- Tabela de teses comuns com classificação e resposta padrão (quando aplicável)

**Dados estruturados** (`cadeia_X.md`, `tabela_X.md`):
- Tabelas com cabeçalho descritivo
- Fontes citadas
- Data de referência explícita para dados mutáveis

**Retórica** (`framing_X.md`):
- Frame dominante declarado
- Movimentos argumentativos numerados com exemplos de expressões
- Vocabulário controlado: termo técnico correto × termos a evitar
- Erros retóricos catalogados com explicação do dano

## SCHEMAS/ — contratos de input

### Critério de obrigatoriedade

Obrigatório quando: (a) a skill recebe mais de 5 campos de dados do caso, ou (b) a skill gera texto a partir de dados estruturados, ou (c) a skill tem pipeline com script Python que precisa de input.

### Padrão mínimo do schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "[NomeSkill]Input",
  "description": "Dados de entrada para [função da skill]",
  "type": "object",
  "required": ["campo1", "campo2"],
  "properties": {
    "campo1": {
      "type": "string",
      "description": "O que este campo representa",
      "example": "Valor de exemplo concreto"
    }
  }
}
```

Campos com valores fixos usam `enum`. Campos de data usam `"format": "date"`. Campos numéricos declaram se são `integer` ou `number`.

## scripts/ — código Python

### Critério de obrigatoriedade

Obrigatório quando a skill: (a) gera DOCX via zipfile, (b) processa arquivos, (c) realiza cálculos que dependem de iteração ou dados externos, (d) valida output.

### Padrão de cabeçalho obrigatório

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Nome do script] — [função em uma linha]

Uso: python3 script.py --input /caminho/input.json --output /caminho/output.ext
"""
```

### Regras críticas

- L9: nunca omitir acentos. Todas as strings com acentuação completa.
- `encoding='utf-8'` explícito em todo `open()`, `read_text()`, `write_text()`.
- `argparse` com `--input`, `--output`, `--config` (quando aplicável).
- `try/except` com mensagem de erro clara ao usuário, não stack trace bruto.
- `main()` isolada, chamada por `if __name__ == '__main__': main()`.
- Verificação visual do output obrigatória antes de entregar ao usuário.

## examples/ — casos-teste

### Padrão obrigatório de cada caso

```markdown
## Caso [positivo/negativo] N — [título descritivo concreto]

**Contexto:** [o que a usuária disse ou fez — específico, com dados]

**Comportamento esperado:**
1. [passo verificável]
2. [passo verificável]
...

**Output esperado:** [o que aparece para a usuária — específico]
```

### Distribuição obrigatória

3 positivos: uso padrão + variante com dado faltante resolvido + variante com dado complexo.
2 negativos: o que a skill NÃO faz (com o comportamento correto descrito, não apenas "recusa").

Proibido: caso com "input válido → output correto" sem dados concretos.
Proibido: caso negativo que descreve apenas o bloqueio sem descrever o que a skill faz em vez disso.

## Checklist de completude (auditoria pós-criação)

Para cada pasta declarada no frontmatter em `recursos_compartilhados`:

- [ ] Pasta existe com ≥ 1 arquivo de conteúdo real
- [ ] MODELOS/: cada arquivo tem ≥ 70% de conteúdo pronto
- [ ] ASSETS/: cada arquivo é autossuficiente (legível sem depender de outro)
- [ ] SCHEMAS/: campos obrigatórios declarados com `description`
- [ ] scripts/: cabeçalho UTF-8, argparse, main() isolada
- [ ] examples/: 3 positivos + 2 negativos com dados concretos
- [ ] references/: ≤ 200 linhas cada, sem duplicação do SKILL.md
