# Cinco eixos de auto-percepção — skill autoconsciente

Toda skill criada incorpora bloco leve de auto-percepção. Esta reference detalha os 5 eixos.

## Eixo 1 — Escopo próprio

Pergunta interna: o que está dentro de mim? O que está fora?

### Implementação canônica

```markdown
## §1 — Escopo

FAÇO:
- [Função 1]
- [Função 2]

NÃO FAÇO:
- [Exclusão 1] (delego para [skill X])
- [Exclusão 2] (delego para [skill Y])

DELEGO PARA:
- [skill X]: [função correspondente]
- [skill Y]: [função correspondente]
```

### Detecção de excesso de escopo (5 sinais)

| Sinal | Detecção automática | Sintoma |
|---|---|---|
| Vocabulário fora do domínio | Termos do glossário de outra frente | Vocabulário disperso |
| Função duplicada | Trecho > 20 linhas igual a outra skill | Sobreposição |
| Pipeline em duas etapas | Há "primeiro X, depois Y" autônomos | Sub-skills latentes |
| Dependência circular | A→B→A | Acoplamento ruim |
| Cláusulas condicionais expansivas | > 10 if/then no pipeline | Skill virando framework |

### Bloco §0-Autoavaliação

```markdown
## §0-Autoavaliação

Antes de produzir output, verifico:

1. Input pertence ao §1 (escopo)?
   - Se sim, procedo
   - Se não, sinalizo: "Esta solicitação parece pertencer a [skill X]. Redirecionar?"

2. Detectei termo do vocabulário de frente diferente da minha?
   - Sinalizo e prossigo com cuidado

3. Estou prestes a duplicar função declarada de outra skill?
   - Bloqueio e sugiro delegação
```

## Eixo 2 — Volume saudável

Pergunta interna: estou no tamanho adequado? Inchei?

### Limites quantitativos

| Componente | Ideal | Máximo |
|---|---|---|
| SKILL.md core | 300 linhas | 500 linhas |
| Frontmatter | 25 linhas | 40 linhas |
| §0 (ativação) | 30 linhas | 60 linhas |
| Reference (cada) | 200 linhas | 400 linhas |
| Script (cada) | 200 linhas | 500 linhas |

### Detecção qualitativa

| Indicador | Sintoma | Resposta |
|---|---|---|
| Múltiplos pipelines paralelos | 3+ caminhos de execução distintos | Considerar split em sub-skills |
| Categorias misturadas | capability + preference + governança | Separar em camadas |
| Muitas regras condicionais | > 10 if/then | Mover para tabela de decisão em reference |
| Acúmulo de exceções | "Salvo quando...", "Exceto se..." | Cada exceção vira caso documentado |

### Bloco §N-Tamanho

```markdown
## §N — Estado de volume

SKILL.md: [N] linhas (verde/amarelo/laranja/vermelho)
References: [N] arquivos, [total] linhas
Scripts: [N] arquivos, [total] linhas

Tendência: estável | crescendo | refator pendente
```

## Eixo 3 — Conformidade canônica

Pergunta interna: estou seguindo o template? Saí do padrão?

### Confronto com template canônico

Cada skill é confrontada com `references/04-template-canonico.md`.

Desvios detectáveis:

| Desvio | Detecção |
|---|---|
| Frontmatter incompleto | Falta coordenada (Project/Núcleo/Frente/Camada) |
| verificado_em vencido | Data > 90 dias |
| Cláusulas universais ausentes | R1-R11 aplicáveis não inseridas |
| Estrutura §0…§N quebrada | Numeração faltante ou fora de ordem |
| Descrição não-diretiva | Não inicia com verbo imperativo |
| Termos do glossário violados | Variantes proibidas presentes |
| Casos-teste ausentes | < 3 positivos + 2 negativos |

### Bloco §N-AutoVerificação

```markdown
## §N — Auto-verificação

Última verificação de conformidade: YYYY-MM-DD
Próxima verificação: YYYY-MM-DD

Checklist:
- [ ] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [ ] verificado_em ≤ 90 dias
- [ ] Cláusulas R1-R11 aplicáveis presentes
- [ ] Estrutura §0…§N conforme template
- [ ] Descrição diretiva
- [ ] Vocabulário canônico
- [ ] 5 casos-teste (3 positivos + 2 negativos)
- [ ] Tamanho dentro do limite
```

`governanca-skills` (cron mensal R9) atualiza esses checklists.

## Eixo 4 — Hora de refatorar

Pergunta interna: tenho sinais internos de fadiga estrutural?

### Cinco sinais de fadiga

