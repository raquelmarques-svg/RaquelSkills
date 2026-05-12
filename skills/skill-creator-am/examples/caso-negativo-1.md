# Caso negativo 1 — Tentativa de criar skill duplicada

## Input

Raquel: "criar skill analise-jurisprudencial para examinar acórdãos do STF e STJ, extrair ratio decidendi e comparar com casos análogos"

## Comportamento esperado

A skill-creator-am detecta sobreposição substancial com `analise-precedente` (skill já instalada). Roda Verificação 1 (duplicidade na biblioteca) e bloqueia criação.

### Fluxo

1. **§0-Ativação — 6 perguntas iniciadas**

2. **Verificação 1 — Duplicidade — antes mesmo de completar §0:**
   
   A skill-creator-am roda comparação:
   - Nome proposto: `analise-jurisprudencial` (24 chars)
   - Biblioteca atual contém: `analise-precedente` (18 chars)
   - Distância de Levenshtein entre nomes: 14 (não imediato)
   - Mas a descrição proposta encosta no escopo declarado de `analise-precedente`:
     - Análise de acórdãos: ✓ presente em ambas
     - Ratio decidendi: ✓ presente em ambas
     - Comparação com casos análogos: ✓ presente em ambas
   - Similaridade de descrição: **78%** (acima de 60% — bloqueio vermelho)

3. **Bloqueio devolvido com transparência:**

```
🔴 BLOQUEIO — Verificação 1 (duplicidade)

A skill proposta sobrepõe substancialmente a `analise-precedente`
já instalada na biblioteca.

Comparação:
                         Proposta              analise-precedente
─────────────────────────────────────────────────────────────────
Análise de acórdãos      ✓ central             ✓ central
Ratio decidendi          ✓ extração            ✓ extração
Comparação com análogos  ✓ comparação          ✓ comparação
Tribunais cobertos       STF, STJ              STF, STJ, TJs

Similaridade de descrição: 78% (acima do limite de 60%)

Caminhos possíveis (R6 — adaptação antes de negar):

(a) Estender analise-precedente:
    Adicionar funcionalidade nova mantendo skill única.
    Vantagem: zero duplicação.
    Como: editar analise-precedente para incorporar o que falta.
    
(b) Skill complementar com escopo distinto:
    Se a proposta tem ângulo diferente (ex.: ênfase em ratio vs
    obiter, em análise quantitativa, em mapeamento por tribunal),
    refazer a descrição destacando esse ângulo único.
    
(c) Cancelar a criação:
    analise-precedente já atende a necessidade declarada.

Recomendação: (a) ou (c). 

(b) só se houver função genuinamente nova que não cabe em 
analise-precedente.
```

4. **Aguarda decisão da Raquel.**

5. **Não procede para etapas 2-7 do pipeline Create.**

6. **Não gera nenhum arquivo.**

7. **Log de tentativa bloqueada:**
   ```yaml
   - timestamp: 2026-05-11T16:00:12
     operacao: criar (bloqueada)
     skill: analise-jurisprudencial
     motivo: duplicidade com analise-precedente (78% similaridade)
     decisao_pendente: aguardando Raquel
   ```

## Output esperado

Mensagem de bloqueio clara com:
- Diagnóstico explícito da sobreposição
- Comparação lado a lado
- 3 caminhos alternativos (R6 — adaptação antes de negar)
- Recomendação substantiva
- Nenhum arquivo gerado

## Critério de aprovação

- Bloqueio acontece (não permite criar duplicata)
- Diagnóstico mostra a similaridade quantitativa
- R6 oferece adaptação concreta antes de negar
- Decisão fica com a Raquel, não com a skill
- Log registra a tentativa bloqueada
- Pipeline Create não procede para etapas posteriores

## Erros que invalidariam o teste

- Criar a skill mesmo com 78% de similaridade
- Apenas dizer "skill duplicada, recuso" sem alternativas (viola R6)
- Não mostrar quantitativamente a sobreposição
- Decidir pela Raquel ("vou estender a analise-precedente")
- Não registrar tentativa em log
