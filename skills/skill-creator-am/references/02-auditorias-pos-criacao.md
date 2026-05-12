# Auditorias pós-criação A1–A21 — detalhamento operacional

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

## Auditoria 3 — Lições L1-L21 aplicáveis incorporadas

Critério: skill incorpora lições aplicáveis conforme tipo.

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
| L9 (UTF-8) | Toda skill com scripts Python |
| L10 (artefatos obrigatórios) | Toda skill com MODELOS/ASSETS/SCHEMAS |
| L11 (git sync) | Toda skill com pipeline de entrega |
| L12 (escopo misto) | Toda skill (sempre — via V8) |
| L13 (contrato) | Toda skill com input estruturado |
| L14-L18 (ambiente) | Skills com scripts e instalação |
| L19 (git_auto_commit) | Toda skill com frontmatter git |
| L20 (chains_to contrato) | Toda skill com chains_to declarado |
| L21 (boundary informacoes) | Toda skill que referencia _compartilhados |
| LM1-LM2 | mod4 e skills com DOCX corporativo apenas |

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

## Auditoria 17 — git_auto_commit seguro (L19)

Critério: o campo `git_auto_commit` no frontmatter não declara `true` sem evidência de pipeline funcional.

Fundamento: `git_auto_commit: true` implica que o §4-G (Git sync) foi implementado, testado e confirmado com `git push` bem-sucedido em ambiente real. Declarar `true` sem essa evidência é falsa promessa de entrega automática — a skill aparece como entregue mas o repositório não foi atualizado.

Procedimento:
1. Ler campo `git_auto_commit` no frontmatter
2. Se `git_auto_commit: true`, verificar:
   a. §4-G está presente no SKILL.md com bloco PowerShell completo?
   b. O log de auditoria registra ao menos um `git push` bem-sucedido para esta skill?
3. Se `git_auto_commit` ausente: tratar como `false` (default seguro)

Critérios:
- `git_auto_commit: false` ou campo ausente: verde (default seguro)
- `git_auto_commit: true` + §4-G presente + push confirmado no log: verde
- `git_auto_commit: true` + §4-G ausente ou push não confirmado: **vermelho (bloqueio)**

## Auditoria 18 — chains_to com contrato verificável (L20)

Critério: cada skill listada em `chains_to` existe na biblioteca instalada e tem schema de input declarado.

Fundamento: `chains_to` é um contrato de interface, não uma anotação informal. Uma skill que aponta para downstream inexistente ou sem schema cria dependência irrastreável — quando a cadeia falha, não há forma de identificar qual elo quebrou. L20 exige que todo `chains_to` seja verificável antes da criação.

Procedimento:
1. Para cada entrada em `chains_to`:
   a. Verificar existência em `C:\RaquelSkills\skills\[nome]\SKILL.md`
   b. Se existe: verificar que `SCHEMAS/` contém ao menos um arquivo de schema, OU que `_compartilhados/SCHEMAS/` contém schema referenciado por esta skill
2. Registrar: existe (S/N) + tem schema (S/N)

Critérios:
- Skill existe + tem schema: verde
- Skill existe + sem schema: amarelo (alerta — contrato parcial)
- Skill não existe: **vermelho (bloqueio)** — não criar skill com `chains_to` apontando para vazio

Exceção: skill nova que ainda será criada pode ser declarada com nota `# pendente` e prazo explícito. Sem prazo: bloqueio.

## Auditoria 19 — Boundary informacoes vs skills (L21)

Critério: nenhum arquivo de `_compartilhados/informacoes/` está instalado como `.skill` invocável, nem declarado em `depends_on` como se fosse skill funcional.

Fundamento: arquivos de referência (vocabulário, padrões redacionais, normas indexadas) são dados lidos passivamente — não são skills que executam lógica. Quando um reference file é tratado como skill, ele carrega frontmatter falso, aparece no manifesto de skills e consome slot de contexto sem produzir output. `padrao-redacional` foi o caso canônico: instalado como skill, corrigido para `_compartilhados/informacoes/` após detecção.

Procedimento:
1. Para cada entrada em `depends_on`, verificar:
   a. O caminho aponta para `_compartilhados/informacoes/`? → falha: reference file não é skill
   b. O arquivo tem `description` com verbo de ação (Crie, Gere, Audite)? → se não, suspeito de ser reference file disfarçado
