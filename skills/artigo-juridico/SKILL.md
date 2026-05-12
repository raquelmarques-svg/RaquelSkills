---
name: artigo-juridico
description: |
  Use esta skill para escrever, revisar, criticar, melhorar ou reformatar artigos científicos jurídicos em português brasileiro — especialmente para periódicos como Revista do CNMP, Revista de Direito Administrativo, Atuação, ou qualquer revista jurídica científica nacional. Ative sempre que a usuária mencionar: "escreva o artigo", "revise o artigo", "critique o artigo", "melhore o artigo", "coteje com guia de escrita acadêmica", "reescreva à luz das correções", "análise frase por frase", "análise parágrafo por parágrafo", "seção por seção", "artigo científico jurídico", "publicação em revista jurídica". Ativar também quando a usuária pedir para verificar palavras-chave, resumo, hipótese, referências, remissões normativas ou estrutura canônica de artigo acadêmico jurídico.
project: NT3
nucleo: N2
frente: constitucional
camada: C2
categoria: capability
version: 2.0.0
verificado_em: 2026-05-12
git_repo: C:\RaquelSkills
git_auto_commit: true
depends_on: []
chains_to:
  - mod4
licoes_aplicadas:
  - L1, L2, L3, L5, L10, L11
regras_aplicaveis:
  - R1, R2, R3, R6, R10, R11
---

# artigo-juridico — Produção e Revisão de Artigos Científicos Jurídicos

## §0 — Ativação e gates

Ativar quando a usuária mencionar: escrever artigo, revisar artigo, critique o artigo,
coteje com guia de escrita, análise frase por frase, artigo científico jurídico, periódico
jurídico, publicação em revista jurídica.

## §0 — Regras universais

R1 (exportação): perguntar antes de gerar DOCX ou PDF.
R2 (preservação): nunca deletar; itens removidos vão para `_APAGAR/` com timestamp.
R3 (backup): backup antes de modificar SKILL.md existente.
R6 (adaptação): propor ajuste antes de recusar.
R10 (discordância útil): diagnóstico real, não complacência.
R11 (economia de ação): ponderar custo antes de propor solução cara.

## §1 — Escopo

FAÇO:
- Escrita de artigo científico jurídico desde o zero
- Revisão sistemática em três passes (seção, parágrafo, frase)
- Diagnóstico de qualidade com checklist canônico completo
- Verificação de palavras-chave, resumo/abstract, hipótese, remissões normativas
- Análise de conceitos e categorias analíticas novas
- Adequação ao periódico-alvo

NÃO FAÇO:
- Peça processual → delego para skill C5 pertinente
- Análise de precedente para incorporação ao artigo → acionar `analise-precedente` antes
- Formatação DOCX de entrega final → delego para `mod4`

DELEGO PARA:
- `analise-precedente` — quando o artigo invoca precedentes que precisam ser auditados
- `mod4` — formatação .docx do artigo finalizado
- skill C5 pertinente — quando o resultado alimenta peça processual

---

## §2 — Trigger semântico

| Núcleo | Exemplos |
|---|---|
| Escrita | "escreva o artigo", "parte do zero" |
| Revisão | "revise o artigo", "melhore o artigo", "frase por frase" |
| Diagnóstico | "critique o artigo", "checklist", "coteje com guia" |
| Componentes | "revise as palavras-chave", "corrija as remissões" |

---

## §3 — Perguntas obrigatórias antes de começar

Antes de escrever ou revisar, confirmar:
- Qual o periódico-alvo e sua seção temática?
- Qual o limite de laudas ou palavras?
- Existe template ou guia de submissão específico do periódico?
- Qual o prazo de submissão?
- Existe versão prévia a ser revisada, ou a escrita parte do zero?

Se o artigo já existe, ler integralmente antes de emitir qualquer diagnóstico.

---

## §4 — Checklist canônico do artigo científico

Aplicar antes de escrever qualquer versão final e depois de concluir como verificação.

### Título
- [ ] 10 a 15 palavras
- [ ] Sem "análise de" (redunda o método)
- [ ] Sem palavras que se repetem nas palavras-chave
- [ ] Específico o suficiente para identificar o argumento central

