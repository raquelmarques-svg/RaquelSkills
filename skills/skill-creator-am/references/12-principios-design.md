# skill-creator-am / reference 12 — Princípios de design de software aplicados a skills

Esta reference é consultada obrigatoriamente durante V9 (blueprint arquitetural) e durante toda criação, edição ou refatoração de skill. Os princípios aqui não são recomendações — são critérios de design que a skill-creator-am aplica ativamente antes de gerar qualquer SKILL.md.

---

## 1. SOLID adaptado para skills

### S — Single Responsibility Principle (SRP)

Uma skill faz uma coisa. Uma coisa significa: um propósito exprimível em uma frase com verbo + objeto específico + contexto.

Teste SRP: "Esta skill [VERBO] [OBJETO] [CONTEXTO]." Se a frase precisar de "e" para ser completa, a skill viola o SRP.

Exemplos:
- "Analisa o cálculo de renda per capita de processos BPC/LOAS indeferidos por renda." ✓
- "Analisa o cálculo de renda E gera blocos visuais PNG." ✗ → duas skills

### O — Open/Closed Principle

Skills são abertas para extensão (novos domínios, novos tipos de input) e fechadas para modificação de contrato (o schema de input/output não muda — estende).

Aplicação: SCHEMAS/ usa versionamento semântico. `v1.0` → `v1.1` adiciona campos opcionais. `v2.0` quebra contrato — exige migração explícita e notificação a `depends_on`.

### L — Liskov Substitution Principle

Skills do mesmo tipo (ex: duas skills C5 de redação de peça) devem ser intercambiáveis para o caller. Se `replica-acidentaria` e `replica-previdenciaria` existem, ambas recebem `dossie-caso` como input e entregam `petição_estruturada` como output — com schemas compatíveis.

### I — Interface Segregation Principle

Não existe "super-skill" com 20 funções. Cada interface (schema de input) declara apenas os campos que aquela skill realmente usa. Um caller não deve receber informação que não pediu.

Aplicação: skill com schema que tem 15+ campos obrigatórios está violando ISP — decomporta em skills menores com schemas menores.

### D — Dependency Inversion Principle

Skills de alto nível (C5 redação) não dependem de skills de baixo nível (C3 extração). Ambas dependem de abstrações (schemas).

Aplicação: `replica` não chama `pericia-acidentaria` diretamente — ela consome o JSON canônico `analise_pericial.schema.json`. Quem produziu o JSON é irrelevante para `replica`. Isso permite substituir `pericia-acidentaria` por outra skill sem tocar em `replica`.

---

## 2. Domain-Driven Design (DDD) adaptado

### Bounded Context

Cada frente (F1-F6) é um bounded context. Skills de F1 (previdenciário) não devem conter lógica de domínio de F4 (família). Quando um termo existe nos dois domínios com significados diferentes ("renda" em BPC ≠ "renda" em alimentos), cada bounded context tem sua própria definição — não há sharing de conceito entre frentes sem schema explícito de tradução.

### Ubiquitous Language

O glossário em `references/08-glossario-arquitetural.md` é a linguagem ubíqua da biblioteca. Todo SKILL.md, todo schema, todo script usa os termos canônicos do glossário. Variantes proibidas = vocabulário de outro contexto contaminando o atual.

Aplicação na criação: antes de nomear campos do schema, verificar o glossário. Se o termo não existe, propor adição ao glossário antes de criar o schema.

### Aggregate Root

Em composições de skills (ex: `dossie-caso` → `analise-renda-bpc` → `widget-visual` → `mod4`), o `dossie-caso` é o aggregate root — ele detém a verdade sobre o caso e todas as skills downstream derivam seus dados dele, nunca de fontes paralelas.

Consequência: uma skill nunca pergunta ao usuário algo que já está no `dossie-caso`. Se o dado não está no dossier, a skill pede à Raquel para atualizar o dossier primeiro.

### Repository Pattern

Assets compartilhados (`_compartilhados/ASSETS/`) são repositórios de domínio. Uma skill acessa dados de domínio (SM histórico, normas BPC, jurisprudência) sempre via repositório — nunca hardcoded no corpo da skill.

