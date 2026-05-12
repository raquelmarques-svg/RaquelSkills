# Caso positivo 3 — Diagnóstico de `arglab` detectando inchaço

## Input

Raquel: "diagnóstico de arglab"

## Comportamento esperado

A skill-creator-am ativa Modo Diagnostico (ver reference 10). Roda análise completa nas 6 dimensões de saúde e devolve relatório priorizado com score 0-100.

### Fluxo

1. **Localização:**
   - Identifica `arglab` em biblioteca atual
   - Estado conhecido: 977 linhas no SKILL.md, 4 modos (adversarial, construção, crítica interna, mapeamento estratégico)

2. **Coleta de dados:**
   - `wc -l` em todos os arquivos
   - Parse do frontmatter
   - `verificar_duplicacao.py` contra biblioteca
   - Parse de depends_on/chains_to
   - Análise de log de auditoria

3. **Análise nas 6 dimensões:**

### Escopo
- Núcleo declarado: análise argumentativa em 4 modos
- Função fora do escopo detectada: não
- Sinais de delegação corretos: 3 referências (chains_to: revisao-juridica; depends_on: analise-precedente, levanta-fatos)
- Conformidade §1 FAÇO/NÃO FAÇO/DELEGO: 100%

### Volume
- SKILL.md: **977 linhas (VERMELHO — excede 500)**
- References: 4 arquivos, 856 linhas
- Scripts: 2 arquivos, 423 linhas
- Examples: 5 arquivos
- Total: 2.256 linhas

### Conformidade
- Frontmatter: completo
- verificado_em: 2026-03-20 (VÁLIDO até 2026-06-20, 40 dias)
- Cláusulas: R5, R6, R10 presentes; faltam: R9 (auditoria), R11 (economia)
- Estrutura §0…§N: presente
- Casos-teste: 5/5

### Fadiga estrutural (5 sinais)
- ✅ Sinal 1 inchaço quantitativo: SIM (977 > 500)
- ✅ Sinal 2 inchaço qualitativo: SIM (4 pipelines paralelos: adversarial, construção, crítica, mapeamento)
- ✅ Sinal 3 lições acumuladas: SIM (7 lições absorvidas em 90 dias, incluindo IBE, stases interpretativas, escala probativa)
- ❌ Sinal 4 duplicação: NÃO (< 20 linhas com outras)
- ❌ Sinal 5 inconsistência interna: NÃO

**3 sinais ativos → REFATOR OBRIGATÓRIO**

### Recursos compartilhados
- Consume: padrao-redacional, regras-universais
- Próprios duplicados: bloco IBE poderia ir para `_compartilhados/informacoes/` (também usado por replica-analise)

### Integração
- depends_on: [analise-precedente, levanta-fatos] — cross-check ✓
- chains_to: [revisao-juridica] — cross-check ✓
- Ciclos: nenhum

4. **Score de saúde:**

```
score = 100
- 20 (inchaço quantitativo)
- 15 (inchaço qualitativo)
- 10 (lições acumuladas)
- 5 (R9 ausente)
- 5 (R11 ausente)
= 45/100 → ATENÇÃO
```

5. **Recomendações priorizadas:**

CRÍTICAS:
1. Refator obrigatório. Plano sugerido:
   - SKILL.md core: manter pipeline geral (~250 linhas)
   - Extrair Modo Adversarial → reference 05-modo-adversarial.md (~200 linhas)
   - Extrair Modo Construção → reference 06-modo-construcao.md (~180 linhas)
   - Extrair Modo Crítica Interna → reference 07-modo-critica-interna.md (~190 linhas)
   - Extrair Modo Mapeamento → reference 08-modo-mapeamento.md (~150 linhas)
   - Meta: SKILL.md ≤ 300 linhas

ALTAS (semana):
2. Inserir R9 (auditoria mensal) e R11 (economia) no §0-Regras
3. Migrar bloco IBE para `_compartilhados/informacoes/ibe-framework.md`

MÉDIAS (mês):
4. Renovar verificado_em após refator
5. Atualizar version para 2.0.0 (MAJOR, mudança estrutural)

BAIXAS:
6. Examinar se algum dos 4 modos é raramente usado — candidato a desativação

6. **Salvamento:**
   Diagnóstico salvo em `/Drive/Claude/governanca/diagnosticos/arglab-20260511.md`

## Output esperado

Relatório no formato canônico de `references/10-modo-diagnostico.md`, com:
- Score: 45/100
- Classificação: ATENÇÃO
- 6 recomendações em 4 níveis de prioridade
- Plano concreto de refator com tamanhos estimados
- Salvamento automático em pasta de diagnósticos

## Critério de aprovação

- Diagnóstico nas 6 dimensões completo
- Score calculado corretamente
- Classificação coerente
- Plano de refator concreto (não genérico)
- Recomendações priorizadas (não lista plana)
- Skill original não foi modificada (diagnóstico é read-only)
- Backup do diagnóstico salvo em pasta canônica

## Erros que invalidariam o teste

- Modificar arglab sem ter pedido
- Score sem cálculo explícito
- Recomendações vagas ("considerar refator")
- Não identificar os 3 sinais ativos
- Esquecer de salvar diagnóstico em filesystem
