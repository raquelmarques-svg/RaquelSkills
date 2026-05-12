# 12 Auditorias pós-criação — detalhamento operacional

Aplicadas após geração do SKILL.md, references, scripts e examples. Cada falha registra ponto em relatório; criação não conclui até resolução ou exceção justificada.

## Auditoria 1 — Tamanho

Critério: SKILL.md core ≤ 500 linhas (ideal ≤ 300).

Procedimento:
```bash
wc -l SKILL.md
```

Resposta:
- ≤ 300 linhas: verde
- 301-450: amarelo (margem de crescimento)
- 451-500: laranja (próximo limite, próxima modificação obriga refatoração)
- > 500: vermelho (bloqueio, refatorar antes de aprovar)

References: cada arquivo ≤ 200 linhas (ideal); ≤ 400 (máximo).
Scripts: cada arquivo ≤ 200 linhas (ideal); ≤ 500 (máximo).

## Auditoria 2 — Frontmatter completo

Critério: frontmatter contém todos os campos canônicos V4.

Campos obrigatórios:
```yaml
name: string
description: string (multi-line)
project: ProjNN
nucleo: NN
frente: FN ou transversal
camada: CN
categoria: capability | preference | mista
justificativa: string (1 linha)
verificado_em: YYYY-MM-DD
version: X.Y.Z
```

Campos quase-obrigatórios:
```yaml
depends_on: lista
chains_to: lista
licoes_aplicadas: lista
regras_aplicaveis: lista
recursos_compartilhados: dict
```

Bloqueio se campo obrigatório ausente. Alerta amarelo se quase-obrigatório ausente.

## Auditoria 3 — Lições L1-L10 aplicáveis incorporadas

Critério: skill incorpora lições da mod4 conforme tipo.

Tabela de aplicabilidade:

| Lição | Aplica em |
|---|---|
| L1 (bugs path) | Toda skill que escreve arquivos |
| L2 (escopo) | Toda skill (sempre) |
| L3 (regras universais) | Toda skill (sempre) |
| L4 (pergunta por turno) | Skills que pedem confirmação |
| L5 (andaime invisível) | Skills que produzem texto |
| L6 (versão instalada) | Skills com versionamento |
| L7 (encadeamento) | Skills que chamam outras |
| L8 (ambiente-consciente) | Skills que detectam ambiente |
| L9 (zipfile sobre template) | mod4 e similares |
| L10 (letterhead VML) | mod4 apenas |

Bloqueio: aplicáveis ausentes. Alerta: justificar omissão.

## Auditoria 4 — Cláusulas R1-R11 aplicáveis presentes

Critério: skill insere cláusulas universais conforme tipo (ver reference 03).

Tabela de aplicabilidade:

| Tipo de skill | Cláusulas obrigatórias |
|---|---|
| Cria arquivos | R1, R5 |
| Organiza pastas | R2, R3, R5 |
| Modifica outras skills | R3, R9 |
| Produz peças processuais | R4, R10 |
| Faz pesquisa externa | R7, R10 |
| Toca Drive ou Git | R8 |
| Auditoria recorrente | R9 |
| Pode chamar outras skills | L7 implementação |
| Operação cara/lenta | R11 |

Bloqueio: cláusula obrigatória ausente em skill do tipo correspondente.

Implementação: `scripts/inserir_clausulas.py` detecta tipo e injeta automaticamente.

## Auditoria 5 — Descrição diretiva

Critério: campo `description` segue formato VERBO + GATILHOS + PROIBIÇÃO INVERSA.

Procedimento:
1. Extrair primeira frase do `description`
2. Verificar verbo imperativo no início (Crie, Gere, Audite, Organize, etc.)
3. Verificar presença de "INVOQUE quando" ou equivalente
4. Verificar lista de 3-7 gatilhos linguísticos
5. Verificar presença de "NÃO use" ou equivalente

Alerta vermelho se:
- Verbo ausente
- Gatilhos < 3 ou > 7
- Proibição inversa ausente

## Auditoria 6 — Pragmática

Critério: 5 testes pragmáticos passam.

