# casos-teste — recorte-pdf

## CT-01 — Página inteira de decisão

**Entrada:**
- PDF: `processo-joao-silva.pdf`
- Página: 15 (despacho de deferimento)
- Região: inteira
- DPI: 150

**Comando gerado:**
```bash
python3 scripts/recortar_pdf.py \
  --pdf processo-joao-silva.pdf \
  --pages 15 \
  --region inteira \
  --dpi 150 \
  --output C:/RaquelSkills/recortes \
  --prefix joao-silva
```

**Output esperado:**
- `joao-silva-p015-inteira.png` (aprox. 1240×1753px em A4 150DPI)

---

## CT-02 — Intervalo de páginas (laudo pericial pp. 3-7)

**Entrada:**
- PDF: `laudo-pericial-ntep.pdf`
- Páginas: 3-7
- Região: inteira

**Output esperado:** 5 PNGs numerados p003 a p007.

---

## CT-03 — Metade superior (cabeçalho com autuação)

**Entrada:**
- Página: 1, região: superior

**Uso:** extrair autuação do processo para inserir no rodapé de petição.

---

## CT-04 — PDF protegido por senha

**Output esperado:**
```
recorte-pdf: ERRO
motivo: PDF protegido por senha
ação_requerida: fornecer senha ou versão sem proteção
```

---

## CT-05 — Página fora do intervalo

**Entrada:** pages=150, PDF com 80 páginas.

**Output esperado:**
```
ERRO: nenhuma página válida no intervalo '150' (total: 80)
```
