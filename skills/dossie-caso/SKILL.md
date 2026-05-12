---
name: dossie-caso
description: |
  Produz o dossie estruturado de um caso juridico. Organiza fatos em 5 dimensoes (naturais, humanos, clinicos, previdenciarios, juridicos), qualifica completamente as partes (telefone, email, endereco com ponto de referencia), constroi a linha do tempo unificada, distingue questoes de fato de questoes de direito, e interpreta cada prova quanto ao conteudo objetivo e ao valor estrategico. Output conforme dossie-caso.v1.json. INVOQUE quando a usuaria disser: "monte o dossie", "organize o caso", "crie o dossie de [cliente]", "qual a situacao do caso", "o que temos sobre este caso". NAO use para redigir pecas processuais (replica, impugnacao), analisar laudos (pericia-acidentaria), nem formatar DOCX (mod4).
project: Proj02
nucleo: N1
frente: transversal
camada: C1
categoria: capability
justificativa: Produz artefato estruturado (dossie-caso.v1.json) que alimenta todas as skills C5; nao e reference porque gera output externo acionavel por outras skills
version: 1.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: false
depends_on: []
chains_to:
  - levanta-fatos
  - replica
  - pericia-acidentaria
  - pericia-previdenciaria
  - artigo-juridico
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11, L13
regras_aplicaveis:
  - R1, R2, R3, R6, R10, R11
---

# dossie-caso — Dossie Estruturado de Caso Juridico

## §0 — Ativacao e gates

Ativar quando a usuaria pedir: "monte o dossie", "organize o caso", "crie o dossie de [cliente]",
"qual a situacao do caso", "o que temos sobre este caso", ou quando qualquer skill C5 precisar
de base factual antes de redigir peca.

## §0 — Regras universais

R1 (exportacao): perguntar antes de gerar DOCX, PDF ou exportacao estruturada.
R2 (preservacao): nunca deletar; itens removidos vao para `_APAGAR/`.
R3 (backup): backup antes de modificar dossie existente.
R6 (adaptacao): propor ajuste antes de recusar campo.
R10 (discordancia util): apontar contradicao interna nos fatos antes de registra-los.
R11 (economia de acao): se o caso e simples, nao inflar com secoes vazias.

## §1 — Escopo

FAÇO:
- Qualificar completamente as partes (nome, CPF, data nascimento, telefone, email,
  endereco com ponto de referencia, estado civil, profissao)
- Organizar fatos nas 5 dimensoes (naturais, humanos, clinicos, previdenciarios, juridicos)
- Distinguir fato confirmado, fato alegado, fato controvertido e fato presumido
- Construir linha do tempo unificada com relevancia e dimensao de cada evento
- Mapear questoes de fato (o que aconteceu?) separadas de questoes de direito (qual norma?)
- Inventariar provas com conteudo objetivo + interpretacao estrategica + forca probatoria
- Identificar lacunas probatorias com impacto (bloqueante / relevante / acessorio)
- Identificar riscos com probabilidade e mitigacao
- Recomendar skill downstream para proxima acao

NÃO FAÇO:
- Redacao de peca processual (replica, impugnacao, peticao inicial) -> delego para skill C5
- Analise tecnica de laudo pericial -> delego para pericia-acidentaria ou pericia-previdenciaria
- Pesquisa juridica e analise de precedentes -> delego para analise-precedente
- Formatacao DOCX -> delego para mod4
- Organizacao de pasta de cliente -> delego para juridir

DELEGO PARA:
- `levanta-fatos` — coleta de dados brutos a partir de documentos do cliente
- `pericia-acidentaria` — quando fatos clinicos indicam laudo desfavoravel acidentario
- `pericia-previdenciaria` — quando fatos previdenciarios indicam laudo previdenciario
- `replica` — quando fatos juridicos mostram contestacao protocolada
- `analise-precedente` — quando questao de direito invoca jurisprudencia a auditar
- `mod4` — quando dossie deve ser exportado como DOCX corporativo

---

## §2 — Trigger semantico

| Nucleo | Exemplos |
|---|---|
| Criar dossie | "monte o dossie", "crie o dossie de [nome]", "organize o caso" |
| Consultar situacao | "qual a situacao do caso", "o que temos sobre este caso" |
| Atualizar dossie | "atualize o dossie", "adicione ao dossie que..." |
| Base para peca | "antes de escrever a replica, levante os fatos" |

NAO disparo quando: pedido e diretamente uma peca processual sem necessidade de sintese
factual previa, ou quando o caso e tao simples que a peca pode ser redigida diretamente.