Testes:
1. Atos de fala constitutivos identificáveis (declarar, comprometer, instruir)
2. Implicaturas explícitas (não há leitura ambígua)
3. Máximas de Grice respeitadas (quantidade certa, modo claro, relevância, qualidade)
4. Silêncio gerenciado (skill sabe quando não falar)
5. Duplo leitor-alvo considerado (Claude que executa + Raquel que valida)

Avaliação manual; bloqueio se 2+ testes falham.

## Auditoria 7 — 12 dimensões redacionais

Aplicável apenas a skills que produzem texto jurídico.

Dimensões:
1. Sintaxe densa
2. Conectivos explícitos
3. Vocabulário controlado
4. Unidade terminológica
5. Norma-fato-conclusão
6. Diferenciação fato/hipótese/inferência/opinião/objeção/conclusão
7. Causa-efeito-condição-limite-exceção-consequência
8. Distinção correlação-causalidade
9. Sem proibições (travessão intercalador, frase-pórtico, slogan, metáfora, adjetivação vazia, "não X mas Y")
10. Parágrafos com acréscimo (fato/risco/consequência/providência/delimitação)
11. Enumeração com função
12. Falácias/vieses/omissões apontadas

Avaliação manual; alerta vermelho se 3+ dimensões falham.

## Auditoria 8 — Vocabulário canônico respeitado

Critério: skill usa termos do glossário vivo, evita variantes proibidas.

Procedimento:
1. Ler `/Drive/Claude/glossario/transversal/` e `/Drive/Claude/glossario/F[N]-frente/` aplicáveis
2. Para cada termo no SKILL.md, verificar:
   - É forma canônica?
   - É variante proibida?
3. Listar variantes proibidas detectadas

Bloqueio: 5+ variantes proibidas em uso.
Alerta: 1-4 variantes proibidas.

Implementação: `_compartilhados/rotinas/aplica_glossario.py`.

## Auditoria 9 — Casos-teste presentes

Critério: 5 casos em examples/ (3 positivos + 2 negativos).

Procedimento:
1. Listar arquivos em `examples/`
2. Identificar casos positivos (`caso-positivo-N.md`) e negativos (`caso-negativo-N.md`)
3. Verificar formato canônico de cada

Bloqueio: < 5 casos ou formato incorreto.

## Auditoria 10 — Duplicação < 10 linhas com biblioteca existente

Critério: nenhum trecho > 10 linhas duplicado com outra skill.

Procedimento:
1. Para cada skill em `C:\RaquelSkills\skills\`:
   - Extrair blocos de 10+ linhas
   - Comparar com a skill nova
2. Listar duplicações detectadas

Critérios:
- 0 duplicações > 10 linhas: verde
- 1-2 duplicações 10-20 linhas: amarelo
- 1+ duplicação > 20 linhas: vermelho, sugerir Extract

Implementação: `scripts/verificar_duplicacao.py`.

## Auditoria 11 — Dependências consistentes

Critério: depends_on e chains_to fazem referência cruzada coerente.

Procedimento:
1. Para cada skill em `depends_on`, verificar:
   - Skill existe?
   - Skill apontada tem esta no seu `chains_to`?
2. Para cada skill em `chains_to`, verificar:
   - Skill existe?
   - Skill apontada tem esta no seu `depends_on`?

Inconsistência: alerta amarelo, sugerir ajuste em ambas as skills.
Skill apontada inexistente: bloqueio.

## Auditoria 12 — verificado_em ≤ 90 dias

Critério: data de validação dentro da janela.

Procedimento:
```python
from datetime import datetime, timedelta
verificado_em = datetime.fromisoformat(frontmatter['verificado_em'])
limite = datetime.now() - timedelta(days=90)
if verificado_em < limite:
    alerta = "vencido"
