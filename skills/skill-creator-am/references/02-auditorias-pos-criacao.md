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

## Checklist operacional atualizado (A1-A16)

```
[ ] A1:  Tamanho ≤ 500 linhas
[ ] A2:  Frontmatter completo
[ ] A3:  Lições L1-L13 aplicáveis incorporadas
[ ] A4:  Cláusulas R1-R11 aplicáveis presentes
[ ] A5:  Descrição diretiva
[ ] A6:  Pragmática (5 testes)
[ ] A7:  12 dimensões redacionais (se produz texto)
[ ] A8:  Vocabulário canônico
[ ] A9:  5 casos-teste em examples/
[ ] A10: Duplicação < 10 linhas
[ ] A11: Dependências consistentes
[ ] A12: verificado_em ≤ 90 dias
[ ] A13: Artefatos completos (MODELOS/ASSETS/SCHEMAS/)
[ ] A14: tests/ quando scripts/ existe
[ ] A15: ITIL/COBIT compliance (IC-1 a IC-8)
[ ] A16: Contratos de interface (CT-1 a CT-7)
```

