# Princípios Anthropic 2026 — P1-P8 aplicados à biblioteca AM

Princípios do skill-creator oficial (Anthropic 2026) integrados à arquitetura V4.

## P1 — Progressive disclosure (3 camadas)

Princípio: skill revela conteúdo em camadas, do mais essencial ao mais detalhado.

Camadas:
- **Camada 1 — Frontmatter**: identidade, escopo, gatilhos. Sempre lido pelo modelo.
- **Camada 2 — SKILL.md corpo**: pipeline, regras, calibração. Lido quando skill ativa.
- **Camada 3 — References**: detalhamento operacional. Lido sob demanda.

Aplicação na biblioteca AM:
- Frontmatter ≤ 40 linhas
- SKILL.md core ≤ 500 linhas (ideal ≤ 300)
- References só carregam quando seção correspondente é executada
- Examples só carregam para testes

Benefício: economia de contexto, latência menor, performance melhor.

## P2 — SKILL.md ≤ 500 linhas

Princípio: limite duro para o arquivo principal.

Aplicação:
- Auditoria 1 verifica
- Refator automático sugerido > 450 linhas
- Refator obrigatório > 500 linhas

Modularização canônica para skill que cresce:
- Pipeline operacional detalhado → `references/01-pipeline.md`
- Regras condicionais complexas → `references/02-regras.md`
- Tabelas de decisão → `references/03-decisao.md`
- Vocabulário específico → `references/04-vocabulario.md`

## P3 — Uma skill, um trabalho

Princípio: cada skill tem propósito único e bem definido.

Aplicação:
- §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- Verificação 1 (duplicidade) bloqueia skill com múltiplos propósitos
- Auditoria 6 (pragmática) verifica clareza de propósito

Antipadrão: skill que faz "monitoramento + cadastro + análise". Quebrar em três.

## P4 — Categoria declarada

Princípio: skill explicita se é capability ou preference.

Definições:
- **Capability**: faz algo, produz output, outras chamam. Skill autônoma.
- **Preference**: configura comportamento. Não produz output isolado. Modifica como outras operam.
- **Mista**: faz e configura. Raras; justificar.

Aplicação:
- Frontmatter `categoria` obrigatório
- Verificação 3 valida com justificativa
- Mista exige justificativa robusta

## P5 — Skills cultivadas, não construídas

Princípio: skills evoluem por uso real, não por especulação.

Aplicação:
- Modo Cultivate audita uso real
- Lições capturadas via gotcha-skill
- Refator quando há evidência de fadiga (3+ sinais)
- Não refator sem necessidade (R11 — economia)

Diferença prática:
- Construída: prever todos os casos, criar features especulativas
- Cultivada: começar mínimo, evoluir conforme uso

A biblioteca AM segue cultivo: cada refator é resposta a problema real.

## P6 — Quatro coordenadas no frontmatter

Princípio (adaptação AM): toda skill localizada em 4 dimensões.

Coordenadas:
- `project: ProjNN` (1-7)
- `nucleo: NN` (N1-N6)
- `frente: FN` (F1-F6 ou transversal)
- `camada: CN` (C0-C9)

Aplicação:
- Verificação 2 confirma presença
- Auditoria 2 verifica coordenadas válidas
- Inconsistência: alerta vermelho

Diferença do oficial Anthropic: o oficial tem apenas categoria. AM adiciona 3 coordenadas para integrar à arquitetura V4.

## P7 — Backup R3 obrigatório

Princípio (adaptação AM): toda modificação preserva original.

Aplicação:
- Script `backup_skill.py` antes de qualquer edição
- Falha de backup = aborta operação
- Backups em `_backups/[NOME]/[NOME]-YYYYMMDD-HHMMSS.ext`
- Preservação por mínimo 30 dias (janela do Undo)

Diferença do oficial: oficial não tem mecanismo de backup. AM adiciona como cláusula universal.

## P8 — 70% da iteração mora na description

Princípio: maior alavanca de performance é o campo `description`.

Aplicação:
- Verificação 4 valida gatilhos linguísticos
- Auditoria 5 valida formato VERBO + GATILHOS + PROIBIÇÃO INVERSA
- Iteração sucessiva refina descrição com base em ativações reais
- Modo Improve sugere ajustes em description quando falsos positivos/negativos detectados

Estrutura canônica de description:

```
[VERBO IMPERATIVO frase 1].
INVOQUE quando [contexto + situação típica].
Gatilhos: "[palavra 1]", "[palavra 2]", "[palavra 3]" [...].
NÃO use para: [cenário 1], [cenário 2], [cenário 3].
```

---

## Tabela resumo

| Princípio | Aplicação concreta na AM | Auditoria correspondente |
|---|---|---|
| P1 | Frontmatter compacto + references sob demanda | A1, A2 |
| P2 | ≤ 500 linhas core | A1 |
| P3 | §1 FAÇO/NÃO FAÇO/DELEGO PARA | V1, A6 |
| P4 | categoria + justificativa | V3, A2 |
| P5 | Cultivate + gotcha-skill + refator com evidência | Modo Cultivate |
| P6 | 4 coordenadas no frontmatter | V2, A2 |
| P7 | backup_skill.py obrigatório | Sempre |
| P8 | description com VERBO+GATILHOS+PROIBIÇÃO | V4, A5 |

---

## Diferenças entre oficial Anthropic e adaptação AM

| Aspecto | Oficial | AM |
|---|---|---|
| Coordenadas | apenas categoria | 4 coordenadas + categoria |
| Backup | manual | automático via R3 |
| Auditoria mensal | inexistente | R9 obrigatório |
| Lições acumuladas | inexistente | L1-L10 (mod4) |
| Cláusulas universais | inexistente | R1-R11 inseridas conforme tipo |
| Vocabulário canônico | inexistente | glossário vivo consultado |
| _compartilhados/ | inexistente | núcleo comum |
| Princípio do escudo prévio | inexistente | aplicado em skills C5 |
| Quadro de Contato | inexistente | em peças processuais |
| Auto-percepção | parcial | 5 eixos sistemáticos |

A adaptação AM herda fundação Anthropic e adiciona camadas específicas do escritório, governança, integração com Drive vivo e versionamento canônico.
