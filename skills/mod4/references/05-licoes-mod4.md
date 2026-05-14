# references/05-licoes-mod4.md
# mod4 — Lições técnicas de geração de DOCX via zipfile
# Versão: 4.3.0 | Data: 2026-05-14

## LD5 — Zipfile direto é o método padrão e permanente

### Contexto

A versão v4.2.0 documentava dois métodos de geração: `gerar_mod4.py` (primário)
e zipfile direto (fallback quando o script estivesse ausente). A produção da
petição de redesprotocolamento do caso Beatriz Rodrigues (14/05/2026) comprovou
que o script intermediário é uma camada desnecessária — o zipfile direto preserva
100% dos elementos gráficos do template e produz resultado visualmente superior.

### Regra

**Zipfile direto sobre `ASSETS/template_mod4.docx` é o único método válido.**
`gerar_mod4.py` e `validar_mod4.py` estão descontinuados — não devem ser usados
mesmo que estejam presentes na instalação.

### Padrão de código

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile, io, shutil

def gerar_docx(template_path: str, substituicoes: dict, dest_path: str) -> None:
    """
    Aplica substituicoes em word/document.xml e remonta o DOCX preservando
    todos os demais arquivos do template intactos (VML, media, styles, etc.).

    substituicoes: dict no formato {'>placeholder<': '>valor<'}
    """
    shutil.copy2(template_path, '/tmp/mod4_work.docx')

    with zipfile.ZipFile('/tmp/mod4_work.docx', 'r') as zin:
        all_files = {name: zin.read(name) for name in zin.namelist()}

    doc = all_files['word/document.xml'].decode('utf-8')

    for old, new in substituicoes.items():
        doc = doc.replace(old, new)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for fname, data in all_files.items():
            if fname == 'word/document.xml':
                zout.writestr(fname, doc.encode('utf-8'))
            else:
                zout.writestr(fname, data)

    with open(dest_path, 'wb') as f:
        f.write(buf.getvalue())
```

### Por que não usar python-docx nem serialização externa

O `template_mod4.docx` contém:
- Cabeçalho VML (Word Drawing Markup Language) com o logotipo vetorial
- Imagem de assinatura cursiva inserida via `<v:imagedata>`
- Estilos calibrados (`Ttulo1`, `Ttulo2`, `PargrafodaLista`, `Normal`)
- Numeração configurada em `word/numbering.xml`

Qualquer serialização externa (python-docx, docxcompose, etc.) descarta o VML
e reestrutura o ZIP com perda dos elementos gráficos. O zipfile direto preserva
todos esses componentes porque apenas substitui strings em `word/document.xml`
e remonta o arquivo sem modificar os demais membros do ZIP.

---

## LD6 — Placeholders intermediários em substituições encadeadas

### Problema

Substituição sequencial de strings que formam cadeia (A→B, B→C, C→D) produz
dupla substituição: o texto recém-inserido "B" é reprocessado na etapa seguinte
que busca por "B".

```python
# ERRADO — cadeia sem proteção
doc = doc.replace('>Fevereiro/2026<', '>Marco/2026<')   # fev -> mar
doc = doc.replace('>Marco/2026<',     '>Abril/2026<')   # mar -> abr  (converte inclusive o que acabou de chegar de fev!)
doc = doc.replace('>Abril/2026<',     '>Maio/2026<')    # abr -> mai  (converte inclusive o que chegou de mar!)
# Resultado: fev foi para mar, que foi para abr, que foi para mai — ERRADO
```

### Solução

Tokens intermediários únicos e não-colisionáveis na primeira passagem,
resolução dos valores definitivos na segunda.

```python
# CORRETO — dois passos com tokens
# Passo 1: proteger origens com tokens unicos
doc = doc.replace('>Fevereiro/2026<', '>__MESA__<')
doc = doc.replace('>Marco/2026<',     '>__MESB__<')
doc = doc.replace('>Abril/2026<',     '>__MESC__<')

