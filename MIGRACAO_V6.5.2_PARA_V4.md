# Migração: Arquitetura V6.5.2 → V4

**Data**: 2026-05-11  
**Origem**: Biblioteca Raquel Skills V6.5.2  
**Destino**: Almeida Marques V4  
**Status**: Documentação de referência

---

## Resumo executivo

A arquitetura **V6.5.2** era centrada na skill `governanca-skills` como orquestrador monolítico.

A arquitetura **V4** descentraliza essas responsabilidades em:
- Scripts Python orquestradores (`_compartilhados/rotinas/`)
- Skills especializadas (CREATE, EDIT, REFACTOR)
- Regras universais (R1-R11)
- Log centralizado de auditoria

**Benefícios da V4:**
- ✅ Modularização (cada script tem uma responsabilidade)
- ✅ Rastreabilidade (log de auditoria em YAML)
- ✅ Automatização (scripts podem rodar sem intervenção)
- ✅ Escalabilidade (novas skills sem modificar orquestrador)

---

## Mapeamento funcional: V6.5.2 → V4

### 1. Modo CRIAÇÃO (governanca-skills V6.5.2)

**O que fazia:**
```
input: descrição de skill
operação: gerar SkillCreationSpec
output: especificação aprovada
```

**Na V4:**
```
Responsável: skill-creator-am (CREATE mode)
Entrada: Descrição + exemplos + categoria
Processo: Validação contra R6 (adaptação) + R10 (discordância)
Saída: SKILL.md + estrutura de pastas
Arquivo: C:\RaquelSkills\skills\[skill-name]\
Registro: _inventario.md + _log-auditoria.md
```

**Diferenças:**
- ❌ Não usa SkillCreationSpec XML
- ✅ Usa SKILL.md com frontmatter YAML (mais simples)
- ✅ Integrado com regras R1-R11

---

### 2. Modo AUDITORIA LEVE (governanca-skills V6.5.2)

**O que fazia:**
```
input: skill existente
operação: verificar campos mínimos
output: relatório de auditoria
```

**Na V4:**
```
Responsável: auditar_skill_completo.py (CULTIVATE mode)
Entrada: Nenhuma (varre C:\RaquelSkills\skills\)
Processo: Verifica tamanho, versão, duplicação, frontmatter
Saída: governanca/audit-YYYYMM.md
Frequência: Mensal (R9)
Métricas:
  - Linhas ≤ 500 (core logic)
  - verificado_in ≤ 90 dias
  - Duplicação ≤ 20 linhas
  - Frontmatter válido (4 coordenadas + categoria + version)
```

**Diferenças:**
- ✅ Automatizada (não precisa de input manual)
- ✅ Relatório consolidado (audit-YYYYMM.md)
- ✅ Métricas de qualidade (R9)
- ❌ Sem busca por "verbo dominante" (simplificado)

---

### 3. Modo CLASSIFICAÇÃO (governanca-skills V6.5.2)

**O que fazia:**
```
input: conteúdo indefinido
operação: classificar como skill / asset / template / etc
output: ficha de classificação
```

**Na V4:**
```
Responsável: parser_skill_md.py
Entrada: SKILL.md ou arquivo Markdown
Processo: Parse de frontmatter, validação contra schema
Saída: Objetos Python com metadados
Uso: Integrado em auditar_skill_completo.py
```

**Diferenças:**
- ✅ Automático (não precisa de decision trees)
- ✅ Rápido (simples parse YAML)
- ❌ Sem UI de escolha (mais programático)

---

### 4. Modo DIVISÃO (governanca-skills V6.5.2)

**O que fazia:**
```
input: skill com múltiplos verbos dominantes
operação: propor split em skills menores
output: plano de divisão
```

**Na V4:**
```
Responsável: skill-creator-am (REFACTOR mode)
Entrada: Proposta de divisão (manualmente ou via auditoria)
Processo: Gera plano, cria novos SKILL.md, backup automático
Saída: 2+ skills menores + registro em _log-auditoria.md
Regra: R3 (backup) + R2 (preservação)
```

**Diferenças:**
- ✅ Integrado com REFACTOR (não é operação isolada)
- ✅ Automático de backup (R3)
- ❌ Detecta divisão via auditoria R9, não automaticamente

---

### 5. Modo FUSÃO (governanca-skills V6.5.2)

