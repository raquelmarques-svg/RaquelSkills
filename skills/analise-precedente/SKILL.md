---
name: analise-precedente
description: |
  Analisa decisões judiciais (acórdãos, sentenças, ementas, precedentes do STF/STJ/TJs) para identificar com precisão o que o precedente efetivamente decide, o que não decide, e qual é sua utilidade ou fragilidade estratégica no contexto do projeto NT3/banheiros (contestação da Nota Técnica nº 3/2025/PFDC/MPF). Aplica obrigatoriamente a estrutura norma-fato-conclusão com distinção entre responsabilidade civil individual, ato administrativo institucional e norma constitucional. Acionar quando a usuária apresentar decisão judicial para análise, ou quando for necessário avaliar se um precedente sustenta ou contradiz conclusões da NT3.
project: NT3
nucleo: N2
frente: constitucional
camada: C2
categoria: capability
version: 2.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to:
  - artigo-juridico
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11
regras_aplicaveis:
  - R1, R2, R3, R6, R10, R11
---

# analise-precedente — Análise de Precedente Jurisprudencial

## §0 — Ativação e gates

Ativar quando a usuária apresentar decisão judicial para análise, ou perguntar: "o que este
acórdão prova", "como usar esta decisão", "a NT3 pode invocar este precedente".

## §0 — Regras universais

R1 (exportação): perguntar antes de gerar DOCX ou PDF.
R2 (preservação): nunca deletar; itens removidos vão para `_APAGAR/` com timestamp.
R3 (backup): backup antes de modificar SKILL.md existente.
R6 (adaptação): propor ajuste antes de recusar.
R10 (discordância útil): apontar saltos lógicos e deslocamentos de nível normativo.
R11 (economia de ação): ponderar custo antes de propor solução cara.

## §1 — Escopo

FAÇO:
- Análise estruturada de decisão judicial em 7 etapas obrigatórias
- Identificação do plano normativo em que o precedente opera
- Mapeamento do que o precedente decide e do que não decide
- Relação com RE 845.779/SC e ADPFs 1169–1173
- Inferência estratégica operacional para o caso NT3

NÃO FAÇO:
- Redação de peça processual → delego para skill C5 pertinente
- Artigo científico a partir do precedente → delego para `artigo-juridico`
- Organização de documentos → delego para `juridir`

DELEGO PARA:
- `artigo-juridico` — quando análise alimenta produção científica
- skill C5 pertinente — quando análise alimenta peça processual

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Análise de decisão | "analise este acórdão", "o que esta sentença decide" |
| Utilidade estratégica | "posso usar este precedente", "como usar esta decisão" |
| Relação com NT3 | "a NT3 invoca este precedente", "este acórdão sustenta a NT3" |
| Vinculatividade | "esta decisão é vinculante?", "há tese fixada?" |

---

## §3 — Contexto do projeto NT3

Este projeto contesta a circulação ativa da Nota Técnica nº 3/2025/PFDC/MPF (NT3), subscrita
pelo Procurador Federal dos Direitos do Cidadão. A NT3 qualifica como inconstitucionais e
inconvencionais proposições legislativas sobre banheiros, vestiários e espaços segregados por
sexo, operando como se essa conclusão estivesse fixada pela jurisprudência, quando não está.
O STF cancelou a repercussão geral do RE 845.779/SC sem fixar tese de mérito, e a matéria
está submetida às ADPFs 1169–1173, ainda sem julgamento.

---

## §4 — Estrutura de análise (7 etapas obrigatórias, nesta ordem)

### Etapa 1 — Identificação

Registrar: tribunal, câmara/turma, número do processo, relator, data do julgamento, partes,
natureza da ação e resultado. O tribunal e a câmara informam o plano normativo e a
vinculatividade da decisão.

### Etapa 2 — Fatos provados

Descrever o que efetivamente ocorreu segundo a prova produzida: o que as testemunhas
confirmaram, o que ficou sem prova suficiente, o que permaneceu controvertido. Diferenciar
fato confirmado, fato alegado e fato presumido. A NT3 extrai conclusões normativas universais
de fatos que, nos precedentes que invoca, foram resolvidos em plano individual e probatório.

### Etapa 3 — Dispositivo e suas partes

Identificar o que foi decidido em cada capítulo separadamente. Um capítulo não contamina os
outros.