### Palavras-chave
- [ ] 4 a 6 termos
- [ ] Nenhum repete palavra do título (regra absoluta)
- [ ] Cada termo é conceito técnico ou analítico, não palavra genérica
- [ ] Pelo menos um descritor de indexação ampla (nome da lei, área do direito)

### Resumo e Abstract
O resumo deve conter cinco partes explícitas, nesta ordem:
1. Problema ou lacuna identificada
2. Objetivo do artigo
3. Método utilizado
4. Resultado principal
5. Conclusão ou contribuição

- [ ] Resumo e Abstract são espelhos precisos
- [ ] A última frase do resumo enuncia a conclusão, não as propriedades do método

### Introdução (sequência obrigatória)
- [ ] Contextualização do problema
- [ ] Identificação da lacuna ou problema específico
- [ ] Estado da arte com literatura consultada
- [ ] Nota sobre presença ou ausência de posições contrárias na literatura
- [ ] Pergunta de pesquisa explícita e delimitada
- [ ] Hipótese explícita em parágrafo próprio
- [ ] Declaração de exclusões do escopo
- [ ] Método e organização das seções
- [ ] Pontos-chave: frase final explicitando a principal contribuição

### Sumário
- [ ] Títulos do Sumário idênticos aos títulos das seções no corpo do texto

### Quadros, Figuras e Tabelas
- [ ] Título acima do elemento
- [ ] "Fonte: elaboração do autor." abaixo de todo elemento de autoria própria
- [ ] Fonte externa citada em nota quando reproduz dados de terceiros
- [ ] Elemento referenciado no texto antes de aparecer

### Notas de rodapé e Referências
- [ ] Toda referência citada em nota aparece na lista de Referências
- [ ] Toda referência na lista de Referências é citada em pelo menos uma nota
- [ ] Remissões normativas completas: art. + §/caput + inciso + alínea quando aplicável
- [ ] Referências jurisprudenciais e legislativas em seções separadas das bibliográficas

### Conclusão
- [ ] Retoma os movimentos do artigo de forma sintética (sem repetir o introdutório)
- [ ] Proposta prática, recomendação ou agenda de pesquisa futura

---

## §5 — Análise de conceitos e categorias analíticas novas

### Identificação
Listar todos os termos que: não aparecem na doutrina dominante com o sentido adotado;
são emprestados de outra área e aplicados ao direito por analogia; aparecem na doutrina
com sentido diferente do adotado no artigo.

### Avaliação de cada termo novo
1. Precisão semântica: o termo captura exatamente o que precisa sem ambiguidade?
2. Ausência de tensão interna: o termo não contradiz a tese do artigo?
3. Economia: é o termo mais curto que preserva a distinção necessária?
4. Forma curta: existe forma abreviada para uso ao longo do texto?
5. Apresentação: o termo é definido na primeira menção?

### Verificação de termos canônicos
A acepção adotada coincide com a acepção dominante? Se diverge, a divergência está
declarada e justificada? A fonte canônica está citada na primeira menção?

---

## §6 — Metodologia de revisão sistemática (três passes obrigatórios)

### Passe 1 — Seção por seção

Para cada seção: pertinência ao argumento central; cabimento (conteúdo na seção certa);
ordem na sequência lógica; construção com abertura, desenvolvimento e encerramento;
coerência com o argumento geral; fontes normativas e doutrinais corretas e atualizadas.

### Passe 2 — Parágrafo por parágrafo

Para cada parágrafo: acrescenta pelo menos um entre fato novo, risco novo, consequência
nova, providência nova, delimitação nova? Parágrafos que repetem em abstrato o que já
foi demonstrado em concreto devem ser eliminados. A frase temática está na posição adequada.
A progressão é lógica: afirmação → evidência → conclusão.

### Passe 3 — Frase por frase

**Violações críticas (reescrita obrigatória):**
- Travessão intercalado: substituir por parênteses ou ponto-e-vírgula
- Construção "não X, mas Y": reescrever de forma afirmativa
- Frase-pórtico (introdução sem conteúdo que anuncia o que virá): eliminar
- Metadiscurso sem função ("como se demonstrou", "conforme exposto"): eliminar

