#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executa casos de teste do widget-visual."""
import json, subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "gerar_widget.py"
CASOS  = sorted((Path(__file__).parent).glob("caso-*/input.json"))
ok = 0
fail = 0

for caso_input in CASOS:
    caso_dir = caso_input.parent
    inp = json.loads(caso_input.read_text(encoding="utf-8"))
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--tipo",    inp["tipo"],
         "--titulo",  inp["titulo"],
         "--dados",   json.dumps(inp["dados"]),
         "--output",  "/tmp/widget_test",
         "--prefixo", inp.get("prefixo","teste")],
        capture_output=True, text=True
    )
    if result.returncode == 0 and "OK" in result.stdout:
        print(f"  PASS  {caso_dir.name}")
        ok += 1
    else:
        print(f"  FAIL  {caso_dir.name}")
        print(f"        stdout: {result.stdout[:200]}")
        print(f"        stderr: {result.stderr[:200]}")
        fail += 1

print(f"\nResultado: {ok} pass, {fail} fail")
sys.exit(0 if fail == 0 else 1)
