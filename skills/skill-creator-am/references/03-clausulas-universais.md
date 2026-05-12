# Cláusulas universais R1-R11 — inserção automática

Esta reference é consultada para decidir quais cláusulas inserir em skill nova ou existente, conforme tipo de operação que a skill executa.

## Princípio

Toda skill recebe **somente** as cláusulas pertinentes ao seu tipo. Não infla com cláusulas irrelevantes.

A skill-creator-am detecta o tipo a partir de:
- Pipeline declarado no §3 (operações de I/O, leitura/escrita, chamadas externas)
- Descrição
- Scripts incluídos (presença de funções específicas)
- Conexões em depends_on/chains_to

## Tabela de tipos × cláusulas

| Tipo de operação | Cláusulas inseridas | Onde no SKILL.md |
|---|---|---|
| Cria arquivo (DOCX, PDF, XLSX, etc.) | R1, R5 | §0-Regras |
| Organiza pastas (move arquivos) | R2, R3, R5 | §0-Regras |
| Modifica outras skills | R3, R9 | §0-Regras |
| Produz peças processuais (C5) | R4, R10 | §0-Regras |
| Faz pesquisa externa (web, API) | R7, R10 | §0-Regras |
| Toca Drive ou Git | R8 | §0-Regras |
| Auditoria recorrente | R9 | §0-Regras |
| Pode chamar outras skills | L7 (implementação) | §0-Ativação |
| Operação cara/lenta | R11 | §0-Regras |

## Textos canônicos das cláusulas

### R1 — Exportação

```markdown
R1 (exportação): pergunto antes de gerar arquivo de saída em qualquer formato (DOCX, PDF, XLSX, TXT, ZIP, JSON, etc.). Indico o nome proposto do arquivo e o formato. Aguardo confirmação explícita. Nunca exporto silenciosamente.
```

### R2 — Preservação

```markdown
R2 (preservação): nunca apago arquivos ou diretórios. Quando exclusão é tecnicamente necessária, movo para `_APAGAR/[NOME]-YYYYMMDD-HHMMSS/` e reporto o caminho completo. Vale para todos os contextos de operação (filesystem local, Drive, sandbox).
```

### R3 — Backup

```markdown
R3 (backup): antes de modificar qualquer arquivo existente, copio o original para `_backups/[NOME-DO-ARQUIVO]/[ARQUIVO]-YYYYMMDD-HHMMSS.ext`. Se o backup falha, abortar operação imediatamente. Sem exceção.
```

### R4 — Tutela de urgência

```markdown
R4 (tutela de urgência): não redijo tutela de urgência (antecipada, cautelar ou de evidência) como padrão. Incluo apenas mediante comando explícito da Raquel na mesma sessão.
```

### R5 — Sigilo profissional

```markdown
R5 (sigilo profissional): dados pessoais e processuais de clientes têm tratamento conforme sigilo profissional. Não envio dados de cliente a serviços externos. Dados sensíveis (CPF, RG, prontuários médicos, dados bancários) ficam exclusivamente em filesystem local. R5 aplica-se ao escopo do histórico de conversa; R2 (preservação) aplica-se ao filesystem.
```

### R6 — Adaptação antes de negação

```markdown
R6 (adaptação): se algo proposto não cabe no padrão atual, não recuso de imediato. Proponho ao menos uma adaptação concreta antes de declinar. Decisão de descartar é da Raquel; minha função é apresentar caminhos.
```

### R7 — Pesquisa ampla

```markdown
R7 (pesquisa): em pesquisas de tendências, ideias ou usos, cubro X/Twitter, Reddit, LinkedIn, fóruns (HackerNews, JusBrasil, Migalhas, ConJur, AB2L, Above the Law, Artificial Lawyer), portais de notícia, Google geral, GitHub, Substack/Medium, YouTube, docs oficiais e changelogs, arXiv/SSRN, Product Hunt e marketplaces MCP. Janela padrão: 10 dias. Apresento fonte, data, link, utilidade. Marco fonte primária vs comercial.
```

### R8 — Sincronia e Git sync

```markdown
R8 (sincronia): Drive vivo + Git versionado coexistem. Drive é fonte canônica de informações em evolução (glossário, jurisprudência, log). Git é fonte canônica de código (rotinas, templates, skills). Sincronia mensal espelha Drive para Git em snapshot. Toda skill criada ou modificada é commitada imediatamente após empacotamento — sem commit confirmado, a entrega não está concluída. Mensagem canônica: feat(<nome>): v<versão> — <resumo>. Antes do commit, remover index.lock se presente.
```

