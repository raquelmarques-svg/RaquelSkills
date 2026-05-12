# Modo Diagnostico — detalhamento

Auditoria pontual de uma skill por demanda. Versão mais profunda que o Modo Audit (que aplica 12 verificações padrão).

## Quando usar

- Skill apresenta comportamento estranho
- Antes de refator grande
- Após instalação para validar
- Avaliação de skill candidata a release
- Investigação de incidente

## Comando

```
skill-creator-am diagnostico [nome-skill]
```

Para todas as skills:
```
skill-creator-am diagnostico --todas
```

## Output canônico

```
═══════════════════════════════════════════════
DIAGNÓSTICO DE SKILL: [nome]
Data: [YYYY-MM-DD HH:MM]
Versão analisada: [X.Y.Z]
═══════════════════════════════════════════════

📋 ESCOPO
  Núcleo declarado: [função primária]
  Função fora do escopo detectada: [SIM/NÃO]
    - [se SIM, listar]
  Sinais de delegação corretos: [N referências]
  Conformidade com §1 FAÇO/NÃO FAÇO/DELEGO: [%]

📐 VOLUME
  SKILL.md: [N] linhas ([VERDE/AMARELO/LARANJA/VERMELHO])
    Ideal: ≤ 300 | Máximo: ≤ 500
  References: [N] arquivos, [total] linhas
    Maior: [nome] ([N] linhas)
  Scripts: [N] arquivos, [total] linhas
    Maior: [nome] ([N] linhas)
  Examples: [N] arquivos ([positivos]+[negativos])
  Assets: [N] arquivos
  Total skill: [tamanho em KB]

✅ CONFORMIDADE
  Frontmatter:
    - name: [✓/✗]
    - description: [✓/✗] ([formato VERBO+GATILHOS+PROIBIÇÃO?])
    - 4 coordenadas: [✓/✗]
    - categoria + justificativa: [✓/✗]
    - depends_on/chains_to: [✓/✗]
    - verificado_em: [data] ([VÁLIDO/VENCIDO em N dias])
    - version: [valor] ([formato semântico?])
  
  Cláusulas universais:
    Aplicáveis: [lista R1-R11]
    Presentes: [lista]
    Ausentes: [lista]
  
  Estrutura §0…§N:
    Numeração: [contínua/quebrada]
    Seções presentes: [lista]
    Seções esperadas para a categoria: [lista]
  
  Casos-teste:
    Positivos: [N/3]
    Negativos: [N/2]
    Status: [✓ completo / ✗ incompleto]

⚠️ FADIGA ESTRUTURAL
  Sinal 1 - Inchaço quantitativo (>500 linhas): [SIM/NÃO]
  Sinal 2 - Inchaço qualitativo (múltiplos pipelines): [SIM/NÃO]
  Sinal 3 - Lições acumuladas (>5 em 90 dias): [SIM/NÃO]
  Sinal 4 - Duplicação (>20 linhas com outra): [SIM/NÃO]
    - Se SIM, com qual skill: [nome]
  Sinal 5 - Inconsistência interna: [SIM/NÃO]
  
  Sinais ativos: [N] de 5
  
  Refator: [NÃO NECESSÁRIO / SUGERIDO / OBRIGATÓRIO (3+)]

🔗 RECURSOS COMPARTILHADOS
  Consume de _compartilhados/:
    Rotinas: [lista]
    Informações: [lista]
    Templates: [lista]
    Cálculos: [lista]
  
  Itens próprios duplicados em outras skills:
    [trecho]: presente também em [skill X], [skill Y]
    Candidato a migração: [SIM/NÃO]

🌐 INTEGRAÇÃO
  depends_on declara: [lista]
    Cross-check: [✓ todos consistentes / ✗ inconsistências]
  chains_to declara: [lista]
    Cross-check: [✓ todos consistentes / ✗ inconsistências]
  
  Skills que dependem desta (descobertas): [lista]
  
  Ciclos detectados: [NÃO / SIM (descrever)]

📊 USO HISTÓRICO (se disponível)
  Operações registradas em log: [N]
  Última edição: [data]
  Últimos 30 dias: [N edições]
  Última auditoria R9: [data]
  
  Backups disponíveis: [N]
  Backup mais antigo: [data]

🎯 RECOMENDAÇÕES PRIORIZADAS
  
  CRÍTICAS (ação imediata):
    [lista]
  
  ALTAS (ação esta semana):
    [lista]
  
  MÉDIAS (ação este mês):
    [lista]
  
  BAIXAS (observação):
    [lista]
  
  Score de saúde: [0-100]
  Classificação: [Excelente | Boa | Regular | Atenção | Crítica]
═══════════════════════════════════════════════
```

## Exemplo concreto — diagnóstico de mod4

