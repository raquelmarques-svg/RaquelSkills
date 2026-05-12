# skill-creator-am / reference 13 — ITIL e COBIT aplicados à biblioteca AM

---

## ITIL adaptado: skills como serviços gerenciados

### Princípio 1 — Foco no valor (Value Focus)

Toda skill deve responder: qual o valor entregue a Raquel, medido em resultado jurídico ou redução de esforço? Skills sem valor mensurável são candidatas a deprecação.

Pergunta de criação obrigatória: "Quanto tempo/esforço esta skill economiza por uso? Em que tipo de caso?"

Se a resposta for vaga ("ajuda na análise"), a skill não tem propósito definido — refusar criação até escopo ser preciso.

### Princípio 2 — Começar onde você está (Start Where You Are)

Antes de criar skill nova, auditar o que existe. A biblioteca atual tem N skills — alguma já cobre parcialmente o caso? Se sim, estender (modo Edit) antes de criar nova.

Aplicação: V1 (duplicidade) + V8 (análise funcional) juntas implementam este princípio.

### Princípio 3 — Progredir iterativamente com feedback (Iterate with Feedback)

Skills nascem em v1.0.0 com escopo mínimo viável. Extensões chegam em patches após uso real. Nenhuma skill nasce tentando cobrir todos os casos de uso possíveis.

Aplicação: `version: MAJOR.MINOR.PATCH`. PATCH = correção. MINOR = extensão sem quebra de contrato. MAJOR = quebra de contrato — exige migração das skills downstream.

### Princípio 4 — Colaborar e promover visibilidade (Collaborate and Promote Visibility)

`chains_to` e `depends_on` declarados em toda skill = visibilidade do catálogo de serviços. Sem esses campos, a biblioteca é opaca — ninguém sabe quem chama quem.

Catálogo de serviços = `_compartilhados/catalogo.md` (a criar via modo Cultivate): lista de todas as skills, versão, propósito, SLA declarado, última auditoria.

### Princípio 5 — Pensar e trabalhar de forma holística (Think and Work Holistically)

Uma mudança em uma skill pode quebrar skills downstream. Antes de editar qualquer SKILL.md ou schema, verificar o grafo de dependências: quem depende de mim? Minha mudança quebra o contrato deles?

Aplicação: modo Edit inclui passo de análise de impacto — listar todas as skills em `depends_on` da skill editada e verificar compatibilidade.

### Princípio 6 — Manter simples e prático (Keep It Simple and Practical)

Complexidade não é qualidade. Uma skill de 200 linhas que faz uma coisa bem é superior a uma skill de 600 linhas que tenta fazer tudo.

Métrica: se o §1 (FAÇO) tem mais de 8 itens, a skill provavelmente viola SRP. Refatorar.

### Princípio 7 — Otimizar e automatizar (Optimize and Automate)

Scripts em `_compartilhados/scripts/` são a automação da biblioteca. Toda tarefa repetida manualmente 3+ vezes em skills diferentes é candidata a script compartilhado.

---

## COBIT adaptado: governança da biblioteca

### EDM01 — Garantir estabelecimento e manutenção do framework de governança

O framework de governança da biblioteca é a própria `skill-creator-am` com V1-V9 + A1-A15 + R1-R11 + L1-L13. Ele não pode ser bypassado. Toda skill criada fora do pipeline da `skill-creator-am` é não-conforme e deve ser auditada pelo modo Govern antes de uso.

### EDM02 — Garantir entrega de valor

Cada skill tem um `SLA declarado` no frontmatter:

```yaml
sla:
  tempo_resposta: "< 2 turnos de chat"
  output_garantido: "análise textual + JSON estruturado"
  condicoes_de_falha: "PDF ilegível, data da decisão ausente"
  fallback: "reportar o que foi possível extrair + listar o que falta"
```

Sem SLA, a skill não tem critério de qualidade verificável.

### EDM03 — Garantir otimização de riscos

Riscos de uma skill são documentados em `references/` ou no próprio SKILL.md:
- Risco de dado desatualizado (SM, normas) → mitigado por `verificado_em ≤ 90 dias`
- Risco de output incorreto → mitigado por examples/ com casos negativos
- Risco de scope creep → mitigado por V8 em toda operação
- Risco de regressão → mitigado por `tests/` quando scripts/ existe

### APO01 — Gerenciar o framework de gerenciamento de TI

O `_inventario.md` em `C:\RaquelSkills\` é o CMDB (Configuration Management Database) da biblioteca. Cada skill é um CI (Configuration Item) com: nome, versão, camada, frente, `depends_on`, `chains_to`, `verificado_em`, status (ativo/depreciado/draft).

O inventário é atualizado automaticamente pelo pipeline §4-G após cada commit.

### BAI03 — Gerenciar identificação e construção de soluções

Toda skill nova passa pelo pipeline V1-V9 antes de existir. Não há criação ad-hoc. A documentação (SKILL.md + references/) é criada junto com a skill, nunca depois.

### DSS01 — Gerenciar operações

Modo Cultivate (auditoria mensal R9) é o processo DSS01 da biblioteca: verifica se todas as skills estão operacionais, dentro do prazo de verificação, sem regressão de schema.

### MEA01 — Gerenciar performance e conformidade do monitoramento

Métricas da biblioteca (a medir mensalmente via modo Cultivate):
- % de skills com `verificado_em ≤ 90 dias`
- % de skills com `chains_to` declarado
- % de skills com schema de input declarado
- Número de skills em estado "draft" (criadas mas sem examples/)
- Número de dependências quebradas (skill em `depends_on` que não existe)

---

## Checklist ITIL/COBIT para criação de skill (V9-ITIL)

```
[ ] IC-1: Propósito exprimível em uma frase (ITIL value focus)
[ ] IC-2: Auditoria de biblioteca feita antes de criar (ITIL start where you are)
[ ] IC-3: Escopo mínimo viável — sem gold-plating (ITIL keep it simple)
[ ] IC-4: chains_to + depends_on declarados (ITIL visibility)
[ ] IC-5: SLA declarado no frontmatter (COBIT EDM02)
[ ] IC-6: Riscos documentados em references/ (COBIT EDM03)
[ ] IC-7: CI registrado no _inventario.md após criação (COBIT APO01)
[ ] IC-8: Impacto em skills downstream analisado (ITIL holistic)
```
