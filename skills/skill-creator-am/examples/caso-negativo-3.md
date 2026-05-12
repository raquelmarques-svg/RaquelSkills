# Caso negativo 3 — Falha por artefatos incompletos (MODELOS/ com < 70% conteúdo)

## Input

Raquel: "criar skill ms para mandado de segurança"

*(após §0-Ativação e verificações, a skill-creator-am gera o SKILL.md, mas produz MODELOS/ com apenas cabeçalhos e instruções de preenchimento — sem texto jurídico pronto)*

## Comportamento esperado

A skill-creator-am detecta na Auditoria A13 que os modelos têm < 70% de conteúdo pronto e bloqueia o empacotamento.

### Fluxo

**Geração inicial — MODELOS/ insuficiente:**

```markdown
# Modelo — Fumus Boni Iuris

## Quando usar
[descrever quando usar]

## Estrutura
[escrever o texto aqui]

## Instruções
[preencher com o caso concreto]
```

O arquivo acima tem 6 linhas de conteúdo real, 4 são placeholders generalizados — 67% de placeholder, acima do limite de 30%.

**Auditoria A13 — falha detectada:**

```
🔴 AUDITORIA A13 — FALHA

MODELOS/fumus_boni_iuris.md: 67% de placeholder (limite: 30%)
MODELOS/periculum_in_mora.md: 71% de placeholder (limite: 30%)
MODELOS/pedido_liminar.md: 58% de placeholder (limite: 30%)

Os modelos acima não têm conteúdo jurídico suficiente para uso direto.
Um modelo com > 30% de placeholder exige que o Claude invente o conteúdo
na hora do uso, gerando inconsistência entre sessões (L10).

Ação requerida: reescrever os modelos com texto jurídico completo.
Nenhum arquivo empacotado antes da correção.
```

**Correção aplicada — MODELOS/ com conteúdo real:**

```markdown
# Modelo — Fumus Boni Iuris

## Quando usar
Quando o ato coator viola direito líquido e certo documentalmente comprovado
e a contestação do impetrado se limita a defender a legalidade formal do ato
sem enfrentar o mérito do direito alegado.

## Estrutura

O fumus boni iuris assenta-se em dois pilares autônomos e cumulativos.

O primeiro é normativo: o art. [X] da [Lei/Resolução/Portaria] assegura ao
impetrante o direito de [descrever o direito], independentemente de [condição
que o impetrado exige indevidamente]. A exigência imposta pelo impetrado —
[descrever a exigência] — não encontra amparo no texto normativo citado e
configura extensão analógica proibida na esfera administrativa restritiva.

O segundo é probatório: o documento de fl. [N] demonstra que o impetrante
[descrever o fato comprovado]. Diante dessa prova pré-constituída, o direito
alegado é líquido e certo nos termos do art. 1º, §1º, da Lei 12.016/2009.

## Instruções de preenchimento
- [X]: número do artigo normativo aplicável
- [Lei/Resolução/Portaria]: identificar o diploma normativo
- [descrever o direito]: direito concreto do impetrante
- [condição que o impetrado exige]: requisito ilegal imposto
- [fl. N]: indicar o documento nos autos

## Variante — quando há negativa expressa do impetrado
[texto alternativo para quando o impetrado negou expressamente o direito
em manifestação escrita juntada ao processo]
```

**Auditoria A13 — aprovada após correção:**
- fumus_boni_iuris.md: 12% placeholder → verde
- periculum_in_mora.md: 18% placeholder → verde
- pedido_liminar.md: 22% placeholder → verde

## Output esperado

**Na falha:** mensagem de bloqueio com arquivo por arquivo, percentual de placeholder, motivo (L10) e instrução de correção. Nenhum .skill gerado.

**Após correção:** aprovação em A13, empacotamento, §4-G (Git sync), entrega via present_files.

## Critério de aprovação

- A13 executada antes do empacotamento
- Bloqueio claro com diagnóstico quantitativo por arquivo
- Referência à L10 na mensagem de bloqueio
- Nenhum arquivo gerado enquanto A13 falha
- Empacotamento só após correção e re-aprovação

## Erros que invalidariam o teste

- Empacotar a skill com MODELOS/ incompletos sem bloquear
- Reportar A13 como aviso (amarelo) quando placeholder > 30% — deve ser vermelho (bloqueio)
- Não referenciar L10 na mensagem
- Corrigir os modelos autonomamente sem mostrar o diff à Raquel para aprovação