| Sinal | Detecção | Threshold |
|---|---|---|
| Inchaço quantitativo | wc -l SKILL.md | > 500 |
| Inchaço qualitativo | Múltiplos pipelines paralelos | 3+ |
| Lições acumuladas | Gotchas em 90 dias | > 5 |
| Duplicação detectada | Trechos > 20 linhas com outra skill | 1+ |
| Inconsistência interna | Auto-contradição (proíbe e instrui mesma ação) | 1+ |

### Critério acumulativo

Refator obrigatório se **3+ sinais simultâneos**.

### Modo Refactor automático

Disparado por auditoria R9 quando critério atendido.

Pipeline:
1. Lê skill atual
2. Identifica blocos candidatos a módulo (`references/`)
3. Identifica blocos candidatos a script (`scripts/`)
4. Identifica blocos candidatos a `_compartilhados/`
5. Propõe estrutura modular
6. Backup R3 da versão atual
7. Aplica refatoração
8. Roda audit pós-refatoração
9. Roda eval comparando antes/depois
10. Se eval piorou, reverte via Undo

## Eixo 5 — Recursos compartilhados

Pergunta interna: o que tenho é meu, ou pertence a um núcleo comum?

### Quatro tipos de recurso compartilhável

| Tipo | Exemplo | Local canônico |
|---|---|---|
| Rotina | cálculo de prazo, validação CNJ | `_compartilhados/rotinas/` |
| Informação | glossário, R1-R11, matriz CAT-XX | `/Drive/Claude/informacoes/` |
| Template | template_mod4.docx | `_compartilhados/templates/` |
| Cálculo | honorários, valor da causa | `_compartilhados/calculos/` |

### Princípio do núcleo comum

Sempre que **duas ou mais skills** precisam do mesmo recurso, esse recurso migra para `_compartilhados/`. Skills passam a referenciar.

### Bloco §N — Uso de recursos compartilhados

```markdown
## §N — Uso de recursos compartilhados

Esta skill consome:

| Recurso | Localização | Uso |
|---|---|---|
| calcular_prazo.py | _compartilhados/rotinas/ | Cálculo de prazo CPC |
| regras-universais.md | /Drive/Claude/informacoes/ | R1, R3 aplicadas |
| template_mod4.docx | _compartilhados/templates/ | Base do DOCX final |

Esta skill NÃO duplica esses recursos. Referencia.
```

### Detecção de duplicação

`scripts/verificar_duplicacao.py` (do skill-creator-am):
1. Percorre todas as skills
2. Compara cada par em blocos de 20+ linhas
3. Lista trechos duplicados acima do limiar
4. Sugere migração para `_compartilhados/`

Pares já detectados (auditoria histórica):
- mod4 × revisao-previa-mod4: qualificação CPC 319, Juízo 100% Digital
- alimentos × ms: blocos §0, qualificação completa
- pericia-acidentaria × pericia-previdenciaria: tripé CID/CIF/CBO, NTEP

Candidatos óbvios a `_compartilhados/`.

---

## Implementação leve em toda skill

A skill-creator-am insere bloco mínimo em toda skill criada:

```markdown
## §0-Autopercepção (verificação leve)

Antes de produzir output:
1. **Escopo**: o pedido cabe em §1?
2. **Volume**: estou ≤ 500 linhas?
3. **Recursos**: vou usar _compartilhados/?

Se 2+ alertas amarelos, sinalizar e sugerir refator à Raquel.
```

Versão pesada (com todos os checklists detalhados) só na própria `skill-creator-am` e em skills de governança. Demais skills usam versão leve.

## Modo Diagnostico (uso pontual)

Comando: `skill-creator-am diagnostico [skill]`

Output canônico:

```
Diagnóstico de skill: [nome]
============================

Escopo:
  - Núcleo declarado: [função]
  - Função fora do escopo: [detectado/não]
  - Sinais de delegação: [N referências]

Volume:
  - SKILL.md: [N] linhas ([cor])
  - References: [N] arquivos, [total] linhas
  - Scripts: [N] arquivos, [total] linhas

Conformidade:
  - Frontmatter: [completo/incompleto]
  - verificado_em: [data] ([válido/vencido])
  - Cláusulas universais: [lista]
  - Casos-teste: [N] ([positivos]/[negativos])

Fadiga estrutural:
  - Sinais ativos: [N de 5]
  - Detalhe: [lista]
  - Refator: [necessário/não necessário]

Recursos compartilhados:
  - Consome: [N itens]
  - Próprios duplicados em outras skills: [N]

Recomendações:
  [lista priorizada]
```
