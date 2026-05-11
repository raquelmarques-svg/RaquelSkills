# mod4 / reference 01 — Pipeline técnico

## Proibição fundamental

Nunca gerar o DOCX do zero via python-docx, docx-js ou qualquer serializador externo.

O template `ASSETS/template_mod4.docx` contém três elementos que não sobrevivem à serialização externa:

1. **Cabeçalho VML** — marca d'água A4 completo em três headers (`rId10`, `rId11`, `rId14`), via `w:pict` + `v:shape`, `position:absolute`, referenciando `media/image2.png` via `rId1` local. Qualquer serializador recria como DrawingML e quebra o layout.
2. **Assinatura cursiva** — `wp:inline` com `rId9` → `media/image1.png`, `cx=1900000 cy=1069000` EMU, centralizada. Reconstrução manual altera dimensões e posição.
3. **sectPr com 6 referências** — `rId10–rId15` + `<w:titlePage/>`. Perder qualquer referência elimina cabeçalho ou rodapé em alguma página.

O único caminho correto: ler o template via `zipfile`, substituir `word/document.xml`, copiar todos os demais itens sem filtrar.

## Script de montagem

```python
import zipfile, io, os
from pathlib import Path

TEMPLATE = Path("ASSETS/template_mod4.docx")  # localizado via find
OUTPUT   = Path("/mnt/user-data/outputs/<nome>.docx")

# 1. Ler template
with zipfile.ZipFile(TEMPLATE) as z:
    tpl_xml = z.read('word/document.xml').decode('utf-8')

# 2. Extrair sectPr (preserva as 6 referências + titlePage)
sp_start = tpl_xml.rfind('<w:sectPr')
sp_end   = tpl_xml.index('</w:sectPr>') + len('</w:sectPr>')
sect_pr  = tpl_xml[sp_start:sp_end]

# 3. Extrair bloco de assinatura (parágrafos finais do template)
# O script gerar_mod4.py faz isso via extract_signature_block()
# Nunca reconstruir manualmente — copiar do template

# 4. Montar novo document.xml (feito pelo gerar_mod4.py)
# CORPO = XML dos parágrafos gerados pelo script
# new_xml = NAMESPACE_DECL + <w:body> + CORPO + finais + sect_pr + </w:body> + </w:document>

# 5. Repacar ZIP substituindo apenas document.xml
buf = io.BytesIO()
with zipfile.ZipFile(TEMPLATE, 'r') as src, \
     zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as dst:
    for item in src.infolist():
        data = (new_xml.encode('utf-8')
                if item.filename == 'word/document.xml'
                else src.read(item.filename))
        dst.writestr(item, data)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(buf.getvalue())
print(f"OK — {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
```

## Estrutura do template preservada

```
template_mod4.docx
├── word/document.xml          ← SUBSTITUIR (script gera novo)
├── word/header1.xml           ← PRESERVAR (cabeçalho VML — páginas pares)
├── word/header2.xml           ← PRESERVAR (cabeçalho VML — padrão)
├── word/header3.xml           ← PRESERVAR (cabeçalho VML — primeira página)
├── word/footer1.xml           ← PRESERVAR (rodapé N/T — páginas pares)
├── word/footer2.xml           ← PRESERVAR (rodapé N/T — padrão)
├── word/footer3.xml           ← PRESERVAR (rodapé vazio — primeira página)
├── word/media/image1.png      ← PRESERVAR (assinatura cursiva — rId9)
├── word/media/image2.png      ← PRESERVAR (logo A4 — rId1 nos headers)
└── word/_rels/                ← PRESERVAR integralmente
```

## Parágrafos finais do template (não reconstruir)

```
[0]  {{DATA}}                              — Cambria 12pt, espaço after=40, esquerda
[1]  wp:inline rId9 (assinatura cursiva)   — centralizado, cx=1900000 cy=1069000 EMU
[2]  RAQUEL DE ALMEIDA MARQUES             — Cambria 12pt negrito, centralizado
[3]  OAB/SP 519.794                        — Cambria 11pt, centralizado
[4]  raquelmarques@almeidamarques.adv.br   — Cambria 11pt, centralizado
[5]  Almeida Marques Advocacia e Cons.     — Cambria 11pt itálico, centralizado
```

`extract_signature_block()` no script localiza o bloco pelo placeholder `{{DATA}}` e copia os 6 parágrafos integralmente, substituindo apenas o texto da data.

## sectPr canônico (extraído do template)

```xml
<w:sectPr>
  <w:headerReference w:type="even"    r:id="rId10"/>
  <w:headerReference w:type="default" r:id="rId11"/>
  <w:footerReference w:type="even"    r:id="rId12"/>
  <w:footerReference w:type="default" r:id="rId13"/>
  <w:headerReference w:type="first"   r:id="rId14"/>
  <w:footerReference w:type="first"   r:id="rId15"/>
  <w:titlePage/>
  <w:pgSz w:w="11906" w:h="16838"/>
  <w:pgMar w:top="1417" w:right="1701" w:bottom="1417" w:left="1701"
           w:header="2268" w:footer="709" w:gutter="0"/>
</w:sectPr>
```

## Erros críticos e correções

| Erro | Causa | Correção |
|---|---|---|
| Assinatura ausente | `word/document.xml.rels` não preservado | Copiar todos os itens do ZIP sem filtro |
| Cabeçalho em branco | Headers não preservados | Idem |
| Rodapé em todas as páginas | `<w:titlePage/>` ausente do sectPr | Extrair sectPr do template, nunca reescrever |
| Assinatura com dimensões erradas | Reconstrução manual em vez de cópia | Usar `extract_signature_block()` |
| `firstLine` zerado no corpo | `<w:pPr>` explícito sem `firstLine` herda zero | Sempre declarar `first_line=c('indent.corpo_primeira_linha')` |