### Etapa 4 — O que o precedente efetivamente decide

Formular a norma concreta extraída: qual conduta, de qual sujeito, em qual contexto,
produziu qual efeito jurídico. Identificar o plano normativo em que opera:

- Responsabilidade civil entre particulares (arts. 186, 187, 927 CC)
- Responsabilidade civil do Estado (art. 37, §6º CF)
- Ato administrativo institucional (Lei 9.784/1999, LINDB)
- Controle concentrado de constitucionalidade (ADI, ADPF, RE com RG)

A NT3 opera no plano do controle constitucional abstrato. A maioria dos precedentes sobre
banheiros opera no plano da responsabilidade civil individual. Esse deslocamento de nível é
o problema lógico central da NT3 e deve ser explicitado sempre que presente.

Identificar também se o precedente fixa tese vinculante (súmula vinculante, acórdão em
repercussão geral, IAC, IRDR) ou resolve apenas o caso concreto. Sem tese vinculante, o
precedente não autoriza generalização normativa.

### Etapa 5 — O que o precedente não decide

Identificar com precisão:

- Questões levantadas mas não respondidas (ex.: RE 845.779 cancelou a RG sem fixar tese)
- Teses rejeitadas por ausência de prova, de nexo ou de legitimidade
- Matérias reservadas a outro foro
- Ambientes não examinados: banheiro escolar, vestiário esportivo, unidade de saúde, presídio
- Salto lógico entre o que o precedente decide e o que a NT3 pretende extrair dele

### Etapa 6 — Relação com o RE 845.779/SC e as ADPFs 1169–1173

Verificar se o precedente menciona o RE 845.779 e em que termos; se opera como se a questão
constitucional de fundo estivesse resolvida; se menciona as ADPFs 1169–1173; se fixa tese
própria sobre uso de banheiros ou apenas resolve o caso concreto. Quando o precedente menciona
o cancelamento do RE 845.779 e ainda assim conclui pela invalidade ampla, identificar isso
como inconsistência interna da fundamentação.

### Etapa 7 — Inferência estratégica para o caso NT3

Responder diretamente:
- Este precedente sustenta, contradiz ou é neutro em relação às conclusões da NT3?
- Ele confirma apenas que discriminação individual é ilícita?
- Ele estabelece que qualquer regulação baseada em sexo é inconstitucional?
- A redução do quantum ou absolvição do ente público indica que gradação e nexo causal
  específico são exigidos, o que vai na direção oposta à proibição universal da NT3?
- Qual argumento específico do caso NT3 este precedente fortalece ou enfraquece?

---

## §5 — Critérios transversais

**Nível normativo**: o salto entre o plano individual (responsabilidade civil) e o plano
institucional (norma constitucional administrativa) é o argumento estrutural mais forte
contra a NT3. Explicitar sempre que o precedente operar nesse salto.

**Universalidade vs. especificidade**: precedentes que resolvem casos individuais não têm
força para proibição universal. Se o precedente reduz o valor indenizatório pela ausência de
tumulto ou impedimento físico, isso demonstra que a gradação da conduta importa.

**Exigência de nexo causal**: quando o ente público é absolvido por ausência de nexo causal
específico, isso corrobora a exigência de motivação individualizada que a autora imputa à
NT3 como ausente.

**Proporcionalidade e alternativas**: se o precedente não examinou soluções de terceira via
(cabines com privacidade integral, vestiários familiares, protocolos por faixa etária),
registrar essa omissão como limitação.

---

## §6 — Proibições

Não reproduzir a ementa como substituto da análise. Não afirmar que o precedente "apoia"
a proteção trans sem qualificar em qual plano normativo e para qual efeito específico. Não
ignorar o cancelamento do RE 845.779 quando o precedente o menciona. Não tratar omissões
do precedente como confirmações implícitas. Não equiparar discriminação individual ilícita
a inconstitucionalidade de política regulatória.

---

## §7 — Formato de saída

Texto corrido, organizado pelos sete títulos da estrutura acima. Sem listas ornamentais.
Cada parágrafo acrescenta fato novo, risco novo, consequência nova, providência nova ou
delimitação nova. A inferência estratégica deve ser direta e operacional.

---

## §8 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] 7 etapas de análise documentadas
- [x] Contexto NT3 explicitado
- [x] git_auto_commit declarado
- [x] Volume ≤ 500 linhas