```

Para skill nova: verificado_em = data de criação → automaticamente OK.
Para skill editada: atualizar verificado_em na edição.

Alerta vermelho: verificado_em ausente ou > 90 dias.

---

## Síntese — checklist operacional

Após gerar SKILL.md + references + scripts + examples:

```
[ ] A1: Tamanho ≤ 500 linhas
[ ] A2: Frontmatter completo
[ ] A3: Lições L1-L10 aplicáveis incorporadas
[ ] A4: Cláusulas R1-R11 aplicáveis presentes
[ ] A5: Descrição diretiva
[ ] A6: Pragmática (5 testes)
[ ] A7: 12 dimensões redacionais (se produz texto)
[ ] A8: Vocabulário canônico
[ ] A9: 5 casos-teste presentes
[ ] A10: Duplicação < 10 linhas
[ ] A11: Dependências consistentes
[ ] A12: verificado_em ≤ 90 dias
```

Se todas verdes, criação aprovada. Senão, devolver relatório priorizado.

## Auditoria 13 — Artefatos completos (MODELOS/, ASSETS/, SCHEMAS/)

Critério: toda pasta declarada em `recursos_compartilhados` existe com conteúdo real.

Procedimento:
1. Ler `recursos_compartilhados` do frontmatter
2. Para cada pasta declarada, verificar existência física
3. Para MODELOS/: verificar que cada arquivo tem ≥ 70% de conteúdo pronto
   - Contar placeholders `[entre colchetes]`
   - Placeholder > 30% do arquivo = falha
4. Para ASSETS/: verificar que cada arquivo é autossuficiente (legível sem depender de outro)
5. Para SCHEMAS/: verificar que campos obrigatórios têm `description`

```python
def auditar_artefatos(skill_path):
    import yaml, re
    from pathlib import Path
    skill = Path(skill_path)
    fm = yaml.safe_load(open(skill / 'SKILL.md').read().split('---')[1])
    recursos = fm.get('recursos_compartilhados', {})
    falhas = []
    for categoria, arquivos in recursos.items():
        if not isinstance(arquivos, list): continue
        for arq in arquivos:
            p = skill / arq
            if not p.exists():
                falhas.append(f"AUSENTE: {arq}")
                continue
            if 'MODELOS' in arq or 'modelos' in arq:
                conteudo = p.read_text(encoding='utf-8')
                placeholders = len(re.findall(r'\[[^\]]+\]', conteudo))
                palavras = len(conteudo.split())
                if palavras > 0 and placeholders / palavras > 0.3:
                    falhas.append(f"INCOMPLETO (>{30}% placeholder): {arq}")
    return falhas
