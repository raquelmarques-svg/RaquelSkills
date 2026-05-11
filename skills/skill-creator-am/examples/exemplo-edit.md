# Exemplo: EDIT — Atualizar skill existente

## Cenário

A skill `analise-precedente` v1.0.0 precisa ser atualizada para **suportar também acórdãos estrangeiros** (de cortes internacionais).

## Diálogo com skill-creator-am

**Usuária:**
```
Atualizar skill analise-precedente:
- Versão 1.0.0 → 1.1.0
- Adicionar suporte para CIDH, Corte Europeia, ITLOS
- Manter compatibilidade com v1.0.0
```

**skill-creator-am:**
```
✅ Editando skill analise-precedente

1. Backup automático criado:
   _backups/analise-precedente/analise-precedente-SKILL-20260511-103045.md

2. Frontmatter atualizado:
   version: 1.0.0 → 1.1.0
   verified_in: 2026-05-11 → 2026-05-11 (data de edit, não auditoria)

3. SKILL.md modificado:
   - Nova seção: "Cortes internacionais"
   - Exemplos: acórdão CIDH, sentença ITLOS

4. Compatibilidade verificada:
   - v1.1.0 é backward-compatible (aceita inputs v1.0.0)
   - ✅ Sem breaking changes

5. Log registrado:
   2026-05-11 | 10:50 | EDIT | analise-precedente | v1.0.0 → v1.1.0 | ativa | Adicionado suporte para cortes internacionais (CIDH, Corte Europeia, ITLOS)
```

**Resultado:**
```
✅ Skill atualizada com sucesso

- Versão em _inventario.md: 1.1.0
- Backup preservado: _backups/analise-precedente/
- Log registrado em _log-auditoria.md
- Próxima auditoria: 2026-06-11 (30 dias)

Se precisar desfazer, use:
  python undo_operacao.py --skill analise-precedente
```
