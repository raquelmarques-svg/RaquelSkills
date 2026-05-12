# skill-creator-am / reference 14 — Contratos de interface

Uma skill sem contrato declarado é uma caixa-preta sem API. Quem a chama não sabe o que passar. Quem a consome não sabe o que esperar. Esta reference define como contratos de interface são criados, versionados e verificados.

---

## O que é um contrato de interface

Um contrato de interface define:
1. **Input contract** — o que a skill recebe (schema JSON de entrada)
2. **Output contract** — o que a skill entrega (schema JSON de saída)
3. **Preconditions** — o que deve ser verdadeiro antes de invocar
4. **Postconditions** — o que é garantido após execução bem-sucedida
5. **Invariants** — o que nunca muda durante a execução
6. **SLA** — tempo, qualidade e condições de falha

---

## Onde vivem os contratos

```
_compartilhados/SCHEMAS/
├── input/
│   ├── dossie_caso.v1.schema.json       ← input canônico do aggregate root
│   ├── calculo_renda_bpc.v1.schema.json ← input de analise-renda-bpc
│   ├── analise_pericial.v1.schema.json  ← output de pericia-* / input de replica
│   └── blocos_visuais.v1.schema.json    ← output de analise-* / input de widget-visual
└── output/
    ├── petica_estruturada.v1.schema.json ← output de skills C5
    ├── analise_textual.v1.schema.json    ← output de skills C4
    └── docx_corporativo.v1.schema.json  ← output de mod4
```

Schemas de input e output compartilhados ficam em `_compartilhados/SCHEMAS/`. Schemas específicos de uma skill ficam em `SCHEMAS/` dentro da skill.

---

## Estrutura padrão do schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "analise_renda_bpc.v1",
  "title": "Análise de Renda BPC — Input",
  "description": "Input para analise-renda-bpc. Produzido por dossie-caso ou fornecido diretamente.",
  "version": "1.0.0",
  "produced_by": ["dossie-caso"],
  "consumed_by": ["analise-renda-bpc"],
  "type": "object",
  "required": ["processo_pdf_path", "data_decisao", "nb_bpc"],
  "properties": {
    "processo_pdf_path": {
      "type": "string",
      "description": "Caminho absoluto para o PDF do processo administrativo BPC",
      "example": "C:/Clientes/Maria/processo_bpc_nb123.pdf"
    },
    "data_decisao": {
      "type": "string",
      "format": "date",
      "description": "Data da decisão de indeferimento no formato YYYY-MM-DD. Determina o SM vigente.",
      "example": "2026-02-05"
    },
    "nb_bpc": {
      "type": "string",
      "pattern": "^[0-9]{10}-[0-9]$",
      "description": "Número do benefício BPC no formato NNN.NNN.NNN-N",
      "example": "725.636.927-2"
    }
  },
  "additionalProperties": false
}
```

---

## Versionamento de contratos

Segue semver com regras estritas:

| Mudança | Versão | Impacto |
|---|---|---|
| Adicionar campo opcional | MINOR (1.0 → 1.1) | Sem quebra — consumers ignoram campo novo |
| Remover campo | MAJOR (1.x → 2.0) | Quebra — consumers dependem do campo |
| Mudar tipo de campo | MAJOR (1.x → 2.0) | Quebra — consumers esperam tipo diferente |
| Mudar nome de campo | MAJOR (1.x → 2.0) | Quebra — consumers referenciam nome antigo |
| Adicionar campo obrigatório | MAJOR (1.x → 2.0) | Quebra — producers atuais não enviam o campo |

Quando uma mudança é MAJOR:
1. Criar `v2.schema.json` sem remover `v1.schema.json`
2. Declarar `deprecated_at` no schema v1
3. Notificar todas as skills em `consumed_by` do schema v1
4. Dar prazo de migração (próxima auditoria R9)

---

## Preconditions, Postconditions, Invariants

Declarados no §0-Autopercepção de cada skill:

```markdown
## §0 — Contrato de execução

Preconditions (devem ser verdadeiras antes de executar):
- PDF do processo disponível e legível
- Data da decisão presente no documento ou informada explicitamente
- NB BPC válido

Postconditions (garantidas após execução bem-sucedida):
- JSON de análise conforme `analise_renda_bpc.v1.schema.json` entregue
- Pelo menos 1 vício identificado e classificado por autonomia
- SM verificado contra `_compartilhados/ASSETS/sm_historico.md`

Invariants (nunca mudam durante execução):
- SM usado é sempre o da data da decisão, não do ano corrente
- Parcelas sem documento de fonte pagadora são sempre classificadas como vício
- Output nunca contém dado inventado — ausência de dado = campo null com flag "não encontrado"
```

---

## Checklist de contrato (auditoria A15)

```
[ ] CT-1: Schema de input existe e está em SCHEMAS/ ou _compartilhados/SCHEMAS/
[ ] CT-2: Schema de output existe e está declarado
[ ] CT-3: produced_by e consumed_by declarados no schema
[ ] CT-4: Campos obrigatórios têm description e example
[ ] CT-5: Campos enum têm todos os valores possíveis listados
[ ] CT-6: Version do schema segue semver
[ ] CT-7: Preconditions declaradas no §0
[ ] CT-8: Postconditions declaradas no §0
[ ] CT-9: SLA declarado no frontmatter
[ ] CT-10: Mudanças MAJOR geram schema v+1 sem remover vN anterior
```

---

## Diagrama de sequência canônico (fluxo BPC como exemplo)

```
Raquel → dossie-caso          : fornece dados do caso
dossie-caso → analise-renda-bpc : entrega calculo_renda_bpc.v1.json
analise-renda-bpc → [análise] : extrai, verifica SM, classifica vícios
analise-renda-bpc → Raquel    : entrega análise textual
analise-renda-bpc → widget-visual : entrega blocos_visuais.v1.json [opcional]
widget-visual → mod4          : entrega PNG por bloco
analise-renda-bpc → replica   : entrega analise_textual.v1.json [opcional]
replica → mod4                : entrega peticao_estruturada.v1.json
mod4 → Raquel                 : entrega DOCX corporativo
```

Cada seta é um contrato. Cada contrato tem um schema. Nenhuma skill passa informação via contexto implícito de sessão — apenas via schema explícito.
