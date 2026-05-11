# RaquelSkills — Almeida Marques V4

Biblioteca de skills jurídicos e processamento de documentos.

**Arquitetura**: V4 (desde 2026-05-11)  
**Ambiente**: Windows 10+, Python 3.14.3, Git  
**Status**: Em desenvolvimento — Tier 2 concluído

---

## 🚀 Quick Start

### Criar nova skill
```powershell
cd C:\RaquelSkills\skills
mkdir [skill-name]
# skill-creator-am guia você no processo
```

### Auditar biblioteca
```powershell
cd C:\RaquelSkills\_compartilhados\rotinas
python auditar_skill_completo.py --todas --salvar
# Gera: C:\RaquelSkills\governanca\audit-YYYYMM.md
```

### Desfazer última operação
```powershell
python undo_operacao.py --skill [skill-name]
# Restaura de _backups/
```

---

## 📁 Estrutura

```
C:\RaquelSkills/
├── skills/                        (Skills implementadas)
│   └── skill-creator-am/          ✅ Orquestrador V4
│       ├── SKILL.md
│       ├── README.md
│       ├── examples/
│       ├── templates/
│       └── schemas/
├── _compartilhados/               (Código compartilhado)
│   ├── rotinas/                   (Scripts orquestradores)
│   │   ├── auditar_skill_completo.py
│   │   ├── log_auditoria.py
│   │   ├── parser_skill_md.py
│   │   ├── extrair_para_compartilhados.py
│   │   └── undo_operacao.py
│   ├── templates/                 (Templates reutilizáveis)
│   └── calculos/                  (Funções matemáticas/jurídicas)
├── _backups/                      (Backup automático — não versionar)
├── outputs/                       (Saída de skills — não versionar)
├── _APAGAR/                       (Scratch area — não versionar)
├── .gitignore                     (Regras de versionamento)
├── README.md                      (Este arquivo)
├── MIGRACAO_V6.5.2_PARA_V4.md    (Histórico de transição)
└── .claude/                       (Configuração interna)
    └── skills/_internal/
        └── governanca-skills/     (Referência histórica V6.5.2)

/Drive/Claude/                     (Vivo — informações em evolução)
├── informacoes/                   (7 documentos canônicos)
│   ├── regras-universais.md       (R1-R11)
│   ├── padrao-redacional.md
│   ├── licoes-mod4.md
│   └── ...
├── governanca/                    (Controle)
│   ├── _inventario.md             (33 skills planejadas)
│   ├── _log-auditoria.md          (Operações registradas)
│   └── audit-YYYYMM.md            (Relatório mensal)
├── glossario/                     (Termos — 6 frentes)
│   ├── transversal/
│   ├── F1-previdenciario/
│   └── ...
└── jurisprudencia/                (Precedentes — 8 tribunais)
    ├── stf/
    ├── stj/
    └── ...
```

---

## 🎯 Governança V4

**Regras universais** (R1-R11):
- **R1**: Exportação — perguntar antes de gerar
- **R2**: Preservação — nunca apagar (mover para _APAGAR/)
- **R3**: Backup — backup antes de modificar
- **R6**: Adaptação — propor ajuste antes de negar
- **R9**: Auditoria — mensal, automatizada
- **R10**: Discordância — apontar inconsistências
- **R11**: Economia — planejar antes de executar

Veja: `C:\Users\raque\Meu Drive\Claude\informacoes\regras-universais.md`

---

## 📊 Requerimentos

### Sistema
- Windows 10 ou posterior
- PowerShell 5.1+
- 10 GB de espaço livre

### Software
- **Python** 3.14.3+
- **Git** 2.40+
- **Tesseract OCR** 5.x + tessdata português
- **Whisper** (openai-whisper) com modelo medium (1.5 GB)

### Biblioteca Python
```
python-docx, openpyxl, pdfplumber, pytesseract, pillow,
pdfminer.six, python-dateutil, holidays, lxml, regex, pyyaml
```

---

## 🔄 Workflow típico

### 1. Criar skill
```
Você: "Quero skill que analisa precedentes judiciais"
skill-creator-am: Valida, propõe estrutura
Resultado: C:\RaquelSkills\skills\analise-precedente\SKILL.md
```

### 2. Implementar
```
Você edita SKILL.md, preenche examples/, templates/
Testa com auditar_skill_completo.py --skill analise-precedente
```

### 3. Refatorar (se necessário)
```
extrair_para_compartilhados.py detecta duplicação
skill-creator-am propõe REFACTOR
Resultado: Função comum em _compartilhados/rotinas/
```

### 4. Auditar (mensal)
```
python auditar_skill_completo.py --todas --salvar
Resultado: governanca/audit-202605.md (por exemplo)
```

---

## 📖 Documentação

| Documento | Localização | Propósito |
|-----------|-------------|----------|
| Regras R1-R11 | `/Drive/Claude/informacoes/regras-universais.md` | Governança |
| Padrão redacional | `/Drive/Claude/informacoes/padrao-redacional.md` | Escrita jurídica |
| Inventário | `governanca/_inventario.md` | Lista de skills |
| Auditoria mensal | `governanca/audit-YYYYMM.md` | Relatório mensal |
| Migração V6.5.2→V4 | `MIGRACAO_V6.5.2_PARA_V4.md` | Histórico |
| skill-creator-am | `skills/skill-creator-am/README.md` | Como criar skills |

---

## 🧪 Teste de integridade

```powershell
# Verificar ambiente
python -c "import yaml, docx, openpyxl; print('✅ OK')"

# Verificar Git
git remote -v

# Verificar Tesseract
tesseract --list-langs

# Verificar Whisper
python -c "import whisper; print(whisper.__version__)"

# Primeira auditoria
cd _compartilhados\rotinas
python auditar_skill_completo.py --todas --salvar
```

---

## 🤝 Contribuindo

1. **Criar skill**: Use skill-creator-am
2. **Editar skill**: Use skill-creator-am EDIT mode
3. **Refatorar**: Use skill-creator-am REFACTOR mode
4. **Auditar**: Execute mensalmente auditar_skill_completo.py
5. **Commit**: `git add . && git commit -m "..."`
6. **Push**: `git push origin main`

---

## 📝 Histórico

| Data | Versão | Marcos |
|------|--------|--------|
| 2026-05-11 | V4.0 | Tier 0 + Tier 1 + Tier 2 completo |
| — | V6.5.2 | Arquitetura anterior (governanca-skills) |

---

## 📞 Suporte

- **Criar skill**: Veja `skills/skill-creator-am/examples/`
- **Auditar**: Execute `auditar_skill_completo.py --help`
- **Backup**: Recupere de `_backups/[skill-name]/`
- **Histórico**: Consulte `MIGRACAO_V6.5.2_PARA_V4.md`

---

**Desenvolvido por**: Raquel de Almeida Marques  
**Mantido com**: Claude (Anthropic) + skill-creator-am  
**Licença**: Privada — Almeida Marques Advocacia
