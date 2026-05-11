# mod4 / reference 05 — Schema de input

## Campos

**Obrigatórios:** `enderecamento`, `qualificacao_autora`, `nome_acao`, `secoes`, `assinatura`

**Opcionais:** `tribunal_localizacao`, `processo`, `subtitulo_acao`, `qualificacao_re`, `pedidos`, `valor_causa`, `data`

## Tipos de conteúdo em `secoes[].conteudo[]`

| tipo | Uso | Campos adicionais |
|---|---|---|
| `paragrafo` | Corpo padrão com firstLine=720 | `texto` |
| `subtitulo` | Hierarquia decimal (1.1, 1.2...) | `texto` |
| `referencia_doc` | Nome de arquivo em negrito | `texto` |
| `blockquote` | Transcrição literal 4+ linhas | `texto` |
| `tabela` | Tabela com cabeçalho navy/zebra creme | `colunas`, `linhas`, `larguras`, `titulo` |
| `lista` | Lista numerada | `itens` |
| `caixa_destaque` | Fundo creme-claro, barra navy | `texto` |
| `precedente` | Jurisprudência com estrutura tripartida | `referencia`, `ementa_curta`, `aplicacao` |

**PROIBIDOS** (serão rejeitados pelo script com erro explícito):
`caixa_vicio`, `caixa_tese`, `caixa_advertencia`, `caixa_ressalva`

## Campo `sintese`

BLUF imediatamente após o título da seção. Declara a conclusão antes do argumento. Se vazio ou ausente, o espaço é pulado. Cambria 11pt negrito.

## Exemplo mínimo válido

```json
{
  "enderecamento": "Excelentíssimo Juízo da 3ª Vara de Acidentes do Trabalho\nda Comarca de São Paulo/SP",
  "qualificacao_autora": "MARIA DA SILVA, brasileira, ..., vem respeitosamente à presença de Vossa Excelência, por sua advogada infra-assinada, propor a presente",
  "nome_acao": "Ação de Concessão de Benefício Previdenciário",
  "secoes": [
    {
      "titulo": "I. PRELIMINARES E REQUISITOS PROCESSUAIS",
      "conteudo": [
        {"tipo": "paragrafo", "texto": "1. Representação processual: a autora é representada pela advogada Raquel de Almeida Marques, OAB/SP 519.794, nos termos da procuração juntada (cf. **Procuração**, doc. 1)."},
        {"tipo": "paragrafo", "texto": "2. Endereço para intimações: Av. Paulista 1636, sl 1105/876, Bela Vista, São Paulo/SP, CEP 01310-200. E-mail: raquelmarques@almeidamarques.adv.br."}
      ]
    },
    {
      "titulo": "II. DOS FATOS",
      "sintese": "A autora é portadora de LES com nefrite classe III/IV, incapaz para o trabalho desde março de 2019.",
      "conteudo": [
        {"tipo": "paragrafo", "texto": "A autora foi diagnosticada com Lupus Eritematoso Sistêmico em março de 2019 (cf. **Laudo de Reumatologia**, doc. 3, fl. 12–14)."},
        {"tipo": "caixa_destaque", "texto": "O laudo pericial de fls. 143–158 reconhece expressamente a incapacidade total e permanente, fixando a DII em 12/03/2019."}
      ]
    }
  ],
  "pedidos": [
    "A concessão do benefício de Aposentadoria por Incapacidade Permanente (B32), desde a data do requerimento administrativo (12/07/2020).",
    "O pagamento das parcelas vencidas, corrigidas pelo INPC e acrescidas de juros."
  ],
  "valor_causa": "Dá-se à causa o valor de R$ 15.000,00 (quinze mil reais).",
  "data": "11 de maio de 2026",
  "assinatura": "Raquel de Almeida Marques"
}
```

## Regras de montagem do JSON pelo Claude

1. A primeira entrada de `secoes[]` deve ser sempre PRELIMINARES. Se o conteúdo fornecido pela Raquel não incluir PRELIMINARES, inserir com conteúdo mínimo (representação + endereço).
2. `data` deve ser por extenso: "11 de maio de 2026", não "11/05/2026".
3. `pedidos` deve seguir a ordem: incontroverso → principal → secundários → subsidiários → prova/diligência → gerais.
4. `valor_causa` deve conter o valor por extenso entre parênteses.
5. `texto` em `referencia_doc` deve seguir o formato: `"[Número] — [nome do documento] — [autoria ou fonte]"`.
6. Remissão probatória dentro de `paragrafo.texto`: sempre no formato `(cf. **[nome]**, doc. [N], [fl. X–Y])`.
