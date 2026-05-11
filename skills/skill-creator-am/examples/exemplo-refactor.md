# Exemplo: REFACTOR — Otimizar skill existente

## Cenário

Durante auditoria mensal, `extrair_para_compartilhados.py` detecta:
- 85 linhas duplicadas entre `skill-analise-precedente` e `skill-gotcha-skill`
- Ambas extraem "teses jurídicas" com lógica quase idêntica

**skill-creator-am propõe:**

```
🔍 REFACTOR sugerido:

Duplicação encontrada:
  - analise-precedente (linhas 45-130): função extrair_teses()
  - gotcha-skill (linhas 120-205): função extrair_teses()
  
Similaridade: 92% (super alta → confirma duplicação real)

Proposta de refactor:
  1. Extrair função comum: _compartilhados/rotinas/extrair_teses_comum.py
  2. Ambas as skills importam: from rotinas.extrair_teses_comum import extrair_teses
  3. Resultado: 85 linhas → 1 import
  4. Impacto: reduz bloat, centraliza lógica, facilita manutenção

Benefícios:
  ✅ Menos duplicação (85 → 0 linhas duplicadas)
  ✅ Única fonte de verdade para extrair_teses()
  ✅ Manutenção centralizada
  ✅ Testes unitários em um lugar só

Backup automático será criado antes da operação.
Quer prosseguir?
```

**Usuária: "Sim, procede"**

```
✅ REFACTOR executado

Operações:
  1. Backup criado: _backups/analise-precedente-REFACTOR-20260511-110230/
  2. Backup criado: _backups/gotcha-skill-REFACTOR-20260511-110231/
  3. Arquivo criado: _compartilhados/rotinas/extrair_teses_comum.py
  4. SKILL.md (analise-precedente): import adicionado
  5. SKILL.md (gotcha-skill): import adicionado
  6. Versões atualiz adas: ambas → v1.0.0 (compatível, refactor interno)

Log registrado:
  2026-05-11 | 11:02 | REFACTOR | analise-precedente + gotcha-skill | v1.0.0 | ativa | 
    Extraída função extrair_teses_comum() para _compartilhados/rotinas/; 
    reduziu duplicação de 85→0 linhas

Próxima auditoria: 2026-06-11
```

**Resultado:**
```
Antes (duplicação):
  analise-precedente: 500 linhas
  gotcha-skill: 480 linhas
  Total: 980 linhas (85 duplicadas)

Depois (refactor):
  _compartilhados/rotinas/extrair_teses_comum.py: 85 linhas
  analise-precedente: 420 linhas (importa da rotina)
  gotcha-skill: 400 linhas (importa da rotina)
  Total: 905 linhas (-75 linhas de bloat)
  
  Economia: 7.6% menos código, sem perda de funcionalidade
```

Se precisar desfazer:
```
python undo_operacao.py --refactor-id 20260511-110230
```
