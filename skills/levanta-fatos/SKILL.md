---
name: levanta-fatos
description: |
  Extrai fatos estruturados de documentos juridicos brasileiros (CTPS, CNIS, CAT, PPP, laudos, exames, processo administrativo INSS) e produz output conforme fatos-estruturados.v1.json. INVOQUE quando a usuaria disser: "leia os documentos", "extraia os dados", "levante os fatos", "o que tem neste CNIS", "leia a CTPS", "extraia do processo administrativo", "o que o laudo diz sobre NB e datas". NAO use para analisar laudos periciais (pericia-acidentaria), redigir pecas (skills C5), montar dossie narrativo (dossie-caso) nem calcular renda BPC (analise-calculo-renda-bpc).
project: Proj02
nucleo: N1
frente: transversal
camada: C1
categoria: capability
justificativa: Extrai dados brutos de documentos e os entrega como fatos-estruturados.v1.json para dossie-caso e skills C5; nao e reference porque produz output acionavel
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
recursos_compartilhados:
  schemas:
    - _compartilhados/SCHEMAS/output/fatos-estruturados.v1.json
chains_to:
  - dossie-caso
  - replica
  - pericia-acidentaria
  - pericia-previdenciaria
  - analise-calculo-renda-bpc  # plugin externo — não está em skills/
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11, L13
regras_aplicaveis:
  - R1, R2, R6, R10, R11
---

# levanta-fatos — Extracao de Fatos Estruturados de Documentos

## §0 — Ativacao e gates

Ativar quando a usuaria apresentar documentos para leitura e extracao de dados: "leia os
documentos", "extraia os dados do CNIS", "o que a CTPS mostra", "levante os fatos do processo
administrativo". Tambem ativar quando skill C5 solicitar base factual antes de redigir peca.

## §0 — Regras universais

R1 (exportacao): perguntar antes de gerar arquivo de output estruturado.
R2 nao se aplica (skill nao cria arquivos existentes).
R6 (adaptacao): se documento esta ilegivel ou truncado, sinalizar e extrair o que for possivel.
R10 (discordancia util): apontar inconsistencia entre documentos antes de registrar como fato.
R11 (economia de acao): se ja existe dossie com dados extraidos, verificar antes de reextrair.

## §1 — Escopo

FACO:
- Ler documentos fornecidos pela usuaria (PDF, imagem, texto colado) e extrair campos estruturados
- Identificar e registrar: processo, partes, CNAE, CIDs, beneficios (NB/especie/DID/DII/DIB/DCB/RMI)
- Extrair historico de vinculos empregaticos (funcao, CNAE, periodo) da CTPS e do CNIS
- Identificar documentos presentes vs. ausentes
- Verificar se o par CNAE x CID consta da Lista A do Decreto 3.048 (Anexo II) — campo ntep_aplicavel
- Sinalizar inconsistencias entre documentos (ex.: DID na CAT diverge do laudo)
- Produzir output conforme fatos-estruturados.v1.json

NAO FACO:
- Analisar laudo pericial tecnicamente -> delego para pericia-acidentaria ou pericia-previdenciaria
- Interpretar fatos estrategicamente para a tese -> delego para dossie-caso
- Redigir peca processual -> delego para skill C5 pertinente
- Calcular renda per capita BPC -> delego para analise-calculo-renda-bpc
- Organizar pasta de documentos -> delego para juridir

DELEGO PARA:
- `dossie-caso` — quando dados extraidos devem alimentar dossie narrativo completo
- `pericia-acidentaria` ou `pericia-previdenciaria` — quando laudo esta entre os documentos
- `analise-calculo-renda-bpc` — quando processo e BPC e ha dados de renda a calcular

---

## §2 — Trigger semantico

| Nucleo | Exemplos |
|---|---|
| Leitura de documento | "leia este CNIS", "leia a CTPS", "leia o processo administrativo" |
| Extracao de dados | "extraia os dados", "levante os fatos", "quais NBs aparecem" |
| Verificacao de documento | "o que tem neste laudo", "quais CIDs estao no processo" |
| Preparacao para peca | "antes de escrever, levante os fatos do caso" |

NAO disparo quando: pedido e analise tecnica de laudo (-> pericia-*), calculo de renda BPC
(-> analise-calculo-renda-bpc), ou redacao de peca direta sem necessidade de extracao previa.

---

## §3 — Documentos suportados e o que extrair de cada um

### CTPS (Carteira de Trabalho e Previdencia Social)
Extrair: nome completo, CPF, data de nascimento, cada vinculo empregatico com empregador +
CNPJ + funcao + data admissao + data saida (null se atual) + salario contratual.
Sinalizar: periodos em branco, rasuras, divergencia de nome entre registros.

### CNIS (Cadastro Nacional de Informacoes Sociais)
Extrair: NIT/PIS, lista de vinculos com CNPJ + CNAE + competencias de contribuicao + remuneracao.
Lista de beneficios com NB + especie + DII + DIB + DCB + RMI. Qualidade de segurado na DID.
Sinalizar: periodos sem contribuicao, vinculo sem CNAE informado, especie de beneficio diferente
do esperado.

### CAT (Comunicacao de Acidente de Trabalho)
Extrair: data do acidente ou do diagnostico, CID informado, descricao do acidente/doenca,
empregador (nome + CNPJ + CNAE), parte do corpo atingida, situacao geradora, medico que assinou.
Sinalizar: CAT emitida pelo proprio empregador (forte para o nexo), CAT emitida pelo sindicato
ou pelo proprio segurado (valor probatorio diferente), ausencia de CAT.