```

Resposta:
- 0 falhas: verde
- 1-2 falhas de conteúdo: amarelo (completar antes de aprovar)
- Pasta física ausente: vermelho (bloqueio)

## Auditoria 14 — tests/ presente quando scripts/ existe

Critério: skills com scripts Python têm infraestrutura de teste.

Procedimento:
1. Verificar se `scripts/` contém ≥ 1 arquivo `.py`
2. Se sim, verificar se `tests/` existe
3. Verificar se `tests/` contém `run_tests.py` e ≥ 2 casos (subpastas `caso-NN/`)

Resposta:
- scripts/ ausente: auditoria não aplica (verde)
- scripts/ presente, tests/ presente com run_tests.py + 2 casos: verde
- scripts/ presente, tests/ ausente: amarelo (recomendado, não bloqueante)
- scripts/ presente, tests/ com < 2 casos: amarelo


## Auditoria 15 — ITIL/COBIT compliance

Critério: skill cumpre os 8 itens do checklist IC da reference 13.

Procedimento:
1. Ler reference 13 (ITIL/COBIT)
2. Verificar cada item IC-1 a IC-8 contra o SKILL.md e o frontmatter

```
[ ] IC-1: Propósito exprimível em uma frase (ITIL value focus)
[ ] IC-2: Auditoria de biblioteca feita antes de criar
[ ] IC-3: Escopo mínimo — § 1 FAÇO tem ≤ 8 itens
[ ] IC-4: chains_to + depends_on declarados
[ ] IC-5: SLA declarado no frontmatter
[ ] IC-6: Riscos documentados
[ ] IC-7: CI registrado no _inventario.md
[ ] IC-8: Impacto em downstream analisado
```

Resposta:
- 8/8: verde
- 6-7/8: amarelo (completar antes da próxima auditoria R9)
- < 6/8: vermelho (bloqueio de uso em produção até conformidade)

## Auditoria 16 — Contratos de interface (reference 14)

Critério: skill tem contratos de input e output declarados e verificáveis.

Procedimento:
1. Verificar se SCHEMAS/ existe com schema de input
2. Verificar se schema de output está declarado (em SCHEMAS/ da skill ou em _compartilhados/SCHEMAS/)
3. Verificar presença de preconditions e postconditions no §0
4. Verificar se `produced_by` e `consumed_by` estão no schema

Checklist:
```
[ ] CT-1: Schema de input em SCHEMAS/
[ ] CT-2: Schema de output declarado
[ ] CT-3: produced_by e consumed_by no schema
[ ] CT-4: Campos obrigatórios com description e example
[ ] CT-5: Preconditions no §0
[ ] CT-6: Postconditions no §0
[ ] CT-7: SLA declarado no frontmatter
```

Resposta:
- CT-1 ou CT-2 ausentes: vermelho (bloqueio — skill sem contrato não entra em produção)
- CT-3 a CT-7 ausentes parcialmente: amarelo

---

## Auditoria 17 — git_auto_commit honesto

Critério: campo `git_auto_commit` somente é `true` quando há pipeline real de commit automatizado
comprovado (script em scripts/ que executa git commit + push sem intervenção manual).

Procedimento:
1. Verificar valor de `git_auto_commit` no frontmatter
2. Se `true`, verificar se existe script em scripts/ que chama git commit e git push
3. Se `true` sem script: falha — campo declara promessa não implementada

Resposta:
- `git_auto_commit: false` ou `git_auto_commit` ausente: verde (declaração honesta)
- `git_auto_commit: true` com script de commit funcional: verde
- `git_auto_commit: true` sem script: vermelho (bloqueio — declaração falsa em contrato)

Correção padrão: alterar para `git_auto_commit: false` e registrar em `licoes_aplicadas: L11`.

---

## Auditoria 18 — chains_to com skill instalada e schema declarado

Extensão de A11. Critério: toda skill listada em `chains_to` (a) existe na biblioteca E (b) tem
contrato de interface (schema de input em _compartilhados/SCHEMAS/ ou em sua própria SCHEMAS/).

Procedimento:
1. Para cada skill em `chains_to`:
   a. Verificar se existe em `C:\RaquelSkills\skills\[nome]\SKILL.md`
   b. Verificar se existe schema de input em:
      - `C:\RaquelSkills\_compartilhados\SCHEMAS\input\[nome]*.json` OU
      - `C:\RaquelSkills\skills\[nome]\SCHEMAS\*.json`
2. Para skill inexistente: bloqueio (A11 já detecta; A18 adiciona o contrato)
3. Para skill existente sem schema: alerta vermelho — promessa verbal não-contratual

Resposta:
- Todas presentes + todas com schema: verde
- Skill presente, schema ausente: vermelho (chains_to sem contrato é promessa verbal)
- Skill ausente: vermelho (bloqueio — A11)

Nota: skill em chains_to marcada como "ainda não instalada" pode ser declarada com prefixo
`[pendente]` no frontmatter para distinguir promessa futura de dependência ativa.

---

## Auditoria 19 — depends_on declara ASSETS/ como dependências explícitas

Critério: toda referência a arquivo em `ASSETS/` no corpo do SKILL.md deve estar listada em
`depends_on` do frontmatter, para que auditoria A11 possa verificar existência.

Procedimento:
```python
import re, yaml
from pathlib import Path

def auditar_assets_em_depends(skill_path):
    p = Path(skill_path)
    texto = (p / 'SKILL.md').read_text(encoding='utf-8')
    fm = yaml.safe_load(texto.split('---')[1])
    refs_assets = re.findall(r'ASSETS/[\w\-\.]+', texto)
    depends_on = fm.get('depends_on', [])
    ausentes = [r for r in set(refs_assets) if r not in depends_on]
    return ausentes
