---
name: revisao-previa-mod4
description: |
  Revisa conteúdo jurídico antes da formatação pelo mod4. Verifica lógica jurídica (norma→fato→conclusão), completude dos pedidos, honorários, consistência interna e qualidade redacional (R1–R8 padrao-redacional). Produz o bloco "Status: PRONTO PARA mod4" com o JSON status-pre-mod4.v1.json preenchido, ou bloco "BLOQUEADO" com os problemas específicos. INVOQUE quando a usuária disser: "revise antes de enviar para o mod4", "confira a peça", "a peça está pronta?", "está faltando algo?", "verifique os pedidos", "calcule os honorários". O mod4 também invoca automaticamente quando o input não traz o bloco PRONTO.
project: Proj02
nucleo: N1
frente: transversal
camada: C4
categoria: capability
justificativa: Produz output acionável (bloco PRONTO PARA mod4 + JSON status-pre-mod4.v1.json) que libera ou bloqueia o pipeline de formatação — não é reference porque tem pipeline de decisão com resultado concreto.
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
recursos_compartilhados:
  schemas:
    - _compartilhados/SCHEMAS/input/status-pre-mod4.v1.json
  informacoes:
    - _compartilhados/informacoes/padrao-redacional.md
chains_to:
  - mod4
chains_from:
  - replica
  - pericia-acidentaria
  - pericia-previdenciaria
  - artigo-juridico
  - check-protocolo
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11, L13, L19, L20, L21
regras_aplicaveis:
  - R1, R6, R10, R11
---

# revisao-previa-mod4 — Revisão de Conteúdo Jurídico Pré-Formatação

## §0 — Ativação e gates

Ativar quando a peça jurídica estiver redigida e antes de acionar mod4. O mod4 exige
o bloco `Status: PRONTO PARA mod4` — esta skill é quem o produz.

R1 (exportação): perguntar antes de gerar arquivo. O bloco JSON de saída é entregue
em texto no chat; exportação em arquivo exige confirmação.
R6 (adaptação): se a peça está incompleta mas os problemas são menores, sinalizar e
propor correção em vez de bloquear. Decisão de prosseguir é da Raquel.
R10 (discordância útil): apontar problema mesmo que a usuária diga que está pronto.
R11 (economia de ação): se já existe revisão recente da mesma peça no contexto, verificar
antes de reexecutar do zero.

## §1 — Escopo

FAÇO:
- Verificar lógica jurídica: norma → fato → conclusão; cada argumento tem fundamento normativo
- Verificar completude: pedidos mínimos para o tipo de ação presentes (ver ASSETS/pedidos-minimos.md)
- Verificar honorários: calculados, com base e percentual declarados
- Verificar consistência interna: datas, nomes, números de benefício e CIDs coerentes entre si
- Verificar qualidade redacional: R1–R8 de padrao-redacional aplicados
- Verificar campos obrigatórios do schema status-pre-mod4.v1.json (tipo_documento, processo, partes, corpo_texto)
- Classificar problemas: bloqueante (impede formatação) vs. tolerável (pode prosseguir com nota)
- Produzir bloco `Status: PRONTO PARA mod4` com JSON preenchido, ou `Status: BLOQUEADO` com lista de problemas

NÃO FAÇO:
- Redigir a peça → delego para skill C5 pertinente (replica, pericia-*, artigo-juridico)
- Formatar o DOCX → delego para mod4
- Verificar documentos do caso → delego para levanta-fatos ou check-protocolo
- Calcular renda BPC → delego para analise-calculo-renda-bpc
- Analisar laudo pericial → delego para pericia-acidentaria ou pericia-previdenciaria

DELEGO PARA:
- `mod4` — quando output é PRONTO PARA mod4
- skill C5 pertinente — quando problemas bloqueantes exigem reescrita de trecho
- `check-protocolo` — quando documentação do caso ainda está incompleta

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Revisão pré-formatação | "revise antes de enviar", "está pronto para o mod4?", "confira a peça" |
| Completude | "falta algum pedido?", "os honorários estão certos?", "algo a adicionar?" |
| Liberação de pipeline | "pode formatar?", "pode enviar para o mod4?" |
| Invocação automática | mod4 verifica ausência de bloco PRONTO e chama esta skill |

NÃO disparo quando: pedido é de análise técnica de laudo (→ pericia-*), redação de peça nova
(→ skill C5), verificação de documentos do caso (→ levanta-fatos).

## §3 — Dimensões de revisão (D1–D6)

### D1 — Lógica jurídica

Para cada argumento principal da peça:
- A norma invocada existe e está corretamente citada (número de lei + artigo)?
- O fato relatado sustenta a norma invocada?
- A conclusão decorre do fato + norma, ou há salto lógico?
- Há distinção entre fato, hipótese, inferência e conclusão?
- Correlação está sendo apresentada como causalidade? (apontar)

Ver ASSETS/criterios-revisao-por-tipo.md para critérios específicos por tipo de documento.

### D2 — Completude dos pedidos

- Os pedidos mínimos para o tipo de ação estão presentes? (ver ASSETS/pedidos-minimos.md)
- Pedido principal tem fundamento normativo explícito?
- Pedidos subsidiários foram considerados (quando aplicável)?
- Tutela de urgência/evidência: formulada quando cabível?
- Gratuidade de justiça: declarada?
- Honorários advocatícios: incluídos nos pedidos?
- Correção monetária + juros: incluídos e com índice correto?

