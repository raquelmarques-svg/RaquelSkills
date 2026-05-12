---
name: pericia-acidentaria
description: |
  Produz e avalia documentação de perícia médica em ações acidentárias brasileiras: nexo técnico epidemiológico (NTEP), impugnação de laudo, nova perícia (art. 480 CPC), quesitos complementares, análise de concausa, controle de qualidade pericial, benefícios B91/B94/B92. Acionar quando a usuária mencionar: laudo pericial (acidentário), impugnação de laudo, quesitos, nova perícia, art. 480 CPC, anamnese ocupacional, NTEP, CNAE x CID, concausa, capacidade laborativa, laudo sem anamnese, laudo que não afasta o nexo, contradição no laudo, perito não respondeu quesitos, B91, B94, B92.
project: Proj02
nucleo: N1
frente: acidentaria
camada: C5
categoria: capability
version: 2.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
justificativa: Cobre o ciclo completo de perícia em ação acidentária — quesitos, impugnação, nexo NTEP — output concreto e processualmente acionável
depends_on: []
chains_to:
  - mod4
  - replica
licoes_aplicadas:
  - L1, L2, L3, L5, L6, L10, L11
regras_aplicaveis:
  - R1, R2, R3, R6, R10, R11
---

# pericia-acidentaria — Perícia Médica em Ação Acidentária

## §0 — Ativação e gates

Ativar quando a usuária mencionar: laudo pericial (acidentário), impugnação de laudo, NTEP,
CNAE x CID, concausa, anamnese ocupacional, nova perícia, B91/B94/B92.

## §0 — Regras universais

R1 (exportação): perguntar antes de gerar DOCX ou PDF.
R2 (preservação): nunca deletar; itens removidos vão para `_APAGAR/` com timestamp.
R3 (backup): backup antes de modificar SKILL.md existente.
R6 (adaptação): propor ajuste antes de recusar.
R10 (discordância útil): apontar inconsistência técnica no laudo antes de redigir a peça.
R11 (economia de ação): ponderar custo antes de propor solução cara.

## §1 — Escopo

FAÇO:
- Classificação do laudo por tipo (A/B/C conforme pergunta jurídica respondida)
- Identificação de admissão implícita de concausa no texto do laudo
- Protocolo de saída: análise de laudo, impugnação, pedido art. 480, quesitos complementares
- Formulação de quesitos estratégicos (mínimo 12, ideal 18–22)
- Controle de qualidade pré-entrega (6 verificações)

NÃO FAÇO:
- Réplica à contestação integral → delego para `replica`
- Análise de laudo previdenciário (doença comum, BPC-LOAS) → delego para `pericia-previdenciaria`
- Formatação DOCX final → delego para `mod4`
- Organização de pasta do cliente → delego para `juridir`

DELEGO PARA:
- `replica` — petição de réplica completa
- `pericia-previdenciaria` — laudo em ação previdenciária pura
- `mod4` — formatação .docx

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Laudo acidentário | "laudo veio", "laudo sem anamnese", "perito não aplicou NTEP" |
| NTEP | "CNAE x CID", "presunção não afastada", "art. 21-A" |
| Concausa | "perito admitiu concausa", "trabalho piora os sintomas" |
| Quesitos | "formular quesitos", "quesitos complementares acidentário" |
| Nova perícia | "art. 480 CPC", "laudo metodologicamente insuficiente" |

NÃO disparo quando: laudo é previdenciário puro (→ `pericia-previdenciaria`), réplica integral
(→ `replica`), formatação (→ `mod4`).

---

## §3 — Leituras obrigatórias antes de qualquer saída

1. `ASSETS/normas_aplicaveis.md` — base normativa completa
2. `ASSETS/checklist_laudo_qualidade.md` — 18 critérios de controle
3. `ASSETS/vocabulario_controlado.md` — terminologia invariável
4. `ASSETS/framing_e_retorica.md` — enquadramento estratégico
5. O laudo pericial concreto fornecido pela usuária
6. Os quesitos já formulados pelas partes, se houver

---

## §4 — Classificação do laudo (obrigatória antes de qualquer peça)

**TIPO A** — responde à pergunta da presunção do NTEP: analisa CNAE x CID, condições
laborativas concretas, anamnese ocupacional, epidemiologia. Pode afastar a presunção.

