---
title: skill-creator-am
description: "Cria, edita, refatora e audita skills na biblioteca Almeida Marques"
version: 1.0.0
category: capability
núcleo: N5
frente: transversal
camada: C0
projeto: Proj02
author: Raquel de Almeida Marques
verified_in: 2026-05-11
---

# skill-creator-am

**Objetivo**: Orquestrar ciclo completo de vida de skills: Create, Edit, Refactor, Cultivate (auditoria).

## Modos de operação

### 1. CREATE — Criar nova skill

Cria skill do zero respeitando arquitetura V4.

**Entrada**: proposta de skill (objetivo, categoria, exemplos de uso).

**Processo**:
- Valida proposta contra regras R6, R10 (adaptação, discordância útil)
- Gera SKILL.md com frontmatter correto
- Cria estrutura de pastas (examples/, templates/, schemas/)
- Gera README.md minimalista
- Registra em `_inventario.md`

**Saída**: pasta `C:\RaquelSkills\skills\[skill-name]\` pronta para conteúdo.

---

### 2. EDIT — Editar skill existente

Modifica skill sem quebrar dependências.

**Entrada**: skill existente + mudanças (description, versão, lógica).

**Processo**:
- Backup automático (R3)
- Valida mudanças contra R1-R11
- Atualiza frontmatter
- Registra alteração em `_log-auditoria.md`
- Atualiza versão em `_inventario.md`

**Saída**: skill modificada com backup preservado em `_backups/`.

---

### 3. REFACTOR — Reestruturar skill

Melhora qualidade sem alterar comportamento externo.

**Entrada**: skill existente + critérios de refactor (extractar função duplicada, separar concerns).

**Processo**:
- Detecta duplicação via `extrair_para_compartilhados.py`
- Propõe divisão de skill (split) ou fusão (merge)
- Gera relatório de impacto
- Executa refactor com backup

**Saída**: skill otimizada ou dividida em múltiplas skills.

---

### 4. CULTIVATE — Auditoria mensal

Executa auditoria R9 em todas as skills.

**Entrada**: (nenhuma — roda automaticamente)

**Processo**:
- Verifica tamanho (≤ 500 linhas core)
- Verifica versioning (verificado_in ≤ 90 dias)
- Detecta duplicação > 20 linhas
- Valida frontmatter (4 coordenadas + categoria + version)
- Gera relatório consolidado

**Saída**: `governanca/audit-YYYYMM.md` com status de todas as skills.

---

## Regras aplicáveis

- **R1 — Exportação**: Perguntar antes de gerar relatórios/arquivos
- **R2 — Preservação**: Nunca apagar; mover para `_APAGAR/`
- **R3 — Backup**: Backup automático antes de qualquer modificação
- **R6 — Adaptação antes de negação**: Sempre propor ajuste antes de recusar proposta
- **R9 — Auditoria mensal**: Executa ciclo R9
- **R10 — Discordância útil**: Apontar inconsistências na proposta de skill
- **R11 — Economia de ação**: Planejar antes de executar

---

## Dependências

- `parser_skill_md.py` — Parse de SKILL.md
- `auditar_skill_completo.py` — Auditoria
- `log_auditoria.py` — Logging
- `extrair_para_compartilhados.py` — Detecção de duplicação
- `undo_operacao.py` — Desfazer última operação

---

## Exemplos de uso

### Exemplo 1: Criar nova skill

```
Usuária: "Quero criar uma skill que analisa precedentes judiciais"

skill-creator-am:
1. Valida proposta (objetivo claro? categoria? exemplos?)
2. Pergunta: "Precisa de integração com jurisprudência existente?"
3. Gera: C:\RaquelSkills\skills\analise-precedente-v2\SKILL.md
4. Registra em _inventario.md com status "planejado"
```

### Exemplo 2: Refactor — detectar duplicação

```
skill-creator-am roda mensalmente:
1. Encontra 85 linhas duplicadas entre skill-A e skill-B
2. Propõe: "Extrair função X para _compartilhados/rotinas/"
3. Executa refactor com backup
4. Registra em _log-auditoria.md
```

### Exemplo 3: Auditoria mensal

```
python auditar_skill_completo.py --todas --salvar

Resultados:
- 7 skills ✅ OK (tamanho, versão, duplicação ≤ 20 linhas)
- 3 skills ⚠️ AVISO (verificado_in > 90 dias)
- 1 skill 🔴 ERRO (2000 linhas, split necessário)

Relatório: governanca/audit-202605.md
```

---

## Status

**Instalado**: ✅ 2026-05-11  
**Versão**: 1.0.0  
**Última auditoria**: 2026-05-11  
**Próxima auditoria**: 2026-06-11

---

## Notas de implementação

- Modes CREATE, EDIT, REFACTOR são semi-automáticos (feedback humano necessário)
- Mode CULTIVATE é totalmente automático
- Todos os modos registram em log de auditoria (R9)
- Backup automático em todas operações (R3)
