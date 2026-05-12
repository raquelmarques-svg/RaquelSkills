---
title: pericia-previdenciaria
description: "Perícia médica previdenciária — ciclo completo: quesitação, análise de laudo, vícios processuais, impugnação, art. 151, período de graça, BPC/LOAS, manifestação nos 5 dias, estratégia retórica."
version: 2.0.0
category: capability
núcleo: TBD
frente: TBD
camada: TBD
projeto: TBD
author: Raquel de Almeida Marques
verified_in: 2026-05-11
git_repo: C:\RaquelSkills
git_auto_commit: false
---

# pericia-previdenciaria — Perícia Médica Previdenciária

**Ativar quando a usuária mencionar:** laudo pericial, impugnar laudo, quesitação, perito sem
especialidade, nefropatia grave, art. 151, isenção de carência, DII retrospectiva, art. 129-A,
análise retrospectiva, qualidade de segurado, período de graça, art. 15, seguro-desemprego
prorrogação, nova perícia, vício do laudo, laudo sem fundamentação, BPC negado, biopsicossocial,
CIF, qualificador moderado, SLEDAI, BILAG, rituximabe, nefrite lúpica, LES refratário, silêncios
da contestação, manifestação pós-laudo, 5 dias para manifestar, contestação INSS tese única,
perito ortopedista para LES.

---

## §0 — Princípio organizador

Toda questão pericial tem três dimensões simultâneas: (1) clínica — o que a patologia é e o que
ela faz ao corpo; (2) jurídica — qual norma incide sobre aquele quadro clínico; (3) probatória —
como o laudo (ou a ausência de análise nele) afeta a prova no processo. Trabalhar apenas uma
dimensão implica perder nas outras duas.

## §0-Regras aplicáveis

- **R1 (exportação):** perguntar antes de gerar DOCX ou PDF.
- **R2 (preservação):** nada é deletado; itens removidos vão para `_APAGAR/` com timestamp.
- **R3 (backup):** backup antes de modificar SKILL.md existente.
- **R6 (adaptação):** propor ajuste antes de recusar.
- **R10 (discordância útil):** apontar inconsistências e omissões na estratégia apresentada.
- **R11 (economia de ação):** ponderar soluções caras antes de propô-las.

## §0-Leituras obrigatórias antes de qualquer peça

| Tarefa | Arquivos |
|---|---|
| Quesitação inicial | `templates/quesitacao_padrao.md` + `templates/especialidades_patologias.md` |
| Quesitação BPC-LOAS | `templates/quesitacao_bpc_loas.md` + `templates/qualificadores_cif.md` |
| Análise de laudo | `templates/checklist_laudo.md` + `templates/tipos_vicio_laudo.md` |
| Impugnação | `templates/impugnacao_laudo.md` + `templates/arvore_decisao_pericia.md` |
| Pedido art. 151 | `templates/peticao_art151.md` + `templates/doencas_art151.md` |
| Período de graça | `templates/calculo_periodo_graca.md` |
| Manifestação pós-laudo | `templates/manifestacao_pos_laudo.md` |

---

## §1 — Escopo

**FAÇO:**
- Quesitação estratégica inicial e complementar
- Análise de laudo com protocolo de leitura em 7 etapas
- Impugnação com taxonomia de vícios e pedidos hierarquizados
- Manifestação nos 5 dias pós-laudo complementar (3 cenários)
- Pedido art. 151 (isenção de carência para doenças graves)
- Cálculo de período de graça (art. 15 e §2º)
- Análise retrospectiva obrigatória (art. 129-A, Lei 14.331/2022)
- Mapeamento de silêncios da contestação para réplica
- Estratégia retórica perante o juízo

