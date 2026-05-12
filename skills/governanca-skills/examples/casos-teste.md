# casos-teste — governanca-skills

## CT-01 — Biblioteca totalmente conforme

**Simulação:** todas as skills passam em A1-A21.

**Output esperado:**
```
AUDITORIA R9 — 2026-05-12  |  modo: completo
total: 16  |  verdes: 16  |  amarelas: 0  |  vermelhas: 0
── VERDES ──────────────────────────────────────
  analise-calculo-renda-bpc
  analise-precedente
  ... (lista completa)
SUMÁRIO: biblioteca APROVADA — todas as skills conformes A1-A21
```

---

## CT-02 — Skill com git_auto_commit: true detectada

**Simulação:** `analise-precedente/SKILL.md` com `git_auto_commit: true`.

**Output esperado:**
```
── VERMELHAS (ação requerida) ──────────────────
  analise-precedente: [A17] git_auto_commit: true sem pipeline §4-G documentado
SUMÁRIO: biblioteca COM BLOQUEANTES
```

---

## CT-03 — Skill com depends_on apontando para schema

**Simulação:** `check-protocolo/SKILL.md` com:
```yaml
depends_on:
  - _compartilhados/SCHEMAS/output/fatos-estruturados.v1.json
```

**Output esperado:**
```
── VERMELHAS (ação requerida) ──────────────────
  check-protocolo: [A11] depends_on contém caminho de arquivo: '_compartilhados/SCHEMAS/...'
```

---

## CT-04 — Modo rápido

**Invocação:** `python3 rodar_audit_r9.py --modo rapido`

**Comportamento esperado:** apenas A1/A2/A4/A5/A7/A11/A12/A16/A17/A18/A19/A20 verificados.
Advertências amarelas (A3/A6/A8-A10/A13-A15/A21) ignoradas.

---

## CT-05 — Invocação sem especificar caminho

**Entrada:** "governanca" (sem caminho)

**Comportamento:** skill assume padrão `C:\RaquelSkills\skills\`, confirma com usuária e inicia auditoria.
