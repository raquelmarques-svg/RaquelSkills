# skill-creator-am — Documentação

Orquestrador do ciclo de vida de skills na biblioteca Almeida Marques.

## Quick Start

### Modo CREATE

```
Usuária: "Criar skill para análise de jurisprudência"

skill-creator-am analisa proposta e gera:
- C:\RaquelSkills\skills\[skill-name]\SKILL.md
- Estrutura de pastas (examples/, templates/, schemas/)
- README.md
- Entrada em _inventario.md
```

### Modo EDIT

```
Usuária: "Atualizar skill-x versão 1.0.0 → 1.1.0, adicionar suporte para PDF"

skill-creator-am:
1. Cria backup → _backups/skill-x-YYYYMMDD-HHMMSS/
2. Atualiza SKILL.md
3. Registra em _log-auditoria.md
```

### Modo REFACTOR

```
skill-creator-am detecta:
- 85 linhas duplicadas entre skill-A e skill-B
- Propõe: "Extrair para _compartilhados/rotinas/funcao-xy.py"
- Executa refactor com backup automático
```

### Modo CULTIVATE (Auditoria)

```
python auditar_skill_completo.py --todas --salvar

Gera: governanca/audit-202605.md com status de todas as 33 skills
```

## Estrutura interna

```
skill-creator-am/
├── SKILL.md              ← Definição da skill
├── README.md             ← Este arquivo
├── templates/
│   └── skill-template.yaml    ← Template para novas skills
├── examples/
│   ├── exemplo-create.md      ← Exemplo CREATE
│   ├── exemplo-edit.md        ← Exemplo EDIT
│   └── exemplo-refactor.md    ← Exemplo REFACTOR
└── schemas/
    └── skill.schema.json      ← Validação de SKILL.md
```

## Interação com regras R1-R11

| Regra | Aplicação |
|-------|-----------|
| R1 | Pergunta antes de gerar relatórios |
| R2 | Nunca deleta; move para _APAGAR/ |
| R3 | Backup automático antes de modificar |
| R6 | Propõe adaptação antes de negar proposta |
| R9 | Executa auditoria mensal |
| R10 | Aponta inconsistências em propostas |
| R11 | Planeja antes de executar |

## Dependências

- `parser_skill_md.py` — Parse de SKILL.md/frontmatter
- `auditar_skill_completo.py` — Validação e auditoria
- `log_auditoria.py` — Registro de operações
- `extrair_para_compartilhados.py` — Detecção de duplicação
- `undo_operacao.py` — Restaurar backup

## Próximas melhorias (Tier 2+)

- [ ] Modo IMPROVE — sugerir melhorias com base em métricas
- [ ] Modo BENCHMARK — comparar performance entre skills
- [ ] Modo EVAL — avaliação automática (depende de decisão API vs semiautomático)
- [ ] Integração com Claude API para suggestions de refactor