**TIPO B** — responde à pergunta do nexo clínico direto: examina o segurado clinicamente
sem analisar epidemiologia nem condições laborativas. NÃO afasta a presunção do NTEP.
É o tipo mais comum produzido pelo INSS em contestações padrão.

**TIPO C** — responde à pergunta da incapacidade atual: avalia se o segurado pode trabalhar
hoje. Juridicamente impertinente para a presunção do NTEP.

Laudo Tipo B ou C nunca afasta a presunção (STJ REsp 1.306.113/SC). A classificação
determina o argumento principal da impugnação.

---

## §5 — A pergunta jurídica correta (invariável)

Para afastar a presunção do NTEP (art. 21-A Lei 8.213/91), o laudo deve responder:

> "As condições laborativas concretas do segurado, no CNAE indicado, NÃO contribuíram,
> nem como concausa, para o desencadeamento ou agravamento da patologia CID indicada?"

Qualquer laudo que não responda especificamente a essa pergunta é insuficiente para afastar
a presunção, independentemente da qualidade clínica da avaliação.

---

## §6 — Ônus da prova (regra fixa)

O ônus de afastar a presunção do NTEP é integralmente do INSS (art. 21-A Lei 8.213/91).
A autora não precisa provar o nexo: precisa demonstrar que o INSS não o afastou.

Estrutura argumentativa invariável:
"Para afastar a presunção legal do NTEP, o INSS deveria ter produzido [X]. Não produziu.
Portanto, a presunção permanece íntegra."

---

## §7 — Concausa (regra fixa)

O art. 21, §1º, Lei 8.213/1991 exige apenas contribuição do trabalho para o desencadeamento
ou agravamento, não causação exclusiva.

Monitorar no laudo expressões que admitem concausa implicitamente:
- "pode intensificar", "pode agravar", "pode desencadear"
- "tarefas sobrecarregam", "carga aumenta o risco"
- "em articulações já acometidas", "em estruturas previamente lesadas"
- qualquer variante de "o trabalho piora os sintomas"

Essas expressões somadas ao art. 21, §1º configuram concausa admitida pelo próprio perito,
utilizável contra a conclusão do laudo.

---

## §8 — Protocolo de saída por tipo de tarefa

### Análise de laudo

1. Classificação do tipo (A, B ou C)
2. Pergunta que o laudo respondeu versus pergunta que a lei impõe
3. Contradições internas: achados clínicos incompatíveis com a conclusão
4. Admissões implícitas de concausa identificadas no texto do laudo
5. Critérios do checklist não atendidos (numerar com referência ao ASSET)
6. Conclusão: a presunção do NTEP foi afastada? Com fundamento explícito.

### Impugnação de laudo

Incluir sempre:
- (a) argumento metodológico: pergunta errada respondida
- (b) argumento probatório: ausência de anamnese ocupacional
- (c) argumento lógico: contradição interna do laudo
- (d) argumento normativo: NTEP não afastado (art. 21-A + STJ)
- (e) quesitos complementares numerados (mínimo 12, ideal 18–22)

### Pedido de nova perícia (art. 480 CPC)

Especificar: especialidade do novo perito, mandato explícito (anamnese ocupacional +
análise CNAE x CID + capacidade laborativa sustentada para a função habitual).
Fundamentar na insuficiência metodológica do laudo existente, não na discordância
com a conclusão.

### Quesitos complementares

Sempre numerar. Sempre incluir quesito sobre o NTEP (bloco C). Sempre incluir quesito
de fechamento (perito mantém as conclusões após os quesitos?).

---

## §9 — Cadeia de benefícios e reflexos trabalhistas

Ler `ASSETS/cadeia_beneficios_acidentarios.md` sempre que houver questão sobre espécie de
benefício, conversão de espécie, cálculo de RMI, B94, B92 ou reflexos trabalhistas
(FGTS, estabilidade).

---

## §10 — Controle de qualidade pré-entrega

1. Argumento estruturado como NORMA → FATO → CONCLUSÃO?
2. Ônus corretamente atribuído ao INSS?
3. Pergunta jurídica correta explicitada?
4. Vocabulário controlado respeitado?
5. Concausa implícita no laudo foi identificada e explorada?
6. Cerceamento de defesa mencionado se quesitos não foram respondidos?

---

## §11 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] Distinção acidentário vs previdenciário explicitada no escopo
- [x] git_auto_commit declarado
- [x] Volume ≤ 500 linhas
