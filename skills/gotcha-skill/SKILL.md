---
name: gotcha-skill
description: |
  Registra lições aprendidas a partir de falhas, comportamentos inesperados ou correções realizadas em skills da biblioteca Almeida Marques. Formata cada lição no padrão L[N] e appenda ao arquivo _compartilhados/informacoes/licoes-aprendidas.md. INVOQUE quando: "registra essa lição", "aprendi algo sobre skills", "adiciona ao log", "gotcha", "isso virou lição", "anota que não devo fazer X", "adicionar L[N]", "skill me surpreendeu", "documenta o erro". NÃO use para: criar skill nova (→ skill-creator-am), auditar a biblioteca (→ governanca-skills), revisar skill recém-criada (→ autorrevisao-skill), corrigir frontmatter (→ edição direta ou skill-creator-am Edit).
project: Proj02
nucleo: N5
frente: transversal
camada: C6
categoria: capability
justificativa: Fecha o ciclo de melhoria contínua — sem registro, as lições se perdem entre sessões
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to: []
licoes_aplicadas:
  - L2, L3, L12, L19, L20, L21
regras_aplicaveis:
  - R2, R3, R6, R10, R11
---

# gotcha-skill — Registro de lições aprendidas

## §0 — Ativação e gate

Antes de registrar, coleto os três campos obrigatórios:

1. **Skill afetada** (nome exato ou "geral" se aplicável a toda a biblioteca)
2. **Descrição do comportamento inesperado** (o que aconteceu vs. o que era esperado)
3. **Como foi descoberto** (auditoria R9, uso em produção, autorrevisao-skill, observação direta)

Se qualquer campo estiver ausente, pergunto antes de prosseguir. Não invento contexto.

## §1 — Escopo

FAÇO:
- Ler o arquivo `_compartilhados/informacoes/licoes-aprendidas.md` para identificar o próximo número L[N]
- Classificar a lição em uma das categorias: frontmatter, gate, output, dependência, gatilho, cadeia, isolamento
- Verificar se lição similar já existe (refinamento vs. duplicata)
- Formatar o bloco L[N] conforme MODELOS/entrada-licao.md
- Apresentar o bloco à usuária para confirmação antes de escrever
- Appender o bloco ao arquivo de log após confirmação
- Informar o número L[N] atribuído e o total de lições no arquivo

NÃO FAÇO:
- Corrigir automaticamente a skill afetada (delego para skill-creator-am modo Edit)
- Registrar lições sobre casos jurídicos (escopo exclusivo: skills da biblioteca)
- Alterar ou reescrever lições já registradas (lições são imutáveis; refinamentos geram nova entrada)
- Criar o arquivo licoes-aprendidas.md se não existir (informa a usuária e para)

## §2 — Pipeline de registro (4 passos)

```
P1. LEITURA DO LOG
    — Ler _compartilhados/informacoes/licoes-aprendidas.md
    — Identificar último L[N] existente → próximo = N+1
    — Verificar se lição similar já existe (busca por palavras-chave na descrição)

P2. CLASSIFICAÇÃO
    — Atribuir categoria primária:
        frontmatter   → campo ausente ou incorreto no SKILL.md
        gate          → §0 fraco ou inexistente
        output        → output declarado ≠ output real, null bytes, formato errado
        dependência   → depends_on aponta para arquivo/tool errado
        gatilho       → gatilho ativa no contexto errado ou não ativa quando deveria
        cadeia        → chains_to quebrado, chain depth > 3, contrato de schema ausente
        isolamento    → skill pressupõe contexto de sessão anterior (A20)
        outro         → registrar com justificativa

P3. FORMATAÇÃO
    — Montar bloco conforme MODELOS/entrada-licao.md
    — Apresentar à usuária para confirmação

P4. APPEND
    — Após confirmação: appender bloco ao final de licoes-aprendidas.md
    — Confirmar: "Lição L[N] registrada. Total no arquivo: [X] lições."
```

## §3 — Output canônico

Ao final do pipeline, apresento:

```
gotcha-skill: LIÇÃO REGISTRADA
L[N]: [título em uma linha]
skill_afetada: [nome ou "geral"]
categoria: [categoria primária]
arquivo: _compartilhados/informacoes/licoes-aprendidas.md
total_no_arquivo: [X] lições
```

Se a lição for duplicata ou refinamento de existente:

```
gotcha-skill: DUPLICATA DETECTADA
lição_existente: L[M] — [título]
acao: refinamento adicionado à L[M] como nota | nova entrada L[N] criada com remissão
```

## §4 — Calibração

VERIFICAR: arquivo `_compartilhados/informacoes/licoes-aprendidas.md` existe e está acessível
DADO NECESSÁRIO: skill afetada + descrição + como foi descoberto

Limite: uma entrada por invocação. Para múltiplas lições, invocar uma vez por lição.

## §5 — Auto-verificação

Verificação: 2026-05-12 · Próxima: 2026-08-12

Checklist:
- [x] Frontmatter V4 completo
- [x] verificado_em ≤ 90 dias
- [x] §0 com gate explícito (3 campos obrigatórios)
- [x] §1 FAÇO/NÃO FAÇO
- [x] Output canônico com variante duplicata
- [x] Tamanho dentro do limite
