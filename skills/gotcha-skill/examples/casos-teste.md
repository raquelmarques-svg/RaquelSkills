# casos-teste — gotcha-skill

## CT-01 — Registro de lição nova (categoria: output)

**Entrada fornecida à skill:**
- skill_afetada: skill-creator-am
- comportamento: Write tool gerou arquivo com null bytes, tornando-o binário
- descoberto_via: bash `file SKILL.md` retornou "data" em vez de "UTF-8 text"

**Output esperado:**
- Próximo número identificado corretamente (ex.: L22 se L21 for o último)
- Categoria classificada como `output`
- Bloco formatado conforme MODELOS/entrada-licao.md
- Confirmação solicitada antes de appender
- Após confirmação: "Lição L22 registrada. Total no arquivo: 22 lições."

**Critério de aprovação:** bloco apresentado antes de qualquer escrita; append só após confirmação.

---

## CT-02 — Tentativa de lição duplicata

**Entrada fornecida à skill:**
- skill_afetada: geral
- comportamento: git_auto_commit: true causou commit acidental
- descoberto_via: produção

**Contexto:** L19 já registra exatamente esse comportamento.

**Output esperado:**
```
gotcha-skill: DUPLICATA DETECTADA
lição_existente: L19 — Nunca definir git_auto_commit: true sem pipeline §4-G verificado
acao: refinamento adicionado à L19 como nota | nova entrada L[N] criada com remissão
```
Pergunta à usuária: refinamento de L19 ou nova entrada com remissão?

**Critério de aprovação:** skill não appenda sem decisão da usuária sobre duplicata.

---

## CT-03 — Invocação sem campos obrigatórios

**Entrada:** "gotcha — aprendi algo sobre chains_to hoje"

**Output esperado:**
Gate ativa. Skill pergunta:
1. Qual skill afetada?
2. O que aconteceu vs. o que era esperado?
3. Como foi descoberto?

**Critério de aprovação:** skill para e pergunta; não inventa contexto nem cria entrada parcial.

---

## CT-04 — Arquivo licoes-aprendidas.md inexistente

**Simulação:** arquivo removido ou caminho incorreto.

**Output esperado:**
```
gotcha-skill: BLOQUEADA
motivo: _compartilhados/informacoes/licoes-aprendidas.md não encontrado
acao_requerida: verificar caminho ou criar arquivo antes de invocar gotcha-skill
```

**Critério de aprovação:** skill informa e para; não cria o arquivo por conta própria.

---

## CT-05 — Lição sobre caso jurídico (fora do escopo)

**Entrada:** "aprendi que BPC com renda per capita de R$ 300 deve ser analisado pelo critério..."

**Output esperado:**
Skill identifica que a lição é sobre caso jurídico, fora do escopo da biblioteca de skills.
Informa: "gotcha-skill registra apenas lições sobre skills da biblioteca. Para registrar aprendizados jurídicos, use diretamente o arquivo de anotações do caso."

**Critério de aprovação:** skill recusa sem executar pipeline.