2. Verificar manifesto do plugin: algum `.md` de `_compartilhados/informacoes/` está listado como skill instalada?

Critérios:
- Nenhuma violação: verde
- `depends_on` aponta para informacoes/: **vermelho (bloqueio)** — remover e referenciar como leitura contextual em §0
- Reference file no manifesto como skill: **vermelho (bloqueio)** — desinstalar e mover para informacoes/

## Auditoria 20 — Isolamento de contexto de sessão (elefante branco)

Critério: a skill declara todos os seus inputs obrigatórios explicitamente em §0 e não pressupõe contexto acumulado de outras skills ativas na mesma sessão.

Fundamento: quando múltiplas skills são carregadas na mesma sessão sem limpeza de contexto, suas instruções coexistem e competem — fenômeno de *prompt collision*. Uma skill que depende de contexto implícito (produzido por outra skill no mesmo turno sem checkpoint) falha silenciosamente: o output parece plausível mas aplica regras de outra skill. O checkpoint PRONTO/BLOQUEADO entre skills é o mecanismo de isolamento.

Procedimento:
1. Verificar se §0 lista todos os inputs que a skill precisa para operar (gate explícito)
2. Verificar se §0 não contém frases do tipo "usando o contexto anterior" ou "com base no que foi feito"
3. Se skill tem `depends_on`, verificar que o handoff é via documento (JSON, MD, DOCX) e não via contexto de sessão implícito
4. Verificar se a skill produz bloco de checkpoint (PRONTO/BLOQUEADO ou equivalente) antes de acionar `chains_to`

Critérios:
- §0 com gate explícito + handoff por documento + checkpoint de saída: verde
- §0 com gate implícito (pressupõe contexto acumulado): **amarelo** — reescrever gate
- Handoff por contexto de sessão sem documento intermediário: **vermelho (bloqueio)**
- chains_to acionado sem checkpoint de saída: **vermelho (bloqueio)**

## Auditoria 21 — Profundidade de cadeia ≤ 3 hops sem checkpoint

Critério: cadeias de `chains_to` com profundidade > 3 hops requerem checkpoint explícito (bloco PRONTO/BLOQUEADO) a cada hop.

Fundamento: uma cadeia A→B→C→D com 4 hops sem checkpoint acumula contexto de quatro skills na mesma sessão. A cada hop sem limpeza, a probabilidade de *prompt collision* cresce. O limite de 3 hops sem checkpoint é o ponto em que o custo cognitivo de rastreamento supera o benefício da automação — acima disso, o comportamento do modelo torna-se imprevisível e irrastreável para a Raquel.

Procedimento:
1. Mapear a cadeia completa a partir desta skill via `chains_to` recursivo
2. Contar hops até o primeiro skill sem `chains_to` (terminal)
3. Para cada hop além do terceiro, verificar se existe checkpoint documentado entre os dois skills

Critérios:
- Cadeia ≤ 3 hops: verde
- Cadeia de 4 hops com checkpoint em cada: verde
- Cadeia de 4+ hops sem checkpoint: **vermelho (bloqueio)** — inserir checkpoint ou quebrar a cadeia

Exceção: pipelines de auditoria interna (Audit, Diagnostico, Govern) podem ter cadeia maior porque operam em sessões isoladas e dedicadas, sem skills de conteúdo jurídico coativas.

---

## Checklist operacional atualizado (A1–A21)

```
[ ] A1:  Tamanho ≤ 500 linhas
[ ] A2:  Frontmatter completo
[ ] A3:  Lições L1-L21 aplicáveis incorporadas
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
[ ] A17: git_auto_commit seguro (false por padrão; true só com push confirmado)
[ ] A18: chains_to com contrato verificável (skill existe + tem schema)
[ ] A19: Boundary informacoes vs skills (nenhum reference file como skill invocável)
[ ] A20: Isolamento de contexto de sessão (gate explícito + handoff por documento)
[ ] A21: Profundidade de cadeia ≤ 3 hops ou checkpoint a cada hop adicional
```

Se todas verdes, criação aprovada. Senão, devolver relatório priorizado.