**NÃO FAÇO:**
- Formatação DOCX final → delego para `mod4`
- Réplica à contestação integral → delego para `replica`
- Especificidades de acidente de trabalho → delego para `pericia-acidentaria`
- Organização de pasta do cliente → delego para `juridir`

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Laudo pericial | "laudo veio", "perito respondeu", "laudo sem anamnese" |
| Quesitação | "formular quesitos", "quesitos complementares" |
| Vício técnico | "perito ortopedista para LES", "laudo sem DII", "campo vazio" |
| Instrumento autônomo | "art. 151", "período de graça", "BPC negado" |
| Janela processual | "5 dias para manifestar", "despacho de complementação" |
| Índice clínico | "SLEDAI", "BILAG", "ISN/RPS", "CIF", "qualificador moderado" |

**NÃO disparo quando:** pedido é réplica integral (→ `replica`), formatação DOCX (→ `mod4`),
organização de pasta (→ `juridir`).

---

## §3 — Fase 1: Antes da Perícia

### Especialidade do perito

O art. 156, §2º CPC exige habilitação técnica compatível com a matéria periciada. A habilitação
é pré-requisito de validade, não preferência da parte. Para patologias multissistêmicas (LES,
esclerodermia, vasculites, Sjögren, AR com comprometimento sistêmico), a especialidade nuclear
é Reumatologia. Para doenças renais (nefropatia lúpica, glomerulonefrite, IRC), Nefrologia.

**Vigilância pós-nomeação:** se o juízo nomear perito incompatível, protocolar antes da perícia.
Após o laudo, a incompetência técnica ancora o Vício Tipo 1 e embasa nulidade (art. 156, §2º CPC
+ STJ, REsp 1.771.815/SP).

### Quesitação — arquitetura estratégica

A quesitação é a estrutura de prova do processo. Cada quesito projeta três cenários: (a) perito
favorável — consolida os pontos favoráveis; (b) perito parcialmente favorável — isola o
reconhecido; (c) perito desfavorável — resposta evasiva já caracteriza vício impugnável.

**Módulos obrigatórios:**
1. Identificação e qualificação da doença (classificação internacional vigente)
2. Análise retrospectiva do histórico clínico (art. 129-A, Lei 8.213/1991)
3. Instrumentos de avaliação funcional validados para a patologia
4. Data de Início da Incapacidade (DII) com fundamentação por período e documento
5. Nexo causal entre complicações e doença-base
6. Qualificação para fins do art. 151 (doença grave, lista taxativa)
7. Impacto do esquema terapêutico na capacidade laboral
8. Prognóstico fundamentado — não apenas DCB sem base

---

## §4 — Fase 2: Análise do Laudo

### Protocolo de leitura (ordem obrigatória)

1. **Qualificação do perito** — especialidade declarada vs. patologia da autora.
2. **Documentos analisados** — omissão é vício potencial (art. 473, §1º CPC).
3. **Exame físico** — inconsistências internas e com documentos dos autos.
4. **Campos obrigatórios** — campos em branco (DII, tratamento, quesitos do juízo).
5. **Respostas aos quesitos** — evasão, "prejudicado" sem pressuposto, afirmação negativa sobre período não examinado.
6. **Art. 151** — campo de doenças graves preenchido corretamente.
7. **DII** — fundamentação retrospectiva ou fixação apenas no evento mais recente.

---

## §5 — Fase 3: Impugnação

### Taxonomia dos vícios

Classificar o vício antes de escrever é obrigatório para calibrar o pedido correto (nova perícia,
esclarecimentos ou nulidade específica).

**Estrutura de cada vício:** (a) transcrição literal do trecho; (b) dado correto nos autos que
o contradiz; (c) fundamento normativo ou científico; (d) consequência jurídica específica.

**Pedidos hierarquizados:**
- **Imediato:** implantação do que o laudo reconheceu sem contestação
- **Principal:** nova perícia por especialista competente, com parâmetros obrigatórios enumerados
- **Subsidiário:** esclarecimentos dentro de prazo, com ameaça de substituição

