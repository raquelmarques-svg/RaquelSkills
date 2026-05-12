# Caso positivo 2 — Editar `mod4` para adicionar Quadro de Contato

## Input

Raquel: "edite mod4 para inserir o Quadro de Contato canônico após a qualificação e antes de Preliminares. Use o padrão visual da paleta navy/cream."

## Comportamento esperado

A skill-creator-am detecta operação de Edit em skill existente. Aplica pipeline §5 (Edit). Backup R3 obrigatório antes de tocar em qualquer byte.

### Fluxo

1. **Localização:**
   - Identifica `mod4` em `C:\RaquelSkills\skills\mod4\` (ou `/mnt/skills/user/mod4/` em sandbox)
   - Lê SKILL.md atual

2. **Backup R3 obrigatório:**
   ```bash
   python3 scripts/backup_skill.py C:\RaquelSkills\skills\mod4\SKILL.md
   # Output: _backups/SKILL.md/SKILL-20260511-150000.md
   ```
   Se backup falhar, abortar imediatamente.

3. **Análise da alteração proposta:**
   - Local de inserção: entre §[X] qualificação e §[Y] preliminares
   - Conteúdo: bloco visual Quadro de Contato com paleta navy #2C3B44 / cream #F5F1E8
   - Atualização do template_mod4.docx (asset) se aplicável

4. **Mostra diff proposto à Raquel:**

```diff
--- mod4/SKILL.md (atual)
+++ mod4/SKILL.md (proposto)
@@ §6 Qualificação ... @@
   [conteúdo qualificação completa]
   
+## §6-bis Quadro de Contato canônico
+
+Após qualificação e antes de Preliminares, inserir bloco visual com:
+- Telefone(s) com WhatsApp ativo
+- E-mail principal e secundário
+- Endereço para correspondência
+- Ponto de referência geográfico
+- Mesmas informações da advogada (escritório)
+
+Paleta: navy #2C3B44 (fundo) / cream #F5F1E8 (texto)
+Fonte: Cambria 11pt
+
+Fundamentação:
+- CPC art. 319, §§1-3 (endereço para citação)
+- Resolução CNJ 615/2025 (transparência processual)
+
+Implementação técnica em build_docx.py: ver linha 247.

   ## §7 Preliminares
   ...
```

5. **Aguarda confirmação explícita:**
   "Confirma a alteração? Backup já feito em `_backups/SKILL.md/SKILL-20260511-150000.md`."

6. **Aplica modificação após Raquel confirmar.**

7. **Atualizações automáticas:**
   - Atualiza `version`: 1.4.2 → 1.4.3 (PATCH, adição compatível)
   - Atualiza `verificado_em`: 2026-05-11
   - Atualiza `licoes_aplicadas`: adiciona L10 (letterhead VML) se ainda não listada

8. **Auditorias relevantes pós-edit:**
   - A1 Tamanho: mod4 passa de 675 para 712 linhas. ⚠️ VERMELHO (excede 500).
   - Alerta: "Esta edição empurra mod4 acima do limite. Sugiro Refactor obrigatório. Aceita Refactor agora ou após esta edição?"

9. **R10 (discordância útil):**
   - Aponta que o Quadro de Contato é candidato a `_compartilhados/templates/` porque outras skills C5 também o usarão. Sugere Extract paralelo.

10. **Log registrado:**
   ```yaml
   - timestamp: 2026-05-11T15:00:23
     operacao: editar
     skill: mod4
     backup: _backups/SKILL.md/SKILL-20260511-150000.md
     alteracoes: "adicionado §6-bis Quadro de Contato"
     reversivel_ate: 2026-06-10
     alertas: ["A1 vermelho - excede 500 linhas"]
     sugestoes: ["Refactor obrigatório", "Extract Quadro de Contato para _compartilhados/"]
   ```

## Output esperado

```
✅ mod4 editado
   Backup: _backups/SKILL.md/SKILL-20260511-150000.md
   Versão: 1.4.2 → 1.4.3
   Alterações: §6-bis Quadro de Contato adicionado

⚠️ ALERTAS:
   - A1: SKILL.md agora tem 712 linhas (excede 500). 
     Recomendação: Refactor obrigatório.
   
💡 SUGESTÃO (R10):
   - Quadro de Contato é candidato a _compartilhados/templates/.
     Outras skills C5 reusarão. Quer rodar Extract agora?

📝 Reversível até 2026-06-10 via:
   skill-creator-am undo mod4 2026-05-11T15:00:23
```

## Critério de aprovação

- Backup R3 feito antes de qualquer modificação
- Diff mostrado e confirmação aguardada
- Modificação aplicada apenas após "sim"
- version e verificado_em atualizados
- Auditorias rodadas e alertas reportados
- R10 sugeriu Extract de modo útil
- Log registrado com timestamp e janela de reversão

## Erros que invalidariam o teste

- Editar sem backup R3
- Não mostrar diff
- Modificar sem confirmação explícita
- Esquecer de atualizar version/verificado_em
- Não reportar A1 vermelho
- Silenciar sobre candidatura a `_compartilhados/`
- Log ausente
