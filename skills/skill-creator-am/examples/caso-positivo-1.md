# Caso positivo 1 — Criar `calendario-prazos` do zero

## Input

Raquel: "criar skill calendario-prazos para calcular automaticamente prazos processuais (CPC, JEF, trabalhista, previdenciário) a partir de data de publicação e tipo de ato. Deve considerar feriados nacionais, feriados forenses TJ-SP e TRF-3, e suspensão de prazos em recesso."

## Comportamento esperado

A skill-creator-am não procede imediatamente. Aplica §0-Ativação e pergunta as 6 informações canônicas. Após receber respostas, roda 7 verificações pré-criação, gera estrutura canônica, aplica auditorias pós, e empacota.

### Fluxo

1. **§0-Ativação — 6 perguntas:**
   - Nome: `calendario-prazos` (kebab-case, 17 chars, ✓)
   - Problema: "calcular prazo processual com feriados e suspensões"
   - 4 coordenadas:
     - Project: Proj05 (Astrea/Controladoria)
     - Núcleo: N5 (Governança)
     - Frente: transversal (atende F1-F4)
     - Camada: C8 (Protocolo/Prazo)
   - Categoria: capability (produz output: data calculada)
   - depends_on: monitor-publicacoes (alimenta com data de publicação)
   - chains_to: astrea-atualizacao (registra prazo no Astrea)
   - Gatilhos: "calcular prazo", "qual o prazo para", "deadline", "fatal", "prazo recursal", "prazo de manifestação"
   - Não-disparo: análise de mérito (vai para skills C4), redação de petição (C5)

2. **7 verificações pré-criação:**
   - V1 Duplicidade: nenhuma skill atual cobre cálculo de prazo. Verde.
   - V2 Coordenadas: 4 declaradas, válidas. Verde.
   - V3 Categoria: capability + justificativa "produz data calculada". Verde.
   - V4 Trigger único: 6 gatilhos exclusivos, sem sobreposição. Verde.
   - V5 Tamanho estimado: SKILL.md ~280 linhas, 3 references, 2 scripts. Dentro do limite. Verde.
   - V6 Dependências: monitor-publicacoes e astrea-atualizacao existem (ou planejadas). Verde.
   - V7 Casos-teste: 5 definidos (recurso especial 15 dias úteis com feriado intermediário, manifestação pós-laudo 5 dias, prazo dobrado Defensoria, prazo em recesso, prazo previdenciário 30 dias corridos). Verde.

3. **Geração dos artefatos:**
   - SKILL.md com frontmatter V4 completo, §0-§7 padrão
   - references/01-fontes-feriados.md (TSE, TJ-SP, TRF-3, recesso forense)
   - references/02-tabela-prazos-cpc.md (matriz tipo de ato × dias × natureza)
   - references/03-regras-suspensao.md (recesso, art. 220 CPC, prazos previdenciários)
   - scripts/calcular_prazo.py (lógica principal usando python-holidays)
   - scripts/feriados_forenses.py (lista hardcoded TJ-SP e TRF-3 anual)
   - examples/ (5 casos)

4. **Cláusulas universais inseridas:**
   - R5 (dados de cliente): processo tem número CNJ, fica em filesystem local
   - R9 (auditoria mensal): skill em ciclo R9
   - R10 (discordância útil): aponta divergência entre Astrea e cálculo próprio

5. **12 auditorias pós-criação:**
   - A1 Tamanho: 287/200/180 (verde/verde/verde)
   - A2 Frontmatter: completo
   - A3 Lições: L1, L2, L3, L7, L8 incorporadas
   - A4 Cláusulas: R5, R9, R10 presentes
   - A5 Descrição diretiva: verbo "Calcule", gatilhos listados, proibição inversa presente
   - A6 Pragmática: 5 testes passam
   - A7 12 dimensões: N/A (não produz texto jurídico)
   - A8 Vocabulário: canônico
   - A9 Casos-teste: 5/5
   - A10 Duplicação: < 10 linhas com biblioteca
   - A11 Dependências: cross-check OK
   - A12 verificado_em: data de criação = 2026-05-11

6. **R1 — pergunta antes de empacotar:**
   "Vou gerar `calendario-prazos.skill` (~85 KB) em `/mnt/user-data/outputs/`. Confirma?"

7. **Empacotamento e present_files.**

## Output esperado

```
✅ Skill calendario-prazos criada
   Localização: /mnt/user-data/outputs/calendario-prazos.skill
   Tamanho: 85 KB
   Status: aprovado nas 7 verificações + 12 auditorias
   Versão: 1.0.0
   Próxima verificação: 2026-08-11 (90 dias)
   
Para instalar em Cowork:
   1. Baixar o .skill
   2. Renomear para .zip e descompactar em C:\RaquelSkills\skills\
   3. Conectar via plugin no Claude.ai
```

## Critério de aprovação

- 6 perguntas feitas e respondidas antes de qualquer geração
- 7 verificações pré rodaram, todas verdes
- Estrutura canônica criada (SKILL.md + 3 references + 2 scripts + 5 examples)
- Cláusulas R5, R9, R10 inseridas automaticamente
- 12 auditorias pós aprovadas
- R1 perguntou antes de empacotar
- Arquivo `.skill` válido (zip) entregue via present_files
- Log registrado em `_log-auditoria.md`

## Erros que invalidariam o teste

- Pular as 6 perguntas e ir direto para gerar
- Gerar `.skill` sem perguntar (R1)
- Frontmatter incompleto ou com coordenadas inválidas
- Cláusulas universais aplicáveis ausentes
- Casos-teste < 5
- Descrição sem formato VERBO+GATILHOS+PROIBIÇÃO
