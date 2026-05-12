# 12 Modos operacionais — detalhamento

Cada modo do skill-creator-am tem comando de ativação, inputs esperados, pipeline e output canônico.

## Modo 1 — Create

**Comando**: "criar skill [nome]" ou "nova skill"

**Inputs**:
- Nome proposto (kebab-case)
- Problema concreto resolvido
- 4 coordenadas (Project, Núcleo, Frente, Camada)
- Categoria + justificativa
- depends_on + chains_to
- Gatilhos linguísticos (3-7) + cenários de não-disparo

**Pipeline**: ver §4 do SKILL.md.

**Output**: pacote `.skill` (zip) pronto para instalar.

---

## Modo 2 — Eval

**Comando**: "rodar eval em [skill]" ou "testar skill [nome]"

**Inputs**:
- Skill alvo
- Casos-teste de `examples/` (carregados automaticamente)

**Pipeline**:
1. Localizar skill
2. Carregar examples/*.md
3. Para cada caso, simular input e verificar comportamento
4. Comparar com critério de aprovação
5. Gerar relatório

**Output**:
```
Eval de skill [nome]:
====================
Casos positivos:
  caso-positivo-1: PASS / FAIL [+ detalhe]
  caso-positivo-2: PASS / FAIL
  caso-positivo-3: PASS / FAIL

Casos negativos:
  caso-negativo-1: PASS (bloqueou conforme esperado) / FAIL
  caso-negativo-2: PASS / FAIL

Resumo: N/5 PASS
Conclusão: aprovado / requer ajuste
```

---

## Modo 3 — Improve

**Comando**: "melhorar [skill]" ou "ajustar [skill] após eval"

**Inputs**:
- Skill alvo
- Relatório de eval anterior (opcional)

**Pipeline**:
1. Identificar falhas de eval
2. Para cada falha, propor ajuste em:
   - description (70% das falhas)
   - gatilhos linguísticos
   - §1 escopo
   - pipeline operacional
3. Mostrar diff proposto
4. Aguardar aprovação
5. Aplicar via Modo Edit (com R3 backup)

**Output**: skill modificada + relatório de ajustes.

---

## Modo 4 — Benchmark

**Comando**: "benchmark [skill]" ou "medir variância de [skill]"

**Inputs**:
- Skill alvo
- Casos-teste
- Número N de execuções (padrão: 5)

**Pipeline**:
1. Rodar eval N vezes
2. Calcular variância entre execuções
3. Identificar inputs com resultado inconsistente

**Output**:
```
Benchmark de [skill] (N=5):
==========================
Consistência geral: 80% (4/5 casos consistentes)
Casos inconsistentes:
  caso-positivo-2: passou em 3/5, falhou em 2/5
    Variação: [detalhe]

Recomendação: refinar gatilho linguístico do caso 2.
```

---

## Modo 5 — Cultivate

**Comando**: "cultivar biblioteca" ou "auditoria geral"

**Inputs**:
- Toda a biblioteca em `C:\RaquelSkills\skills\`

**Pipeline**:
1. Para cada skill, rodar audit (Modo 7)
2. Identificar skills com sinais de fadiga
3. Identificar pares de duplicação
4. Identificar candidatos a `_compartilhados/`
5. Gerar relatório consolidado

**Output**:
```
Cultivate da biblioteca - [data]
=================================
Skills auditadas: N
Skills saudáveis: N (verde)
Skills com alerta: N (amarelo)
Skills críticas: N (vermelho)

Refatorações sugeridas:
- [skill X]: 4 sinais de fadiga
- [skill Y]: 3 sinais

Duplicações detectadas:
- [skill A] × [skill B]: bloco de [N] linhas

Candidatos a _compartilhados/:
- [trecho]: aparece em [N] skills

Saúde geral: [%]
```

---

## Modo 6 — Refactor

**Comando**: "refatorar [skill]"

**Inputs**:
- Skill alvo
- (Opcional) plano de modularização proposto

**Pipeline**: ver §7 do SKILL.md.

**Output**: skill refatorada + relatório de mudanças + eval comparativo.

---

## Modo 7 — Audit

**Comando**: "auditar [skill]" ou cron mensal automático

**Inputs**:
- Skill alvo (ou todas)

**Pipeline**:
1. Rodar 12 auditorias pós-criação contra skill
2. Coletar resultados
3. Priorizar achados (vermelho > amarelo > verde)

**Output**:
```
Audit de [skill] - [data]
=========================
[A1] Tamanho: ✅ verde (387 linhas)
[A2] Frontmatter: ✅ verde (completo)
[A3] Lições aplicáveis: ⚠️ amarelo (L7 ausente)
[A4] Cláusulas: ✅ verde
[A5] Descrição diretiva: ✅ verde
[A6] Pragmática: ✅ verde
[A7] 12 dimensões: N/A (não produz texto jurídico)
[A8] Vocabulário: ⚠️ amarelo (2 variantes proibidas)
[A9] Casos-teste: ✅ verde
[A10] Duplicação: ⚠️ amarelo (12 linhas com revisao-previa-mod4)
[A11] Dependências: ✅ verde
[A12] verificado_em: ✅ verde (45 dias)

Resumo: 9 verde / 3 amarelo / 0 vermelho
Status: aprovado com ressalvas
```

---

## Modo 8 — Mirror

**Comando**: "mirror [skill]" ou "verificar institucional"

**Aplicável**: skills das frentes F5 (Bancada Ativista) e F6 (Artemis), que têm requisitos especiais (transparência institucional, alinhamento programático).

**Pipeline**:
1. Audit padrão (Modo 7)
2. Verificações adicionais:
   - Alinhamento programático com pauta da entidade
   - Transparência (sem caixas-pretas operacionais)
   - Replicabilidade (outra entidade pode adotar)

**Output**: audit padrão + relatório de aderência institucional.

---

## Modo 9 — Govern

**Comando**: "aplicar regras a [skill]" ou "governance update"

**Inputs**:
- Skill alvo
- Lista de regras a aplicar (R1-R11)

**Pipeline**:
1. Identificar tipo da skill (`scripts/inserir_clausulas.py`)
2. Determinar cláusulas obrigatórias
3. Comparar com cláusulas presentes
4. Inserir as faltantes
5. Backup R3 antes
6. Atualizar version (PATCH)

**Output**: skill com cláusulas atualizadas + relatório.

---

## Modo 10 — Undo

**Comando**: "undo [skill]" ou "voltar [skill] para [data]"

**Inputs**:
- Skill alvo
- Data ou ID de operação (de `_log-auditoria.md`)

**Pipeline**:
1. Localizar entrada no log
2. Verificar se reversível (≤ 30 dias)
3. Localizar arquivo de backup
4. Mostrar diff entre atual e backup
5. Aguardar confirmação
6. Backup da versão atual (proteção contra reversão errada)
7. Restaurar backup
8. Notificar skills dependentes
9. Registrar reversão no log

**Output**:
```
Undo de [skill]:
===============
Operação revertida: editar em 2026-05-11T14:32:00
Backup restaurado: SKILL-20260511-143200.md
Versão anterior: 1.0.3 → versão atual: 1.0.2
Versão atual movida para backup (proteção)

Skills dependentes notificadas:
- [skill X] (depends_on)
- [skill Y] (chains_to)
```

---

## Modo 11 — Extract

**Comando**: "extrair duplicação" ou "migrar para compartilhados"

**Inputs**:
- Trecho identificado como duplicado
- Skills afetadas

**Pipeline**: ver §8 do SKILL.md.

**Output**:
```
Extract concluído:
=================
Trecho: "[N] linhas de [skill A]"
Migrado para: _compartilhados/[tipo]/[nome]

Skills atualizadas (referenciando agora):
- [skill A]: linhas X-Y removidas, referência inserida
- [skill B]: linhas Z-W removidas, referência inserida

Backups gerados:
- _backups/[skill A]/SKILL-20260511-150000.md
- _backups/[skill B]/SKILL-20260511-150010.md
```

---

## Modo 12 — Diagnostico

**Comando**: "diagnosticar [skill]" ou "diagnóstico"

**Aplicável**: para skill específica (input) ou para toda a biblioteca (`--todas`).

**Pipeline**: ver §10 do SKILL.md.

**Output**: ver reference 10.

---

## Tabela resumo

| Modo | Tempo médio | Frequência típica |
|---|---|---|
| Create | 15-30 min | quando há demanda |
| Eval | 2-5 min | após cada modificação |
| Improve | 10-20 min | após eval com falhas |
| Benchmark | 10-15 min | mensal ou ad-hoc |
| Cultivate | 30-60 min | mensal (R9) |
| Refactor | 30-90 min | sob demanda |
| Audit | 5 min por skill | mensal (R9) |
| Mirror | 10-15 min | mensal para F5/F6 |
| Govern | 10-20 min | sob demanda |
| Undo | 5-10 min | sob demanda |
| Extract | 15-30 min | após detecção em Cultivate |
| Diagnostico | 3-5 min | sob demanda |

## Combinação de modos

Combinações típicas:
- Create + Eval: criação + validação imediata
- Cultivate → Refactor + Extract: auditoria geral → ação
- Audit → Govern: detecta deficiência → aplica regras
- Eval → Improve → Eval: ciclo de refinamento
- Edit → Backup R3 → Audit: modificação segura

Combinações proibidas:
- Undo + Edit simultâneo: estados conflitantes
- Refactor sem Backup R3 prévio: nunca
- Extract sem aprovação humana: nunca