---

## 3. Design Patterns aplicados

### Strategy Pattern

Quando uma skill precisa comportar-se diferentemente conforme o tipo de input, usa o Strategy Pattern: define uma interface comum e cria variantes.

Aplicação: `pericia-acidentaria` e `pericia-previdenciaria` implementam a mesma interface `analise_pericial` com estratégias distintas. `replica` consome `analise_pericial` sem saber qual estratégia produziu o resultado.

### Command Pattern

Toda ação irreversível de uma skill é encapsulada como comando com: nome, parâmetros, resultado esperado, mecanismo de undo (R3 + R2).

Aplicação: o pipeline §4-G (Git sync) é um Command. O backup R3 é o pré-condição do comando. O undo é o modo Undo da skill-creator-am.

### Factory Pattern

A skill-creator-am usa Factory para instanciar a estrutura correta de skill conforme o tipo declarado:
- capability → instancia SKILL.md + MODELOS/ + ASSETS/ + SCHEMAS/ + examples/
- preference → instancia SKILL.md + references/ + examples/ (sem MODELOS/)
- transversal C0 → instancia SKILL.md + scripts/ + tests/ + examples/

### Observer Pattern

O ciclo R9 (auditoria mensal) é um Observer: `governanca-skills` observa todas as skills da biblioteca e dispara quando `verificado_em` > 90 dias ou quando um skill muda de estado.

---

## 4. Princípios de Arquitetura de Sistemas

### Separation of Concerns (SoC)

Cada camada cuida de uma preocupação:
- C3 (extração) — preocupação: onde e como obter os dados
- C4 (análise) — preocupação: o que os dados significam juridicamente
- C5 (redação) — preocupação: como expressar o significado em petição
- C0 (formatação) — preocupação: como apresentar visualmente o output

Uma skill que mistura duas preocupações viola SoC. V8 detecta isso.

### Loose Coupling, High Cohesion

Acoplamento mínimo entre skills: skills se comunicam via schemas versionados, nunca via contexto implícito ou memória de sessão. Alta coesão interna: tudo dentro de uma skill serve ao mesmo propósito.

Métrica: se remover uma função da skill não quebra nada externo, a função tem baixo acoplamento. Se remover uma função da skill quebra o propósito declarado, a função tem alta coesão — está no lugar certo.

### Idempotência

Scripts de uma skill podem ser executados múltiplas vezes com o mesmo input e produzem sempre o mesmo output, sem efeitos colaterais acumulados.

Aplicação: `html_para_png.py` com o mesmo JSON de blocos sempre produz o mesmo PNG. O output não depende de estado anterior. R1 (confirmação antes de exportar) é o gate de idempotência — garante que a execução é intencional.

### State Machine

Skills com pipeline multi-etapa declaram os estados possíveis e as transições:

```
IDLE → ATIVADA → VERIFICANDO_INPUT → PROCESSANDO → OUTPUT_PRONTO → ENTREGUE
                        ↓                    ↓
                   ERRO_INPUT           ERRO_PROCESSO
                        ↓                    ↓
                   AGUARDANDO_CORRECAO   REPORTANDO_ERRO
```

O §0-Autopercepção da skill é a implementação da state machine: antes de produzir output, verifica o estado atual e as condições de transição.

### CRC (Class-Responsibility-Collaboration)

Antes de criar qualquer skill, preencher o cartão CRC:

| Campo | Pergunta | Resposta |
|---|---|---|
| Nome | Qual é o componente? | `analise-renda-bpc` |
| Responsabilidade | O que faz? (uma frase) | Analisa cálculo de renda BPC e identifica vícios |
| Colaboração upstream | Quem me alimenta? | `dossie-caso` via `calculo_renda.schema.json` |
| Colaboração downstream | Quem me consome? | `widget-visual` via `blocos_visuais.schema.json` |
| Não-responsabilidade | O que explicitamente NÃO faço? | Não renderizo PNG, não redijo petição |

O cartão CRC é preenchido durante V9 e arquivado em `references/` da skill como `00-crc.md`.
