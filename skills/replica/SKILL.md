---
name: replica
description: |
  Produz réplica estratégica em ações acidentárias e previdenciárias brasileiras. Cobre: leitura e classificação da contestação do INSS, mapeamento de admissão ficta (CPC art. 341), reforço de presunção NTEP, impugnação de vício de espécie beneficiária (B31/B87 → B91/B94/B92), expansão de pedidos (auxílio-acidente, FGTS, estabilidade, danos morais). Acionar quando a usuária mencionar: réplica, contestação do INSS, resposta à contestação, admissão ficta, art. 341, rebater contestação, INSS contestou, contestação veio, o que fazer com a contestação, refutar defesa do INSS.
project: Proj02
nucleo: N1
frente: acidentaria-previdenciaria
camada: C5
categoria: capability
version: 3.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: true
depends_on: []
chains_to:
  - mod4
  - pericia-acidentaria
  - pericia-previdenciaria
licoes_aplicadas:
  - L1, L2, L3, L5, L6, L10, L11
regras_aplicaveis:
  - R1, R2, R3, R6, R10, R11
---

# replica — Réplica Estratégica em Ações Acidentárias e Previdenciárias

## §0 — Ativação e gates

Ativar quando a usuária mencionar: réplica, contestação do INSS, admissão ficta, art. 341,
rebater contestação, INSS contestou, contestação veio, refutar defesa do INSS.

## §0 — Regras universais

R1 (exportação): perguntar antes de gerar DOCX ou PDF.
R2 (preservação): nunca deletar; itens removidos vão para `_APAGAR/` com timestamp.
R3 (backup): backup antes de modificar SKILL.md existente.
R6 (adaptação): propor ajuste antes de recusar.
R10 (discordância útil): apontar inconsistência ou omissão estratégica antes de gerar.
R11 (economia de ação): ponderar custo antes de propor solução cara.

## §1 — Escopo

FAÇO:
- Diagnóstico da contestação por Tipo I/II/III
- Mapeamento de admissão ficta (CPC art. 341)
- Argumento de NTEP e presunção iuris tantum
- Impugnação de vício de espécie (B31/B87 → B91/B94/B92)
- Expansão de pedidos: B94, B92, FGTS, estabilidade, danos morais
- Produção da petição de réplica completa com seções pertinentes ao caso

NÃO FAÇO:
- Análise técnica de laudo pericial → delego para `pericia-acidentaria` (acidentário) ou `pericia-previdenciaria` (previdenciário)
- Formatação DOCX final → delego para `mod4`
- Análise de precedente jurisprudencial → delego para `analise-precedente`

DELEGO PARA:
- `pericia-acidentaria` — impugnação técnica de laudo acidentário
- `pericia-previdenciaria` — impugnação técnica de laudo previdenciário
- `mod4` — formatação do .docx final
- `analise-precedente` — análise de decisões judiciais invocadas pelo INSS

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Pedido de réplica | "escreva a réplica", "preciso rebater a contestação" |
| Classificação da defesa | "leia a contestação", "o que o INSS contestou" |
| Admissão ficta | "o que o INSS não contestou", "art. 341" |
| Expansão de pedidos | "quais pedidos incluir", "B94, B92, FGTS" |
| Vício de espécie | "INSS concedeu B31 em vez de B91" |

NÃO disparo quando: pedido é análise técnica de laudo (→ `pericia-acidentaria`/`pericia-previdenciaria`), formatação DOCX (→ `mod4`).

---

## §3 — Leitura diagnóstica da contestação

Antes de qualquer produção textual, classificar cada argumento em uma das três categorias:

**Tipo I — Silêncio ou negativa genérica**: o INSS não impugnou o fato especificadamente.
Consequência: admissão ficta automática (CPC art. 341). Não cabe rebater, só declarar.

**Tipo II — Impugnação específica sem prova**: o INSS contestou e não juntou documento novo.
Consequência: ônus não cumprido; negativa não supera a prova documental do autor. Rebater
com inversão do ônus e reforço da prova inicial.

**Tipo III — Impugnação com suporte probatório**: o INSS apresentou laudo, resolução ou prova.
Consequência: análise crítica do conteúdo, identificação de vício ou insuficiência técnica.
Para laudos periciais: acionar `pericia-acidentaria` ou `pericia-previdenciaria`.

### Perguntas de diagnóstico obrigatórias