**Revisão de palavras:**
- Cada advérbio: é necessário? ("precisamente", "genuinamente" — sobrevive sem ele?)
- Cada adjetivo: descritivo ou decorativo?
- Cada substantivo abstrato: existe substantivo mais concreto?

**Conectivos e coerência:**
- Conectivos articulam a relação semântica correta?
- Todos os pronomes e demonstrativos têm referente inequívoco?

---

## §7 — Regras de estilo obrigatórias

### Proibições absolutas

| Proibido | Substituição adequada |
|---|---|
| Travessão intercalado | Parênteses ou vírgulas |
| "não X, mas Y" / "não X, Y" | Afirmar Y diretamente |
| Frase-pórtico | Eliminar ou converter no conteúdo |
| Metadiscurso sem função | Eliminar |
| Slogan sem fundamento | Afirmação factual com fonte |
| Adjetivação vazia | Eliminar ou converter em afirmação factual |
| Abstração sem consequência concreta | Reformular como fato, risco ou providência |
| Lista ornamental | Eliminar ou converter em prosa |
| Repetição em abstrato do demonstrado em concreto | Eliminar |

### Estrutura do raciocínio jurídico

Todo argumento deve seguir: norma → fato → conclusão. Identificar a norma com remissão
completa (lei + artigo + parágrafo + inciso). Diferenciar explicitamente fato, hipótese,
inferência, opinião, objeção e conclusão. Apontar falácias, vieses, omissões e saltos
lógicos quando surgirem.

### Exigências positivas

Terminologia unitária: o mesmo conceito recebe o mesmo nome ao longo de todo o texto.
Definição na primeira menção quando há risco de ambiguidade. Conectivos explícitos: a
relação entre proposições é marcada por conectivo preciso. Dêiticos precisos: "este",
"aquele", "essa", "tal" têm referente inequívoco. Progressão lógica forte.

---

## §8 — Remissões normativas: padrão de completude

| Nível | Correto | Incorreto |
|---|---|---|
| Artigo + parágrafo | art. 20, parágrafo único | art. 20 |
| Artigo + caput | art. 37, caput | art. 37 |
| Artigo + inciso | art. 2º, §único, VII | art. 2º |
| Artigo + alínea | art. 3º, I, alínea "a" | art. 3º, I |

---

## §9 — Formato de saída do diagnóstico

```
## Diagnóstico de qualidade — [Título]

### Checklist canônico
[Para cada item: ✅ satisfeito / ⚠️ parcial / ❌ ausente (com localização)]

### Conceitos e categorias analíticas
[Cada termo novo: avaliação de precisão, tensão interna, economia, apresentação]

### Violações críticas de estilo
[Travessões, "não X mas Y", frases-pórtico — localização + sugestão de correção]

### Problemas de parágrafo
[Parágrafos sem informação nova — localização]

### Remissões normativas incompletas
[Lista com a remissão atual e a remissão correta]

### Prioridade de correção
1. Requisitos de publicabilidade (checklist canônico)
2. Violações críticas de estilo
3. Aprimoramentos de qualidade
```

---

## §10 — Escrita desde o início

1. Confirmar os dados do §3 (periódico, limite, prazo)
2. Mapear o argumento central em uma frase
3. Derivar pergunta de pesquisa e hipótese
4. Estruturar o Sumário e validar com a usuária antes de escrever
5. Escrever seção a seção, aplicando as regras de estilo desde a primeira versão
6. Ao terminar cada seção, aplicar o Passe 3 antes de avançar
7. Ao concluir o rascunho, aplicar o checklist canônico completo (§4)
8. Entregar versão final com contagem de laudas

---

## §11 — Auto-verificação

Última verificação de conformidade: 2026-05-12
Próxima verificação: 2026-08-12

Checklist de conformidade V4:
- [x] Frontmatter completo (4 coordenadas + categoria + version + verificado_em)
- [x] verificado_em ≤ 90 dias
- [x] R1-R11 aplicáveis declaradas em §0
- [x] §1 com FAÇO/NÃO FAÇO/DELEGO PARA explícito
- [x] Três passes de revisão documentados
- [x] Checklist canônico completo em §4
- [x] git_auto_commit declarado
- [x] Volume ≤ 500 linhas
