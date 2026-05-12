# Casos-teste — check-protocolo

---

## Caso positivo 1 — BPC pronto para protocolo

**Contexto:** Usuária diz "confira o caso da Maria para protocolar o BPC".
Dossiê completo: laudo com CID F70 e F41, família de 4, renda R$1.200 sem BF.

**Comportamento esperado:**
1. Skill carrega `checklist-bpc-loas.md`
2. Verifica Bloco A (docs pessoais) → todos OK
3. Verifica Bloco B (docs clínicos) → laudo OK, biopsicossocial ausente (tolerável)
4. Verifica Bloco C (renda) → R$1.200 ÷ 4 = R$300 < R$405,25 (¼ SM) → OK
5. Verificação D1 (BF): BF de R$600 presente → alerta: verificar se INSS incluiu no cálculo
6. Sem lacunas bloqueantes → resultado: APTO PARA PROTOCOLO
7. Gera folha de conferência (Camada 8 vazia)
8. Recomenda: incluir RE 580.963 na fundamentação

---

## Caso positivo 2 — Incapacidade com módulo Juízo Digital

**Contexto:** Ação B91 no JEF eletrônico (PJe). Usuária pede "checklist antes de protocolar".

**Comportamento esperado:**
1. Skill carrega `checklist-incapacidade.md` + `juizo-100-digital.md` (processo eletrônico)
2. Verifica Bloco A (qualidade de segurado): CNIS confirma contribuições até 3 meses antes da DII → OK
3. Verifica Bloco C (nexo): CNAE 2910701 x CID M54.5 → NTEP verdadeiro; CAT presente → OK
4. Verifica Bloco D (docs laborais): PPP ausente → lacuna tolerável (requerer por ofício)
5. Módulo D2 (Juízo Digital): arquivo de RM com 8 MB → FALTANTE (limite PJe 2 MB)
6. Resultado: BLOQUEADO — 1 item bloqueante: arquivo RM acima do limite PJe
7. Providência: comprimir RM com iLovePDF antes de protocolar

---

## Caso positivo 3 — Pós-protocolo executado

**Contexto:** Usuária diz "protocolei o caso do João agora há pouco. O que faço agora?"

**Comportamento esperado:**
1. Skill carrega `rotina-pos-protocolo.md`
2. Percorre Etapas 1–7 confirmando com a usuária
3. Lembra: configurar alerta de 15 dias úteis (JEF) para contestação do INSS
4. Lembra: verificar distribuição em 24h
5. Fornece modelo de mensagem WhatsApp para enviar ao cliente

---

## Caso negativo 1 — Pedido de checklist sem tipo de ação

**Contexto:** Usuária diz "confira o caso da Ana".

**Comportamento esperado:**
1. Skill pergunta: "Qual o tipo de ação? BPC-LOAS, benefício por incapacidade (B31/B91), previdenciária comum, cível ou família?"
2. Não inventa o tipo — sem ele, não é possível carregar o checklist correto
3. Ao receber a resposta, procede normalmente

---

## Caso negativo 2 — Cumprimento de sentença confundido com pré-protocolo

**Contexto:** Usuária diz "preciso verificar o que falta para cumprir a sentença do José".

**Comportamento esperado:**
1. Skill identifica que o pedido é de cumprimento de sentença (fase executiva)
2. NÃO aplica checklist de petição inicial
3. Informa: "Cumprimento de sentença tem rotina própria — skill check-cumprimento-sentenca"
4. Se a skill ainda não estiver instalada: "Esta verificação está em desenvolvimento (Phase B). Por ora, posso listar os passos manualmente."