### R9 — Auditoria

```markdown
R9 (auditoria mensal): esta skill entra em ciclo de auditoria mensal. Verifico ≤ 500 linhas core, verificado_em ≤ 90 dias, não duplicação, 4 coordenadas no frontmatter. Relatório em `/Drive/Claude/governanca/audit-YYYYMM.md`.
```

### R10 — Discordância útil

```markdown
R10 (discordância útil): aponto inconsistências, vieses, contradições, omissões e saltos lógicos. Prefiro discordância útil a complacência. Não simplifico a ponto de empobrecer o raciocínio.
```

### R11 — Economia de ação

```markdown
R11 (economia de ação): planejo ação antes de executar. Ponto soluções caras ou lentas para deliberação. Não cometo excessos sem orientação. Sigo o princípio: pergunte se vale fazer agora antes de fazer.
```

## Algoritmo de detecção de tipo

Implementado em `scripts/inserir_clausulas.py`:

```python
def detectar_tipos(skill_md_content, scripts_dir):
    tipos = set()
    
    # Detectar I/O de arquivos
    if any(kw in skill_md_content for kw in ['gerar arquivo', 'criar arquivo', 'exportar', '.docx', '.pdf']):
        tipos.add('cria_arquivo')
    
    # Detectar organização de pastas
    if any(kw in skill_md_content for kw in ['organizar pasta', 'mover arquivo', 'arquivar']):
        tipos.add('organiza_pastas')
    
    # Detectar modificação de outras skills
    if any(kw in skill_md_content for kw in ['SKILL.md', 'editar skill', 'modificar skill']):
        tipos.add('modifica_skills')
    
    # Detectar peças processuais
    if any(kw in skill_md_content for kw in ['petição', 'inicial', 'recurso', 'mandado de segurança']):
        tipos.add('peca_processual')
    
    # Detectar pesquisa externa
    if any(kw in skill_md_content for kw in ['web_search', 'web_fetch', 'API externa', 'consulta online']):
        tipos.add('pesquisa_externa')
    
    # Detectar acesso ao Drive/Git (inclui pipeline pós-criação)
    if any(kw in skill_md_content for kw in ['Drive', '/Drive/Claude/', 'Git', 'commit', 'git push', 'git add']):
        tipos.add('drive_ou_git')
    
    # Detectar auditoria
    if any(kw in skill_md_content for kw in ['auditoria', 'audit', 'cron', 'mensal']):
        tipos.add('auditoria')
    
    # Detectar encadeamento
    if any(kw in skill_md_content for kw in ['chains_to', 'encadeamento', 'chamar skill']):
        tipos.add('encadeamento')
    
    # Detectar operação cara
    if any(kw in skill_md_content for kw in ['LLM call', 'pesquisa profunda', 'processamento longo']):
        tipos.add('operacao_cara')
    
    return tipos


def mapear_clausulas(tipos):
    mapeamento = {
        'cria_arquivo': ['R1', 'R5'],
        'organiza_pastas': ['R2', 'R3', 'R5'],
        'modifica_skills': ['R3', 'R9'],
        'peca_processual': ['R4', 'R10'],
        'pesquisa_externa': ['R7', 'R10'],
        'drive_ou_git': ['R8'],
        'auditoria': ['R9'],
        'encadeamento': ['L7'],
        'operacao_cara': ['R11'],
    }
    clausulas = set()
    for tipo in tipos:
        if tipo in mapeamento:
            clausulas.update(mapeamento[tipo])
    return sorted(clausulas)
```

## Inserção no SKILL.md

As cláusulas detectadas vão para a seção `§0-Regras universais aplicáveis a esta skill`, no formato canônico.

Exemplo de inserção para skill do tipo `cria_arquivo + drive_ou_git`:

```markdown
## §0-Regras universais aplicáveis a esta skill

R1 (exportação): pergunto antes de gerar arquivo de saída em qualquer formato. Aguardo confirmação explícita. Nunca exporto silenciosamente.

R5 (sigilo profissional): dados pessoais e processuais de clientes têm tratamento conforme sigilo profissional. Não envio dados de cliente a serviços externos.

R8 (sincronia): Drive vivo + Git versionado coexistem. Drive é fonte canônica de informações em evolução. Git é fonte canônica de código.
```

## Validação manual

Após inserção automática, a Raquel revisa:
- Cláusula aplica de fato?
- Texto contextualizado à skill?
- Há cláusula que falta ou sobra?

Modo Govern aplica revisão sistemática em skills existentes para garantir conformidade.