**O que fazia:**
```
input: 2+ skills com output sobrepostos
operação: propor merge e integração
output: plano de fusão
```

**Na V4:**
```
Responsável: extrair_para_compartilhados.py + skill-creator-am
Entrada: Detecção automática de duplicação (≥85% similaridade)
Processo: 
  1. extrair_para_compartilhados.py detecta duplicação
  2. skill-creator-am propõe REFACTOR
  3. Extrai função comum para _compartilhados/rotinas/
  4. Ambas as skills importam a função
Saída: Skill otimizada + rotina compartilhada
Registro: _log-auditoria.md
```

**Diferenças:**
- ✅ Automático (não requer input manual)
- ✅ Cria rotina reutilizável (não deleta, apenas refatora)
- ❌ Sem merge de skills (prefere extrair função comum)

---

### 6. Auto-auditoria (governanca-skills V6.5.2)

**O que fazia:**
```
input: governanca-skills
operação: auto-auditar contra critérios próprios
output: relatório de saúde
```

**Na V4:**
```
Responsável: auditar_skill_completo.py --todas
Entrada: Nenhuma (varre biblioteca)
Processo: Mesmos critérios de outras skills (R9)
Saída: Incluída em audit-YYYYMM.md
Nota: skill-creator-am não se auto-audita (evita recursão)
```

**Diferenças:**
- ✅ skill-creator-am é auditada como skill normal
- ✅ Sem privilégio especial
- ❌ Sem relatório "reflexivo" (mais simples)

---

## Comparação estrutural

| Aspecto | V6.5.2 | V4 |
|---------|--------|-----|
| **Orquestrador central** | governanca-skills (skill monolítica) | skill-creator-am + scripts modulares |
| **Criação de spec** | SkillCreationSpec (XML complexo) | SKILL.md (YAML simples) |
| **Auditoria** | Sob demanda | Automática mensal (R9) |
| **Log** | Não registrava | _log-auditoria.md (YAML) |
| **Inventário** | Implícito em _manifest | _inventario.md (Markdown tabela) |
| **Duplicação** | Detecta via análise manual | Automático (≥85% similarity) |
| **Backup** | Não automático | Automático em todas operações (R3) |
| **Preservação** | Deleta archivos | Move para _APAGAR/ (R2) |
| **Refactor** | Recomendação | Executável automaticamente |

---

## Compatibilidade reversa

**governanca-skills V6.5.2 é mantida como referência histórica:**

```
C:\RaquelSkills\.claude\skills\_internal\governanca-skills\
├── SKILL.md                      ← Documentação original
├── AUDITORIA_CONSOLIDADA.md      ← Último relatório
├── schemas/                       ← Schemas antigos (FYI)
├── templates/                     ← Templates antigos (FYI)
└── scripts/                       ← Scripts antigos (não usados em V4)
```

**Quando consultá-la:**
- Entender como skills eram classificadas em V6.5.2
- Referência de conceitos (verbo dominante, critérios de split)
- Contexto histórico de decisões

**Não é mais usada para:**
- Criar novas skills
- Auditar biblioteca
- Gerar relatórios operacionais

---

## Roteiro de transição (futuro)

Se você tiver **skills existentes** em V6.5.2 que queira migrar:

1. **Analisar** a skill com skill-creator-am (modo REFACTOR)
2. **Gerar** novo SKILL.md em formato V4
3. **Testar** com auditar_skill_completo.py
4. **Registrar** em _inventario.md
5. **Preservar** versão antiga em _backups/

---

## Arquivos de referência

- `C:\RaquelSkills\governanca\regras-universais.md` — Regras R1-R11 (V4)
- `C:\RaquelSkills\.claude\skills\_internal\governanca-skills\SKILL.md` — V6.5.2 (histórico)
- `C:\RaquelSkills\skills\skill-creator-am\` — Orquestrador V4
- `C:\RaquelSkills\_compartilhados\rotinas\` — Scripts V4

---

## Conclusão

**V4 é mais modular, automatizada e rastreável** que V6.5.2.

A transição não é obrigatória para skills existentes, mas **nova** biblioteca começa em V4.

Dúvidas? Consulte:
- `skill-creator-am` (CREATE mode) → para criar skills
- `auditar_skill_completo.py` → para validar
- `regras-universais.md` → para entender governança