1. Quais fatos da inicial o INSS não impugnou expressamente? → Lista para admissão ficta.
2. O INSS contestou o NTEP? Com qual fundamento? Juntou laudo contrário?
3. O INSS contestou a espécie do benefício (B91 vs. B31/B87)? Qual argumento?
4. O INSS impugnou o nexo causal? Invocou doença degenerativa ou causa exclusivamente pessoal?
5. O laudo pericial já saiu? O INSS invocou laudo como fundamento da contestação?
6. Há processo administrativo juntado pelo réu? (Se sim: nenhum ofício é necessário.)
7. Há pedidos de B94, B92, FGTS, estabilidade ou danos morais na inicial? Se não, cabe inclusão na réplica?

---

## §4 — Estrutura-padrão da réplica

```
I.   DO CABIMENTO E DA TEMPESTIVIDADE
II.  DA ADMISSÃO FICTA — CPC ART. 341
III. DO NTEP E DA PRESUNÇÃO IURIS TANTUM
IV.  DO VÍCIO DE ESPÉCIE (quando aplicável)
V.   DO NEXO CAUSAL E DA CONCAUSA (quando impugnado)
VI.  DAS PROVAS REQUERIDAS
VII. DOS PEDIDOS
```

Omitir seções sem suporte fático no caso concreto. Não criar seção vazia.

---

## §5 — Admissão ficta (CPC art. 341)

Aplicar sempre que o INSS não impugnar fato específico. Silêncio e negativa genérica
equivalem para fins do art. 341.

Fatos tipicamente não impugnados pelo INSS: data de admissão, função exercida, CNAE do
empregador, CID do diagnóstico, datas dos NBs, RMI registrada no CNIS, meses de afastamento,
DIB e DCB dos benefícios.

---

## §6 — NTEP — presunção iuris tantum

A presunção do art. 21-A da Lei 8.213/91 opera de pleno direito quando CNAE e CID constam
da Lista A (Decreto 3.048, Anexo II). Para afastar a presunção, o INSS precisa de prova
robusta de causa exclusivamente pessoal (STJ Tema 503). Negativa genérica não afasta.

Estrutura do argumento:
- Norma: art. 21-A Lei 8.213/91 + STJ Tema 503
- Fato: CNAE X × CID Y constam da Lista A → presunção operou
- Prova do INSS: [ausente / insuficiente / genérica]
- Conclusão: presunção íntegra; nexo presumido deve ser mantido

---

## §7 — Vício de espécie beneficiária

Quando o INSS concedeu B31 (auxílio-doença comum) ou B87 (auxílio-doença acidentário com
coeficiente redutor EC 103) em vez de B91 (auxílio por incapacidade temporária acidentária,
100% SB):

- Norma: art. 86 Lei 8.213/91; EC 103/2019 art. 26 §2º
- Fato: NB concedido com espécie errada + diferença de RMI calculada
- Consequência: prejuízo financeiro desde a DIB original (não apenas da DCB)
- Pedido: retificação da espécie + pagamento de diferenças

---

## §8 — Pedidos — expansão acidentária completa

Verificar se a inicial já requereu a cadeia completa. Se não, incluir na réplica:

a) Retificação da espécie para B91 desde a DIB original
b) B94 (auxílio-acidente, art. 86 Lei 8.213) — 50% SB após cessação do B91
c) B92 (aposentadoria por invalidez acidentária, art. 42 §2º) — se incapacidade permanente
d) Depósitos de FGTS pelo período de afastamento (art. 15 §5º Lei 8.036/90)
e) Estabilidade acidentária 12 meses (art. 118 Lei 8.213/91)
f) Danos morais se houver omissão do empregador no CAT ou negligência previdenciária
g) Honorários sucumbenciais

---

## §9 — Output por tarefa

| Tarefa solicitada | Output |
|---|---|
| "leia a contestação" | Diagnóstico por Tipo I/II/III + lista de admissão ficta |
| "escreva a réplica" | Petição completa com seções pertinentes |
| "quais são os pedidos" | Pedidos expandidos com fundamento |
| "o que o INSS não contestou" | Lista de fatos com admissão ficta |

---

## §10 — Proibições

Não redigir seção de provas requerendo documental já juntada pelo réu. Não redigir pedido
de depoimento pessoal sem instrução da autora. Não presumir que o laudo foi favorável ou
desfavorável sem ler o laudo. Não incluir fatos não presentes na inicial sem autorização.
Não usar travessão intercalador. Estrutura obrigatória: norma → fato → conclusão.

---

## §11 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] Laudo pericial delegado para pericia-acidentaria/pericia-previdenciaria
- [x] git_auto_commit declarado
- [x] Volume ≤ 500 linhas
