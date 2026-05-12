# Módulo Juízo 100% Digital — D1–D10

Fundamento: Resolução CNJ 354/2020 (Juízo 100% Digital); PJe (Res. CNJ 185/2013);
e-Proc TRF; Projudi (TJPR e outros); MNI (Modelo Nacional de Interoperabilidade).
Data de referência: 2026-05-12.

Ativar quando: processo tramitar em PJe, e-Proc, Projudi, SEEU ou qualquer sistema eletrônico.

---

## D1 — Sistema identificado e acesso confirmado

| Verificação | OK/Alerta |
|---|---|
| Sistema do tribunal identificado (PJe / e-Proc / Projudi / outro) | |
| Advogado tem login ativo no sistema | |
| Certificado digital ICP-Brasil válido (não vencido) | |
| Token/driver do certificado instalado e funcionando | |

**Ação corretiva:** Certificado vencido → renovar na AC antes de protocolar. Sem certificado: petição não pode ser assinada digitalmente e não será aceita.

---

## D2 — Formato dos documentos

| Verificação | OK/Alerta |
|---|---|
| Todas as peças em formato PDF (preferencialmente PDF/A — ISO 19005) | |
| Documentos escaneados com OCR (texto pesquisável) | |
| Resolução mínima 150 DPI, máximo 300 DPI para escaneamentos | |
| Tamanho total do upload dentro do limite do sistema (PJe: 2 MB por arquivo; e-Proc: 5 MB) | |
| Arquivos nomeados de forma descritiva (ex.: "01-Petição_Inicial.pdf", "02-Procuração.pdf") | |

**Ação corretiva:** Arquivo maior que o limite → dividir com PDF Splitter ou comprimir com iLovePDF.

---

## D3 — Assinatura digital

| Verificação | OK/Alerta |
|---|---|
| Assinatura digital ICP-Brasil aplicada à petição principal | |
| Procuração assinada digitalmente ou com firma reconhecida em cartório | |
| Documentos do cliente: cópias simples são aceitas no Juízo Digital (Res. CNJ 354/2020 art. 5º) | |
| Autenticação de documentos: dispensada para cópias no processo eletrônico (art. 425 CPC) | |

---

## D4 — Procuração e poderes especiais

| Verificação | OK/Alerta |
|---|---|
| Procuração outorgada ao(s) advogado(s) do caso | |
| Poderes especiais declarados (receber citação, transigir, substabelecer — conforme necessidade) | |
| Para JEF: procuração com poderes para receber intimações eletrônicas | |
| Substabelecimento (se houver): assinado e juntado | |

---

## D5 — Distribuição e cadastro das partes

| Verificação | OK/Alerta |
|---|---|
| CPF/CNPJ do(s) réu(s) disponível para cadastro no sistema | |
| Para ações contra o INSS: CNPJ 29.979.036/0001-40; endereço eletrônico do INSS no sistema já cadastrado? | |
| Para ações contra União: CNPJ 00.394.460/0057-28 (AGU responsável) | |
| Endereço completo do réu para intimação (quando não cadastrado no sistema) | |

---

## D6 — Audiência virtual (quando designada)

| Verificação | OK/Alerta |
|---|---|
| Link da audiência virtual recebido e testado (Zoom / Meet / sistema próprio do tribunal) | |
| Cliente informado com link, data, horário e instruções de acesso | |
| Câmera e microfone testados pelo advogado | |
| Documento de identidade do cliente preparado para exibição na tela | |
| Testemunhas informadas do link e horário | |

---

## D7 — Intimações e prazos eletrônicos

| Verificação | OK/Alerta |
|---|---|
| Intimação eletrônica habilitada no portal do advogado no sistema | |
| Alerta de prazo configurado no sistema do escritório (ou na agenda) | |
| Prazo conta a partir da consulta (quando sistema exige consulta) ou da disponibilização? Verificar regra do tribunal | |
| Para PJe: intimação disponibilizada → 3 dias úteis para consultar; após: conta o prazo | |

---

## D8 — Segredo de justiça e restrição de acesso

| Verificação | OK/Alerta |
|---|---|
| Há pedido de segredo de justiça (violência doméstica, família, menores)? | |
| Se sim: marcar flag correspondente no sistema no ato da distribuição | |
| Verificar se o sistema do tribunal implementa o segredo automaticamente para o tipo de ação | |

---

## D9 — Tutela de urgência / liminar

| Verificação | OK/Alerta |
|---|---|
| Pedido de tutela antecipada ou cautelar formulado na petição? | |
| Comprovação de urgência juntada (relatório médico atual, extrato de benefício cessado, etc.) | |
| Para JEF: liminar pode ser concedida por juiz plantonista — verificar se o sistema permite peticionamento fora do horário | |

---

## D10 — Verificação final antes do envio

| Verificação | OK/Alerta |
|---|---|
| Número de folhas conferido com o sistema (algumas varas limitam peças) | |
| Valor da causa calculado e declarado corretamente | |
| Custas iniciais recolhidas (se não for beneficiário da gratuidade) — DARE ou GRU anexada | |
| Para JEF: gratuidade automática (art. 54-A Lei 9.099/95) — dispensar guia | |
| Petição relida antes de assinar — sem erros de nome, número de benefício ou CPF | |
| Envio confirmado: número do protocolo registrado imediatamente após envio | |