### D3 — Honorários

Verificar e calcular quando ausentes. Ver ASSETS/tabela-honorarios.md para bases e percentuais.

Regras básicas:
- JEF: art. 55 Lei 9.099/95 — 20% sobre o valor da condenação (fase conhecimento)
- Vara cível/trabalhista: art. 85 §2º CPC — entre 10% e 20%, sobre o valor da condenação
- BPC: honorários sobre o proveito econômico (retroativo + 12 × RMI)
- Artigo jurídico: não há honorários → campo `null` no schema

Campos a preencher no schema: `percentual` + `base_calculo`.

### D4 — Consistência interna

- Nome do autor idêntico em todo o documento (incluindo qualificação)?
- Número do benefício (NB) idêntico em todos os parágrafos?
- CID principal declarado na qualificação coincide com CID do pedido?
- DII declarada nos fatos coincide com DII mencionada nos pedidos?
- CNPJ/CNAE do empregador consistente entre fatos e nexo?
- Espécie do benefício (B31/B91 etc.) consistente em todos os parágrafos?

### D5 — Qualidade redacional (R1–R8 de padrao-redacional)

Verificações rápidas:
- Há frase-pórtico no início? (proibido — R3)
- Algum parágrafo repete em abstrato o que já foi demonstrado em concreto? (R3)
- Há lista ornamental sem função de controle? (R3/R4)
- O núcleo dominante de cada parágrafo é afirmativo? (R6)
- Conectivos explícitos usados para relacionar proposições? (R7)
- Travessão intercalador usado? (proibido — R7)
- Algum pedido sem fundamento normativo explícito? (R2)

### D6 — Campos obrigatórios do schema status-pre-mod4.v1.json

Verificar presença e preenchimento correto de:
- `tipo_documento` (enum — ver lista no schema)
- `processo.numero` (formato CNJ)
- `partes.autor.nome` + `partes.autor.qualificacao`
- `partes.reu.nome`
- `corpo_texto` (≥ 100 caracteres, em Markdown)

## §4 — Classificação de problemas

**Bloqueante** (impede a emissão do bloco PRONTO):
- Pedido principal ausente
- Fundamento normativo ausente no pedido principal
- Nome do autor inconsistente (divergência entre qualificação e corpo)
- `tipo_documento` não identificável
- `corpo_texto` ausente ou < 100 caracteres

**Tolerável** (emite PRONTO com nota de advertência):
- Pedido subsidiário omitido quando cabível
- Honorários ausentes (skill calcula e propõe valor)
- Índice de correção monetária não especificado (skill declara SELIC como padrão)
- Gratuidade de justiça não declarada (skill adiciona automaticamente)
- Adjetivação vazia em parágrafo isolado (sinalizar sem bloquear)

## §5 — Pipeline operacional

```
1. Receber peça (texto Markdown ou conteúdo do chat)
2. Identificar tipo de documento → carregar critérios de ASSETS/criterios-revisao-por-tipo.md
3. Executar D1 (lógica jurídica)
4. Executar D2 (completude de pedidos) com ASSETS/pedidos-minimos.md
5. Executar D3 (honorários) com ASSETS/tabela-honorarios.md
6. Executar D4 (consistência interna)
7. Executar D5 (qualidade redacional)
8. Executar D6 (campos obrigatórios do schema)
9. Classificar todos os problemas encontrados: bloqueante vs. tolerável
10. Se problema bloqueante → emitir bloco BLOQUEADO com lista específica
11. Se nenhum bloqueante → preencher status-pre-mod4.v1.json + emitir bloco PRONTO PARA mod4
12. Aguardar confirmação da Raquel antes de chamar mod4
```

## §6 — Output: bloco PRONTO PARA mod4

Ver template completo em MODELOS/bloco-pronto-mod4.md.

Estrutura mínima obrigatória:

```
---
Status: PRONTO PARA mod4
Revisado por: revisao-previa-mod4 v1.0.0
Data: AAAA-MM-DD
Problemas toleráveis: [lista ou "nenhum"]
---
[JSON status-pre-mod4.v1.json preenchido]
```

## §7 — Output: bloco BLOQUEADO

```
---
Status: BLOQUEADO
Motivo(s):
1. [problema bloqueante 1]
2. [problema bloqueante 2]
Providência: [ação específica para resolver cada ponto]
---
```

## §8 — Contrato de execução

Preconditions:
- Texto da peça disponível (Markdown ou texto colado)
- Tipo de documento identificável (explícito ou inferível)
- Dados mínimos do processo identificáveis (autor, réu)

Postconditions:
- Todos os 6 critérios de revisão verificados e registrados
- Output é PRONTO ou BLOQUEADO (nunca silencioso)
- Se PRONTO: JSON status-pre-mod4.v1.json preenchido e pronto para mod4
- Se BLOQUEADO: cada problema tem providência específica

## §9 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em <= 90 dias
- [x] R1, R6, R10, R11 presentes
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] 6 dimensões de revisão declaradas (§3)
- [x] Classificação bloqueante/tolerável declarada (§4)
- [x] Pipeline operacional declarado (§5)
- [x] Output PRONTO e BLOQUEADO especificados (§6/§7)
- [x] Preconditions e postconditions declaradas (§8)
- [x] depends_on declara schema e reference (A19)
- [x] git_auto_commit: false (L19)
- [x] chains_to: mod4 (skill instalada — L20)