---

## §3 — Coleta de dados (perguntas obrigatorias)

Antes de montar qualquer dossie, confirmar com a usuaria:

1. Nome completo do cliente e CPF (para identificacao unica)
2. Numero do processo ou, se pre-distribuicao, tipo de acao pretendida
3. Fase atual (instrucao, pos-laudo, sentenca, etc.)
4. Quais documentos a usuaria tem em maos ou no sistema
5. Ha dossie anterior para este cliente? (evita duplicacao — L16)

Se a usuaria fornece documentos fisicos ou PDFs, delegar extracao de dados para `levanta-fatos`
antes de preencher o dossie. Se a usuaria fornece os dados diretamente em conversa,
preencher a partir do relato, marcando campos como `fonte: "Relato da usuaria"`.

---

## §4 — As 5 dimensoes de fatos

### 4.1 — Fatos naturais
Dados biograficos e de contexto permanente: local de nascimento, origem familiar, migracao,
composicao familiar (filhos, dependentes), situacao socioeconomica atual, nivel de instrucao.
Estes fatos mudam pouco e servem para humanizar a narrativa e contextualizar as demais dimensoes.

### 4.2 — Fatos humanos
Condicoes concretas de trabalho e de vida: descricao das tarefas diarias, postura, esforco fisico,
repeticao de movimentos, jornada, turno, historico de vinculos empregaticos com funcao e periodo.
Tambem: impacto da doenca ou acidente na vida cotidiana (o que o cliente nao consegue mais fazer),
rede de suporte familiar, dependencia economica. Estes fatos sao o nucleo da anamnese ocupacional
e da analise de concausa.

### 4.3 — Fatos clinicos
Diagnosticos com CID, data de diagnostico, medico responsavel, tratamentos em curso, internacoes,
cirurgias, medicamentos, exames de imagem e seus achados. Limitacoes funcionais descricao precisa
(nao consegue permanecer em pe mais de X minutos; nao levanta peso acima de Y kg). Estes fatos
fundamentam o nexo clinico e a incapacidade.

### 4.4 — Fatos previdenciarios
Historico de beneficios (NB, especie, DIB, DCB, RMI), CNIS com periodos de contribuicao, qualidade
de segurado, carencia cumprida, periodo de graca. DID, DII e DIB de cada beneficio. Especie
concedida vs. especie correta. Estes fatos sao a base para o argumento de vicio de especie e para
calculo de diferencial de RMI.

### 4.5 — Fatos juridicos
Historico processual cronologico: distribuicao, citacao, contestacao (com ou sem impugnacao do
NTEP), designacao de pericia, laudo, prazos vigentes, sentencas, recursos, execucao. Incluir prazo
remanescente em dias quando existir. Estes fatos determinam a proxima acao processual e a urgencia.

---

## §5 — Qualificacao completa das partes

A qualificacao do autor deve ser suficiente para tres usos distintos: (a) cabecalho de peticao,
(b) contato direto em caso de urgencia processual, (c) localizacao presencial se necessario.

Campos obrigatorios para o autor:
- Nome completo (sem abreviacoes)
- CPF no formato 000.000.000-00
- Data de nascimento
- Estado civil
- Profissao (conforme CTPS, nao titulo academico)
- Telefone principal com DDD
- Email (se disponivel)
- Endereco completo: logradouro + numero + complemento + bairro + cidade + UF + CEP
- Ponto de referencia: descricao geografica para localizacao em visita ou entrega de documentos

Se o cliente nao tiver email ou nao souber o CEP, registrar `null` e marcar como lacuna acessoria.

Para o reu (INSS ou empregador), registrar nome e CNPJ. Para terceiros relevantes (empregador,
assistente tecnico, testemunhas), registrar nome, papel e contato disponivel.

---

## §6 — Questao de fato vs. questao de direito

Esta distincao e o eixo central do dossie juridico e deve ser explicita para cada controversia.

**Questao de fato** responde: o que aconteceu? O que e verdadeiro no plano dos acontecimentos?
Exemplos: o trabalho causou a doenca? O beneficio foi concedido com especie errada? O INSS
notificou o cliente? O empregador emitiu a CAT?
Para cada questao de fato: registrar posicao do autor, posicao do reu, e qual prova resolve.