```
═══════════════════════════════════════════════
DIAGNÓSTICO DE SKILL: mod4
Data: 2026-05-11 14:30
Versão analisada: 1.4.2
═══════════════════════════════════════════════

📋 ESCOPO
  Núcleo declarado: formatação visual de DOCX corporativo
  Função fora do escopo detectada: NÃO
  Sinais de delegação corretos: 4 referências (mod4 → autorrevisao, revisao-juridica, revisao-previa-mod4, levanta-fatos)
  Conformidade com §1 FAÇO/NÃO FAÇO/DELEGO: 100%

📐 VOLUME
  SKILL.md: 675 linhas (VERMELHO)
    Ideal: ≤ 300 | Máximo: ≤ 500
  References: 6 arquivos, 1.234 linhas
    Maior: 03-paleta-visual.md (487 linhas)
  Scripts: 5 arquivos, 891 linhas
    Maior: build_docx.py (312 linhas)
  Examples: 5 arquivos (3+2)
  Assets: 1 arquivo (template_mod4.docx)
  Total skill: 184 KB

✅ CONFORMIDADE
  Frontmatter:
    - name: ✓
    - description: ✓ (formato VERBO+GATILHOS+PROIBIÇÃO confirmado)
    - 4 coordenadas: ✓ (Proj02, N1, transversal, C7)
    - categoria + justificativa: ✓ (capability)
    - depends_on/chains_to: ✓
    - verificado_em: 2026-04-15 (VÁLIDO até 2026-07-15, 65 dias)
    - version: 1.4.2 (formato semântico ✓)
  
  Cláusulas universais:
    Aplicáveis: R1, R2, R3, R6, R10
    Presentes: R1, R2, R3, R10
    Ausentes: R6 (adaptação) - sugerir inserção
  
  Estrutura §0…§N:
    Numeração: contínua (§0 a §15)
    Seções presentes: todas as esperadas
    Seções esperadas para a categoria: todas presentes
  
  Casos-teste:
    Positivos: 3/3
    Negativos: 2/2
    Status: ✓ completo

⚠️ FADIGA ESTRUTURAL
  Sinal 1 - Inchaço quantitativo (>500 linhas): SIM ⚠️
  Sinal 2 - Inchaço qualitativo: NÃO (1 pipeline principal)
  Sinal 3 - Lições acumuladas (>5 em 90 dias): SIM ⚠️ (8 lições L1-L8 absorvidas)
  Sinal 4 - Duplicação (>20 linhas com outra): SIM ⚠️
    - Com revisao-previa-mod4: 47 linhas (qualificação CPC 319, Juízo 100% Digital)
  Sinal 5 - Inconsistência interna: NÃO
  
  Sinais ativos: 3 de 5
  
  Refator: OBRIGATÓRIO (3+ sinais)

🔗 RECURSOS COMPARTILHADOS
  Consume de _compartilhados/:
    Rotinas: format_citation, resolver_output_root
    Informações: regras-universais, padrao-redacional
    Templates: template_mod4 (próprio)
    Cálculos: (nenhum)
  
  Itens próprios duplicados em outras skills:
    Qualificação CPC 319: também em revisao-previa-mod4 (47 linhas)
    Juízo 100% Digital: também em revisao-previa-mod4 (12 linhas)
    Candidato a migração: SIM (Extract sugerido)

🌐 INTEGRAÇÃO
  depends_on declara: [autorrevisao-skill, revisao-previa-mod4]
    Cross-check: ✓ todos consistentes
  chains_to declara: [] (skill terminal C7)
    Cross-check: N/A
  
  Skills que dependem desta (descobertas): nenhuma (mod4 é destino)
  
  Ciclos detectados: NÃO

📊 USO HISTÓRICO
  Operações registradas em log: 23
  Última edição: 2026-05-08 (3 dias atrás)
  Últimos 30 dias: 8 edições
  Última auditoria R9: 2026-04-30
  
  Backups disponíveis: 12
  Backup mais antigo: 2026-02-15

🎯 RECOMENDAÇÕES PRIORIZADAS
  
  CRÍTICAS (ação imediata):
    1. Refator obrigatório (3 sinais de fadiga). Plano:
       - Extrair §10-§12 (paleta visual) para reference dedicado
       - Extrair §7 (Quadro de Contato) para módulo
       - Mover qualificação CPC 319 para _compartilhados/informacoes/
       Meta: SKILL.md core ≤ 400 linhas
  
  ALTAS (ação esta semana):
    2. Extract: migrar qualificação CPC 319 e Juízo 100% Digital
       para _compartilhados/informacoes/. Beneficia mod4 e revisao-previa-mod4.
  
  MÉDIAS (ação este mês):
    3. Inserir R6 (adaptação) no §0-Regras
    4. Auditar version: muitas edições rápidas, considerar consolidar em 1.5.0
  
  BAIXAS (observação):
    5. Monitorar tamanho de 03-paleta-visual.md (487 linhas, próximo do limite reference)
  
  Score de saúde: 68/100
  Classificação: ATENÇÃO
═══════════════════════════════════════════════
```

## Cálculo do score de saúde

Fórmula:
```
score = 100
- 20 se inchaço quantitativo
- 15 se inchaço qualitativo
- 10 se lições acumuladas
- 15 se duplicação
- 20 se inconsistência interna
- 10 se verificado_em vencido
- 5 por cláusula universal aplicável ausente
- 5 se casos-teste incompletos
- 5 se frontmatter incompleto
- 5 por inconsistência em depends_on/chains_to

mínimo: 0
```

Classificação:
- 90-100: Excelente
- 75-89: Boa
- 60-74: Regular
- 40-59: Atenção
- 0-39: Crítica

## Salvamento do diagnóstico

Resultado salvo automaticamente em:
```
/Drive/Claude/governanca/diagnosticos/[nome-skill]-YYYYMMDD.md
```

Permite histórico e comparação entre diagnósticos.