**Nova perícia total** é cabível quando: (i) vício de incompetência técnica estrutural;
(ii) análise retrospectiva completamente ausente; (iii) três ou mais vícios independentes com
causa-raiz comum. **Esclarecimentos** são cabíveis quando o laudo tem substrato técnico mas
apresenta omissões pontuais.

---

## §6 — Fase 4: Manifestação nos 5 dias pós-laudo complementar

**Cenário A — nefropatia grave retificada para SIM:** reiterar art. 151; a isenção de carência
torna prescindível análise de qualidade de segurado. Juntar parecer técnico ISN/RPS se ausente.

**Cenário B — nefropatia grave mantida como NÃO:** demonstrar com citação literal das diretrizes
ACR/EULAR e do próprio laudo que a marcação é erro técnico verificável sem novo exame. Requerer
desconsideração por contrariar prova documental direta (art. 479 CPC).

**Cenário C — BPC-LOAS questionnaire preenchido:** confrontar cada qualificador com a avaliação
INSS. Convergência M+M+M → requerer BPC independentemente do resultado previdenciário.

---

## §7 — Instrumentos legais autônomos

### Art. 151 — isenção de carência

Independe de qualidade de segurado, DII e período de graça. Apresentar como fundamento
subsidiário autônomo, não como reforço. **Nefropatia grave:** estadiamento ISN/RPS classe III
ou superior com imunossupressor documentado satisfaz qualquer critério clínico razoável. Laudo
que marca negativamente sem analisar ISN/RPS comete erro técnico com consequência jurídica direta.

### Art. 15 — período de graça

**§2º — desemprego involuntário:** registro no MTE é prova documental direta, geralmente
disponível no PROCADM ou CNIS. Verificar sistematicamente antes de assumir inaplicabilidade.

### Art. 129-A — análise retrospectiva obrigatória

Introduzido pela Lei 14.331/2022. Ausência total é vício insanável por esclarecimentos —
somente nova perícia resolve.

---

## §8 — Pragmática processual

**Silêncios da contestação.** Fundamento não enfrentado = admissão implícita. Mapear como tabela
na réplica.

**Laudo incontroverso vs. laudo desfavorável.** Separar pedido de implantação imediata do
incontroverso do pedido de nova perícia para o controvertido — misturar os dois permite que o
juízo indefira tudo por precaução.

**Despacho convertendo em diligência.** Ler como mapa do que importa ao juízo. Responder
exatamente àquelas questões na manifestação pós-laudo.

---

## §9 — Regras invioláveis

1. Nunca citar como "orientação médica" o que é critério jurídico. ISN/RPS é fato clínico;
   isenção de carência é consequência jurídica desse fato.
2. Nunca pedir nova perícia sem justificar por que esclarecimentos são insuficientes.
3. Nunca apresentar vício técnico sem citar literalmente o trecho do laudo e o dado que o contradiz.
4. Sempre separar incontroverso de controvertido.
5. Art. 151 é fundamento autônomo — pedido subsidiário independente, não argumento de reforço.

---

## §10 — Casos-teste

**Positivos:**
1. Laudo de perito ortopedista em caso de LES → identifica Vício Tipo 1, requer reumatologista, cita REsp 1.771.815/SP.
2. Campo art. 151 marcado "NÃO" sem análise ISN/RPS → impugnação por erro técnico verificável com diretrizes ACR/EULAR.
3. Análise retrospectiva ausente → vício insanável, pede nova perícia (não esclarecimentos), invoca art. 129-A.

**Negativos:**
1. Pedido de réplica integral → recusa, delega para `replica`.
2. Pedido de DOCX da impugnação → recusa, delega para `mod4`.

---

## Status

**Instalado:** 2026-05-11
**Versão:** 2.0.0
**Última auditoria:** 2026-05-11
**Próxima auditoria:** 2026-08-09

---

## Notas

- Coordenadas (núcleo, frente, camada, projeto) marcadas como TBD: preencher quando o mapa da
  biblioteca estiver disponível.
- Templates referenciados em §0-Leituras ainda não existem — criação pendente (Sprint backlog).
