#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executa casos de teste do recorte-pdf. Requer PDF de amostra em tests/caso-01/."""
import json, subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "recortar_pdf.py"
CASOS  = sorted((Path(__file__).parent).glob("caso-*/input.json"))

if not CASOS:
    print("INFO: nenhum caso de teste com PDF disponível — testes pulados")
    sys.exit(0)

ok = 0
fail = 0
for caso_input in CASOS:
    inp = json.loads(caso_input.read_text(encoding="utf-8"))
    pdf = Path(caso_input.parent / inp.get("pdf_path", "sample.pdf"))
    if not pdf.exists():
        print(f"  SKIP  {caso_input.parent.name} — PDF ausente ({pdf.name})")
        continue
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--pdf",    str(pdf),
         "--pages",  inp["pages"],
         "--region", inp.get("region", "inteira"),
         "--dpi",    str(inp.get("dpi", 150)),
         "--output", "/tmp/recorte_test",
         "--prefix", inp.get("prefixo", "teste")],
        capture_output=True, text=True
    )
    if result.returncode == 0 and "OK" in result.stdout:
        print(f"  PASS  {caso_input.parent.name}")
        ok += 1
    else:
        print(f"  FAIL  {caso_input.parent.name}: {result.stderr[:200]}")
        fail += 1

print(f"\nResultado: {ok} pass, {fail} fail")
sys.exit(0 if fail == 0 else 1)
