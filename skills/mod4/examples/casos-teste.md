# mod4 / examples

## Caso positivo 1 — Invocação completa com Status PRONTO

**Contexto:** Raquel acabou de rodar `revisao-previa-mod4` e o output contém `Status: PRONTO PARA mod4`.

**Input do usuário:**
```
mod4
```
*(com JSON de input já construído pela revisao-previa-mod4)*

**Comportamento esperado:**
1. Detecta `Status: PRONTO PARA mod4` na resposta anterior ✓
2. Valida campos obrigatórios do schema ✓
3. Confirma PRELIMINARES como primeira seção ✓
4. Localiza template via `find`
5. Executa `gerar_mod4.py`
6. Executa `validar_mod4.py` → `status: PRONTO`
7. Copia para `/mnt/user-data/outputs/peticao_maria_silva_20260511.docx`
8. Chama `present_files`

**Output esperado:** link de download do `.docx` sem texto adicional desnecessário.

---

## Caso positivo 2 — Tabela com colunas Tipo/Grau no input

**Contexto:** o input JSON contém uma tabela DAS PROVAS com 4 colunas (N°, Documento, Tipo, Grau).

**Comportamento esperado:**
O script detecta a tabela DAS PROVAS pelas 4 colunas e suprime silenciosamente Tipo e Grau, entregando tabela de 2 colunas (Documento + O que demonstra). Sem pergunta, sem aviso ao usuário — operação transparente.

**Output esperado:** `.docx` com tabela DAS PROVAS de 2 colunas. Relatório do validador menciona "supressão de colunas Tipo/Grau aplicada".

---

## Caso positivo 3 — Input sem PRELIMINARES declaradas

**Contexto:** o JSON de input tem `secoes[]` começando com "DOS FATOS", sem seção de PRELIMINARES.

**Comportamento esperado:**
1. §0-Autopercepção detecta ausência de PRELIMINARES como primeira seção
2. Sinaliza: "PRELIMINARES ausentes — inserindo seção mínima automaticamente"
3. Insere seção com representação processual e endereço para intimações
4. Prossegue com a geração normalmente

**Output esperado:** `.docx` com PRELIMINARES como primeira seção, seguida das seções de mérito originais.

---

## Caso negativo 1 — Invocação sem Status PRONTO

**Contexto:** Raquel digita `mod4` diretamente, sem ter rodado `revisao-previa-mod4`.

**Comportamento esperado:**
1. §0-Autopercepção verifica: `Status: PRONTO PARA mod4` ausente na resposta anterior
2. NÃO gera o `.docx`
3. Responde: "O input não passou por `revisao-previa-mod4`. Execute essa skill primeiro e retorne com o output contendo `Status: PRONTO PARA mod4`."

**Output esperado:** nenhum arquivo gerado. Instrução clara de qual passo executar antes.

---

## Caso negativo 2 — Tipo de caixa proibido no input

**Contexto:** o JSON de input contém `{"tipo": "caixa_tese", "texto": "..."}`.

**Comportamento esperado:**
1. Script detecta tipo proibido durante validação do input
2. NÃO gera o `.docx`
3. R10 (discordância útil): reporta "Tipo `caixa_tese` não é suportado nesta versão. Substitua por `caixa_destaque`. Os tipos proibidos são: caixa_vicio, caixa_tese, caixa_advertencia, caixa_ressalva."
4. Aguarda input corrigido

**Output esperado:** nenhum arquivo gerado. Mensagem com o tipo detectado, o substituto correto e os tipos proibidos listados.