```

Resposta:
- 0 ASSETS não declarados: verde
- 1+ ASSETS referenciados mas ausentes de depends_on: amarelo (não bloqueante, mas
  significa que A11 não consegue verificar existência das dependências reais)

---

## Auditoria 20 — git_repo usa caminho correto para o ambiente de execução

Critério: campo `git_repo` no frontmatter usa caminho Windows (`C:\RaquelSkills`) para skills
executadas via Cowork/PowerShell; skills que executam apenas via bash Linux devem usar o caminho
de mount (`/sessions/.../mnt/RaquelSkills/`). Paths hardcoded que funcionam em apenas um
ambiente sem declaração explícita são falha de L16.

Procedimento:
1. Verificar valor de `git_repo`
2. Se contém `C:\`: verificar se a skill usa scripts PS5/PS7 (compatível)
3. Se contém `/sessions/`: verificar se a skill usa apenas bash (compatível)
4. Se contém nenhum dos dois: alerta amarelo

Resposta:
- Path Windows + skill Cowork-only: verde
- Path Linux + skill bash-only: verde
- Path Windows + skill bash-only sem conversão: amarelo (scripts falharão em ambiente Linux)
- Path ausente: amarelo (default para C:\RaquelSkills, documentar como convenção)

Correção padrão quando há ambiguidade: declarar `git_repo_windows` e `git_repo_linux`
separadamente, ou usar `resolver_output_root.py` para detecção automática.

---

## Auditoria 21 — categoria correta: capability vs. reference

Critério: skill com `categoria: capability` deve produzir output acionável por agente externo
(texto jurídico, análise estruturada, arquivo). Skill que apenas fornece vocabulário, regras ou
padrões para consumo interno de outras skills deve ser `categoria: reference` e residir em
`_compartilhados/references/`, não em `skills/`.

Procedimento:
1. Verificar campo `categoria`
2. Se `capability`: verificar se §1 FAÇO contém pelo menos um item que produz output externo
   (texto, arquivo, análise, formulário, decisão)
3. Se FAÇO contém apenas "fornece vocabulário", "define padrões", "orienta redação" sem
   produção de output: categoria incorreta → reclassificar como `reference`

Exemplos de classificação incorreta detectada:
- `padrao-redacional` como skill (fornece só padrões) → deve ser reference em _compartilhados/
- `vocabulario-controlado` como skill → deve ser reference em _compartilhados/

Resposta:
- capability com output externo documentado: verde
- capability sem output externo identificável: vermelho (reclassificar + mover para _compartilhados/)
- reference como skill em skills/: vermelho (mover para _compartilhados/references/)

---

## Checklist operacional atualizado (A1-A21)

```
[ ] A1:  Tamanho ≤ 500 linhas
[ ] A2:  Frontmatter completo
[ ] A3:  Lições L1-L18 aplicáveis incorporadas
[ ] A4:  Cláusulas R1-R11 aplicáveis presentes
[ ] A5:  Descrição diretiva
[ ] A6:  Pragmática (5 testes)
[ ] A7:  12 dimensões redacionais (se produz texto)
[ ] A8:  Vocabulário canônico
[ ] A9:  5 casos-teste em examples/
[ ] A10: Duplicação < 10 linhas
[ ] A11: Dependências consistentes (chains_to + depends_on)
[ ] A12: verificado_em ≤ 90 dias
[ ] A13: Artefatos completos (MODELOS/ASSETS/SCHEMAS/)
[ ] A14: tests/ quando scripts/ existe
[ ] A15: ITIL/COBIT compliance (IC-1 a IC-8)
[ ] A16: Contratos de interface (CT-1 a CT-7)
[ ] A17: git_auto_commit honesto (true só com pipeline real)
[ ] A18: chains_to com skill instalada E schema declarado
[ ] A19: depends_on declara ASSETS/ referenciados
[ ] A20: git_repo com caminho correto para o ambiente
[ ] A21: categoria capability vs. reference correta
```

Bloqueantes (impedem aprovação da skill): A1 vermelho, A2 (campo obrigatório ausente),
A9 (< 5 casos), A11 (skill inexistente), A16 CT-1/CT-2 ausentes, A17 vermelho, A18 vermelho,
A21 vermelho.

Não-bloqueantes (registrar e corrigir na próxima auditoria R9): A3, A4, A6, A7, A8, A12,
A13 amarelo, A14, A19, A20.