**Questao de direito** responde: qual norma se aplica a esses fatos e qual e a consequencia
juridica? Exemplos: o NTEP presume o nexo neste CNAE x CID? O art. 21-A exige que o laudo
seja Tipo A para afastar a presuncao? A carencia do BPC e per capita ou por renda bruta?
Para cada questao de direito: formular a tese no formato norma + fato + conclusao, com a
jurisprudencia de suporte e a objecao prevista com resposta.

Erro frequente a evitar: tratar questao de direito como questao de fato ("o nexo nao foi
provado" quando o nexo e presumido por lei) e o inverso ("a lei exige X" quando o que esta
em disputa e o fato que aciona a norma).

---

## §7 — Provas e interpretacao

Para cada documento, registrar dois campos separados:

**Conteudo relevante** — o que o documento diz objetivamente, sem valoracao estrategica.
Exemplo: "CAT registra CID M51.1, data do acidente 2023-08-15, empregador Metalurgica ABC Ltda."

**Interpretacao** — o que o documento significa para as teses do autor.
Exemplo: "A CAT emitida pelo proprio empregador inviabiliza a tese de doenca exclusivamente
pessoal, pois o reu reputou o evento como acidentario no ato de registro."

**Forca probatoria**:
- `forte`: sozinha, esta prova sustenta a tese sem necessidade de corroboracao
- `media`: corrobora, mas nao e suficiente isolada
- `fraca`: relevante apenas em conjunto com outras
- `neutra`: presente no processo mas sem peso para nenhuma das teses
- `contraria`: esta prova favorece o reu; registrar para antecipar impugnacao

---

## §8 — Regras de qualidade do dossie

1. Cada fato e classificado em uma dimensao (§4). Fato que pertence a duas dimensoes e
   registrado na dimensao dominante com referencia cruzada na outra.
2. Fato controvertido e marcado como `controvertido: true` e aparece em `questoes.de_fato`.
3. Prova que suporta um fato deve referenciar o fato correspondente (e vice-versa).
4. Questao de direito sem norma citada e rejecao — norma e obrigatoria na formulacao da tese.
5. Lacuna com impacto `bloqueante` exige `como_suprir` preenchido; sem isso o dossie esta
   incompleto para uso por skill C5.
6. A linha do tempo inclui todos os eventos das 5 dimensoes com `relevancia` classificada.
7. `proxima_acao` e `skill_recomendada` sao obrigatorios ao final do dossie.

---

## §9 — Pipeline operacional

```
1. Receber dados (relato, documentos, ou output de levanta-fatos)
2. Confirmar identificacao e numero do processo (§3)
3. Qualificar partes — autor primeiro, depois reu e terceiros (§5)
4. Preencher fatos nas 5 dimensoes (§4), marcando controvertidos
5. Construir linha do tempo unificada (§0 schema: cronologia)
6. Mapear questoes de fato e de direito (§6)
7. Inventariar provas com conteudo + interpretacao + forca (§7)
8. Identificar lacunas com impacto e como_suprir
9. Identificar riscos com probabilidade e mitigacao
10. Preencher status_atual, proxima_acao, skill_recomendada
11. Verificar regras de qualidade (§8)
12. Entregar dossie no formato dossie-caso.v1.json
    (R1: perguntar antes de exportar em arquivo)
```

---

## §10 — Contrato de execucao (preconditions / postconditions)

Preconditions:
- Nome e CPF do cliente fornecidos
- Pelo menos um fato em pelo menos uma das 5 dimensoes preenchido
- Fase atual identificada

Postconditions:
- Output conforme `_compartilhados/SCHEMAS/output/dossie-caso.v1.json` v1.1.0
- Pelo menos uma questao de fato ou de direito mapeada
- `proxima_acao` e `skill_recomendada` preenchidos
- Lacunas com impacto bloqueante com `como_suprir` preenchido

---

## §11 — Auto-verificacao

Ultima verificacao de conformidade: 2026-05-12
Proxima verificacao: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em <= 90 dias
- [x] R1, R2, R3, R6, R10, R11 aplicaveis presentes
- [x] §1 com FACO/NAO FACO/DELEGO PARA explicito
- [x] 5 dimensoes de fatos documentadas (§4)
- [x] Distincao questao de fato vs. questao de direito (§6)
- [x] Provas com conteudo objetivo + interpretacao + forca (§7)
- [x] Qualificacao completa das partes com ponto de referencia (§5)
- [x] Preconditions e postconditions declaradas (§10)
- [x] Output conforme schema dossie-caso.v1.json v1.1.0
- [x] git_auto_commit: false (declaracao honesta — L19)
- [x] chains_to somente com skills existentes na biblioteca — L20
- [x] Tamanho dentro do limite