# Passo 2: resolver tokens com valores definitivos
doc = doc.replace('>__MESA__<',       '>Marco/2026<')
doc = doc.replace('>__MESB__<',       '>Abril/2026<')
doc = doc.replace('>__MESC__<',       '>Maio/2026<')
```

Otimização quando o último elo da cadeia não é origem de nenhum outro:
o valor definitivo pode ser aplicado diretamente no passo 1, poupando um token.

```python
doc = doc.replace('>Fevereiro/2026<', '>__MESA__<')
doc = doc.replace('>Marco/2026<',     '>__MESB__<')
doc = doc.replace('>Abril/2026<',     '>Maio/2026<')   # seguro: Maio nao e origem
doc = doc.replace('>__MESB__<',       '>Abril/2026<')
doc = doc.replace('>__MESA__<',       '>Marco/2026<')
```

### Convenção de nomeação de tokens

- Formato: `>__NOME_EM_MAIUSCULAS__<`
- Underscores duplos garantem que o token não apareça em nenhum XML válido
- Nome deve ser mnemônico: `__DATA_A__`, `__MESA__`, `__VALOR_TOT__`

### Aplicação a datas (exemplo real — redesprotocolamento Beatriz Rodrigues)

```python
# Triplet textual no corpo (substituição simples — sem conflito)
doc = doc.replace(
    '10/02/2026, 10/03/2026 e 10/04/2026',
    '10/03/2026, 10/04/2026 e 10/05/2026'
)

# Células de tabela (cadeia — requer tokens)
doc = doc.replace('>10/02/2026<', '>__DATA_A__<')
doc = doc.replace('>10/03/2026<', '>__DATA_B__<')
doc = doc.replace('>10/04/2026<', '>10/05/2026<')   # ultimo elo — seguro
doc = doc.replace('>__DATA_B__<', '>10/04/2026<')
doc = doc.replace('>__DATA_A__<', '>10/03/2026<')
```

---

## LD7 — Padrão `>texto<` como alvo de busca em document.xml

### Problema

O Word gera elementos `<w:t>` em duas formas:

```xml
<!-- Forma 1: sem atributo — texto simples -->
<w:t>Março/2026</w:t>

<!-- Forma 2: com xml:space="preserve" — textos com espaços adjacentes -->
<w:t xml:space="preserve">Março/2026</w:t>
```

A busca pela tag completa (`<w:t>Março/2026</w:t>`) casa apenas com a Forma 1
e falha silenciosamente na Forma 2. O documento continua válido, mas o
placeholder não é substituído — erro invisível que só aparece ao abrir o DOCX.

### Solução

Usar o delimitador `>texto<` que casa com ambas as formas,
independentemente dos atributos intermediários do elemento.

```python
# CORRETO — casa com Forma 1 e Forma 2
doc = doc.replace('>Março/2026<', '>Abril/2026<')

# ERRADO — falha silenciosamente na Forma 2
doc = doc.replace('<w:t>Março/2026</w:t>', '<w:t>Abril/2026</w:t>')
```

### Alcance e limitações

O padrão `>texto<` captura qualquer elemento que contenha apenas `texto`
entre `>` e `<`, incluindo `<w:t>`, `<w:instrText>` e outros. Isso é
desejável para substituições de conteúdo textual.

O padrão não deve ser usado quando o alvo de busca é um elemento com
conteúdo misto ou quando é necessário distinguir o tipo de elemento.
Nesse caso, usar regex com captura de atributos.

### Combinação com LD6

LD7 e LD6 são complementares: LD7 define o formato do padrão de busca;
LD6 define a ordem de aplicação quando as substituições formam cadeia.
Toda substituição em cadeia deve usar LD7 no formato dos tokens.

```python
# Token correto: >__TOKEN__< (nao <w:t>__TOKEN__</w:t>)
doc = doc.replace('>Fevereiro/2026<', '>__MESA__<')   # LD7: usa >texto<
doc = doc.replace('>__MESA__<',       '>Marco/2026<') # LD7: resolve token
```
