---
name: check-protocolo
description: |
  Verifica se todos os documentos, dados e condições processuais estão satisfeitos antes do protocolo de qualquer peça. Recebe o tipo de ação (BPC/LOAS, incapacidade, previdenciária, cível, família) e percorre o checklist correspondente, gerando a folha de conferência com status OK/FALTANTE/INCOMPLETO por item. INVOQUE quando a usuária disser: "o que falta para protocolar", "pode protocolar?", "confira antes de protocolar", "checklist pré-protocolo", "está pronto para enviar?". Também ativar quando mod4 for acionado sem que os documentos tenham sido conferidos.
project: Proj02
nucleo: N1
frente: transversal
camada: C4
categoria: capability
justificativa: Produz output acionável (folha de conferência com itens OK/FALTANTE/INCOMPLETO) que bloqueia ou libera o protocolo — não é reference porque tem pipeline de decisão e resultado concreto.
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
recursos_compartilhados:
  schemas:
    - _compartilhados/SCHEMAS/output/fatos-estruturados.v1.json
    - _compartilhados/SCHEMAS/output/dossie-caso.v1.json
chains_to:
  - mod4
chains_from:
  - levanta-fatos
  - dossie-caso
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11, L13, L19, L20
regras_aplicaveis:
  - R1, R6, R10, R11
---

# check-protocolo — Verificação Pré-Protocolo

## §0 — Ativação e gates

Ativar quando a usuária apresentar caso para protocolo e pedir conferência, ou quando mod4 for
invocado sem verificação prévia dos documentos. Também ativar quando dossie-caso ou levanta-fatos
finalizarem e a próxima ação for protocolar.

R1 (exportação): perguntar antes de gerar folha em arquivo.
R6 (adaptação): se tipo de ação não se encaixa nos 5 tipos cobertos, adaptar ao mais próximo
e sinalizar a diferença.
R10 (discordância útil): apontar documento ausente ou inconsistência mesmo que a usuária
diga que está tudo pronto.
R11 (economia de ação): se dossie já está montado e completo, usar os dados sem reextrair.

## §1 — Escopo

FAÇO:
- Percorrer checklist do tipo de ação informado (BPC, incapacidade, previdenciária, cível, família)
- Verificar, item por item, o que está presente, o que está faltando e o que está incompleto
- Verificar módulo Juízo 100% Digital (D1–D10) quando processo for eletrônico
- Gerar folha de conferência com status por item
- Sinalizar lacunas bloqueantes (impedem o protocolo) versus lacunas toleráveis (podem ser supridas depois)
- Executar rotina pós-protocolo quando o protocolo for confirmado

NÃO FAÇO:
- Redigir a peça processual → delego para skill C5 pertinente
- Extrair fatos dos documentos → delego para levanta-fatos
- Montar dossiê narrativo → delego para dossie-caso
- Organizar pasta de arquivos → delego para juridir
- Verificar cumprimento de sentença → delego para check-cumprimento-sentenca

DELEGO PARA:
- `mod4` — quando todos os itens obrigatórios estão OK
- `levanta-fatos` — quando documentos estão presentes mas dados não foram extraídos
- `dossie-caso` — quando a base factual está incompleta para montar a peça

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Conferência pré-protocolo | "confira antes de protocolar", "pode protocolar?", "está pronto?" |
| Checklist | "checklist do caso", "o que falta", "lista de documentos" |
| Verificação de aptidão | "o processo está completo?", "posso enviar?" |
| Pós-protocolo | "o que fazer depois de protocolar", "protocolei, e agora?" |

NÃO disparo quando: pedido é de análise de laudo (→ pericia-*), redação de peça sem
conferência prévia solicitada (→ skill C5 direto), organização de pasta (→ juridir).

## §3 — Tipos de ação cobertos

1. `bpc-loas` — BPC/LOAS por deficiência ou doença grave
2. `incapacidade` — Benefícios B31/B91/B92/B94 (auxílio e aposentadoria por incapacidade)
3. `previdenciaria` — Aposentadorias, pensão por morte, salário-maternidade
4. `civel` — Danos morais/materiais por doença ou acidente de trabalho (vara cível/trabalhista)
5. `familia` — Alimentos, guarda, divórcio, inventário

Ver ASSETS/ para o checklist completo de cada tipo.

## §4 — Módulo Juízo 100% Digital (obrigatório quando processo eletrônico)

Ver ASSETS/juizo-100-digital.md para os itens D1–D10.
Ativar automaticamente quando: sistema for PJe, e-Proc, Projudi ou similar.
Itens D1–D10 são adicionados à folha de conferência como seção extra.

## §5 — Classificação de lacunas

Lacuna bloqueante: impede o protocolo. Exemplos: procuração ausente, laudo médico ausente
(incapacidade), CNIS ausente (qualidade de segurado não verificável), CID não consta em
nenhum documento.

Lacuna tolerável: pode ser suprida por ofício, diligência ou substituição posterior.
Exemplos: PPP ausente (pode ser requerido por ofício), exame de imagem antigo (pode ser
atualizado), comprovante de residência vencido (pode ser substituído em audiência).

## §6 — Pipeline operacional

```
1. Identificar tipo de ação (bpc-loas | incapacidade | previdenciaria | civel | familia)
2. Verificar se dossie-caso.v1.json ou fatos-estruturados.v1.json estão disponíveis
3. Carregar checklist correspondente de ASSETS/
4. Para cada item: marcar OK (presente e suficiente), FALTANTE (ausente) ou INCOMPLETO
5. Se processo eletrônico: adicionar módulo D1–D10 de ASSETS/juizo-100-digital.md
6. Classificar lacunas: bloqueante vs. tolerável
7. Se lacuna bloqueante presente: bloquear protocolo, listar providências
8. Se nenhuma lacuna bloqueante: liberar protocolo, gerar folha de conferência
9. Após confirmação de protocolo: executar rotina de ASSETS/rotina-pos-protocolo.md
10. R1: perguntar antes de exportar folha em arquivo
```

## §7 — Folha de conferência (output)

Ver template completo em MODELOS/folha-conferencia.md.
Estrutura: cabeçalho (caso, tipo de ação, data), seções por camada (0–9),
módulo Juízo Digital (quando aplicável), linha de resultado (APTO / BLOQUEADO).

## §8 — Contrato de execução

Preconditions:
- Tipo de ação identificado (explícito ou inferível do dossiê)
- Pelo menos um documento ou relato de fatos disponível

Postconditions:
- Todos os itens do checklist do tipo classificados (OK/FALTANTE/INCOMPLETO)
- Lacunas bloqueantes listadas separadamente
- Resultado: APTO PARA PROTOCOLO ou BLOQUEADO (motivo)
- Rotina pós-protocolo disponível quando protocolo for confirmado

## §9 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em <= 90 dias
- [x] R1, R6, R10, R11 aplicáveis presentes
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] Tipos de ação cobertos declarados (§3)
- [x] Classificação de lacunas declarada (§5)
- [x] Pipeline operacional declarado (§6)
- [x] Preconditions e postconditions declaradas (§8)
- [x] git_auto_commit: false (L19)
- [x] depends_on declara schemas de input (A19)