### PPP (Perfil Profissiografico Previdenciario)
Extrair: CNAE do empregador, descricao de atividades e agentes nocivos por periodo, uso de EPI,
funcao habitual, conclusao tecnica do SESMT sobre exposicao.
Sinalizar: ausencia de descricao de agentes nocivos, EPI com eficacia declarada (pode afastar
nexo por insalubridade mas nao necessariamente por acidente).

### Laudo / relatório médico particular
Extrair: CID principal e secundarios, data do diagnostico, nome do medico e CRM, achados
objetivos (descricao de exames de imagem, testes clinicos), conclusao sobre incapacidade,
limitacoes funcionais descritas, tratamento prescrito.
Sinalizar: laudo sem data, laudo sem descricao de achados objetivos (apenas conclusao), CID
divergente do beneficio concedido.
ATENCAO: nao analisar se o laudo e Tipo A/B/C — isso e tarefa de pericia-acidentaria.

### Exames de imagem (RM, TC, RX, USG)
Extrair: tipo de exame, data, regiao examinada, achados descritivos (ex.: protrusao discal L4-L5
com compressao de raiz S1), CID sugerido pelo laudante se houver.
Sinalizar: exame sem data, exame de data anterior ao vinculo (doenca previa — risco para nexo).

### Processo administrativo INSS (carta-beneficio, despacho, extrato)
Extrair: NB, especie concedida, DID, DII, DIB, DCB, RMI, fundamento do indeferimento (se houver),
CID registrado pelo INSS, data da decisao administrativa.
Sinalizar: especie concedida divergente da esperada (B31 em vez de B91), DID registrada apos
a data que o cliente relata (pode prejudicar retroativo), beneficio cessado sem motivacao.

### Contestacao do INSS
Nao e um documento de fatos — e peca processual. Nao extrair como fatos; encaminhar para
`replica` para leitura e classificacao por Tipo I/II/III.

---

## §4 — Verificacao NTEP (obrigatoria quando CNAE e CID estao presentes)

Quando o documento fornece CNAE do empregador e CID da doenca, verificar se o par consta
da Lista A do Decreto 3.048, Anexo II (Relacao de Agentes Patogenicos).

Resultado possivel:
- `ntep_aplicavel: true` — par consta da Lista A; presuncao de nexo opera (art. 21-A Lei 8.213/91)
- `ntep_aplicavel: false` — par nao consta; nexo deve ser provado individualmente
- `ntep_aplicavel: null` — CNAE ou CID nao disponivel nos documentos; nao e possivel verificar

Registrar no campo `ntep_aplicavel` do schema fatos-estruturados.v1.json.
Ver ASSETS/ntep-lista-a-consulta.md para os principais pares da pratica do escritorio.

---

## §5 — Tratamento de inconsistencias entre documentos

Quando dois documentos apresentam dados conflitantes sobre o mesmo campo, registrar ambos
e sinalizar a inconsistencia em `observacoes`. Nao resolver o conflito por conta propria —
isso e tarefa de dossie-caso ou da usuaria.

Exemplos de inconsistencia frequente:
- DID na CAT (2023-08) diverge do DID no laudo medico (2021-03): registrar ambas, sinalizar
- CNAE na CTPS (2910701) diverge do CNAE no PPP (2920600): registrar ambos
- Nome do cliente grafado diferente em CTPS e CNIS: registrar, nao normalizar sem instrucao
- Beneficio B31 no CNIS mas CAT registrada: sinalizar vicio de especie potencial

---

## §6 — Pipeline operacional

```
1. Receber documentos da usuaria (PDF, imagem, texto)
2. Verificar: ha dossie existente para este cliente? (L16 — evitar duplicacao)
3. Para cada documento: identificar o tipo (§3) e extrair campos correspondentes
4. Unificar dados extraidos: resolver conflitos ou sinalizar inconsistencias (§5)
5. Verificar par CNAE x CID na Lista A (§4)
6. Identificar documentos ausentes (lacunas_documentais no schema)
7. Produzir output fatos-estruturados.v1.json
8. Recomendar skill downstream: se laudo presente -> pericia-*; se base factual para peca
   -> dossie-caso; se BPC -> analise-calculo-renda-bpc
9. R1: perguntar antes de exportar em arquivo estruturado
```

---

## §7 — Contrato de execucao

Preconditions:
- Pelo menos um documento fornecido
- Nome ou NIT do cliente identificavel no documento

Postconditions:
- Output conforme `_compartilhados/SCHEMAS/output/fatos-estruturados.v1.json` v1.0.0
- Campo `documentos_presentes` preenchido com enum correto
- Campo `lacunas_documentais` listando o que deveria estar mas nao foi fornecido
- Inconsistencias entre documentos registradas em `observacoes`
- `ntep_aplicavel` preenchido quando CNAE e CID estao disponiveis

---

## §8 — Auto-verificacao

Ultima verificacao de conformidade: 2026-05-12
Proxima verificacao: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em <= 90 dias
- [x] R1, R6, R10, R11 aplicaveis presentes
- [x] §1 com FACO/NAO FACO/DELEGO PARA explicito
- [x] Tabela de documentos suportados com campos a extrair (§3)
- [x] Verificacao NTEP documentada (§4)
- [x] Tratamento de inconsistencias (§5)
- [x] Preconditions e postconditions declaradas (§7)
- [x] Output conforme schema fatos-estruturados.v1.json
- [x] git_auto_commit: false (L19)
- [x] depends_on declara schema de output (L20 — A19)
- [x] Tamanho dentro do limite
