---
name: governanca-skills
description: >
  Porta de entrada da Biblioteca Raquel Skills V6.5.2. Use sempre que houver
  pedido de criar skill, transformar conteudo em skill, auditar skill
  existente, classificar conteudo entre skill, modo interno, asset,
  template, schema, script, reference, example ou config, dividir skill
  inchada ou fundir skills sobrepostas. Use mesmo quando o pedido vier
  fraseado como "skill-creator", porque skill-creator nativo so pode ser
  acionado depois de governanca-skills emitir SkillCreationSpec aprovada.
  Esta skill nao escreve arquivos da biblioteca, nao altera _manifest e
  nao revisa merito juridico.
version: 6.5.2
layer: internal
family: governanca
activation: explicit
permission_profile: read_only
---

# Finalidade

Decidir o que vira skill, modo interno, asset, template, schema, script,
reference, example ou config, antes de qualquer criacao fisica de arquivo.
Especificar a SkillCreationSpec exigida pelo documento 6, item 5.2.
Auditar skills existentes em nivel leve, checando apenas presenca de
campos minimos, sem julgar substancia. Recomendar divisao quando ha mais
de um verbo dominante. Recomendar fusao quando ha verbo dominante
coincidente e outputs sobrepostos. Auto-auditar-se em nivel leve, sem
duplicar a competencia da healthcheck-biblioteca.

# Transformacao

```text
input bruto: pedido de criar, auditar, classificar, dividir ou fundir
operacao: classificar, especificar e validar contra criterios da V6.5.2
output: SkillCreationSpec aprovada, ou relatorio de auditoria leve, ou
ficha de classificacao, ou plano de divisao, ou plano de fusao, com
status fechado e proxima skill permitida.
```

# Gatilhos

Modo `criacao` ativa quando o input contiver: "crie uma skill",
"transforme isto em skill", "criar skill", "skill-creator", ou descricao
de uma funcao para a qual nao existe skill ainda.

Modo `auditoria` ativa quando o input contiver: "audite a skill",
"audite esta skill", ou referencia a skill existente com pedido de
verificacao.

Modo `classificacao` ativa quando o input contiver: "isto vira skill",
"skill ou modo interno", "classifique este conteudo", ou material
indefinido sem pedido explicito de criacao.

Modo `divisao` ativa quando o input contiver: "divida esta skill",
"esta skill esta inchada", ou diagnostico de skill com mais de um verbo
dominante.

Modo `fusao` ativa quando o input contiver: "funda estas skills",
"estas skills se sobrepoem", ou diagnostico de skills concorrentes.

Modo `auditar-self` ativa quando o input contiver: "audite governanca-skills",
"auto-auditoria da governanca", ou pedido reflexivo equivalente.

# Bloqueios

Esta skill nao escreve arquivos da biblioteca. Esta skill nao aciona
skill-creator nativo diretamente. Esta skill nao altera `_manifest` sem
encaminhar a manifest-manager. Esta skill nao executa migracao sem
encaminhar a migration-manager. Esta skill nao revisa merito juridico.
Esta skill nao redige peca. Esta skill nao gera docx. Esta skill nao
realiza auditoria substantiva, profunda ou de qualidade redacional.

Em caso de pedido bloqueado, emitir status `REJEITADA_DUPLICIDADE` ou
redirecionar para a skill competente.

# Entrada minima

Para todos os modos:

```text
- descricao da funcao ou skill alvo
- tipo de pedido (criacao | auditoria | classificacao | divisao | fusao)
```

Sem esses dois campos, emitir `SPEC_COM_LACUNAS` e pedir complemento.

# Entrada ideal

```text
- rascunho textual da skill ou da funcao
- lista de recursos ja existentes na biblioteca
- exemplos de input e output esperados
- referencia a skills relacionadas
- registros de uso anteriores quando houver
```

Entradas parciais sao aceitas; lacunas devem ser marcadas no output.

# Modos internos

## Modo `criacao`

Procedimento operacional obrigatorio:

1. Confirmar que nao existe skill com mesmo verbo dominante e mesmo output
   primario. Carregar `assets/verbo-dominante.md` e
   `config/palavras-chave-verbo-dominante.yaml`.
2. Aplicar a regra hierarquica de casos cinza (ver
   `assets/regra-hierarquica-casos-cinza.md`): se existe skill-pai com
   verbo dominante compativel, recomendar virar modo interno; caso
   contrario, prosseguir como skill autonoma.
3. Carregar `templates/skill-creation-spec.yaml`.
4. Preencher os campos obrigatorios listados no schema do documento 6
   item 5.2.
5. Validar a spec preenchida com `scripts/validar_skill_creation_spec.py`.
6. Se invalida, emitir `SPEC_COM_LACUNAS` e listar campos faltantes.
7. Se valida, emitir `SPEC_APROVADA`.
8. Indicar como proxima skill: skill-creator-bridge, precedido por
   migration-manager se houver conteudo antigo a reaproveitar.

Output do modo: `skill-creation-spec.yaml` e ficha previa de classificacao.

Status possiveis: SPEC_APROVADA, SPEC_COM_LACUNAS, MIGRAR_RECURSOS,
VIRAR_MODO_INTERNO, VIRAR_RECURSO_SHARED, REJEITADA_DUPLICIDADE.

## Modo `auditoria`

Auditoria leve. Nao avalia substancia, nao julga qualidade redacional,
nao verifica correcao juridica. Checa apenas presenca estrutural.

Procedimento:

1. Carregar `schemas/skill-audit-leve.schema.json`.
2. Carregar `config/criterios-auditoria-leve.yaml`.
3. Para a skill alvo, conferir presenca de:
   ```text
   SKILL.md
   verbo dominante declarado
   transformation com input_state, operation, output_state
   activation com mode e aliases
   input minimo declarado
   output principal declarado
   status_enum declarado
   bloqueios declarados
   allowed_next declarado
   ```
4. Rodar `scripts/auditar_skill_leve.py`.
5. Emitir `relatorio-auditoria-skill.md` apontando apenas o que falta.
6. Para auditoria de qualidade, indicar healthcheck-biblioteca como proxima
   skill, sem executar a auditoria profunda aqui.

Status possiveis: AUDITORIA_OK, AUDITORIA_COM_ALERTAS, AUDITORIA_REPROVADA.

## Modo `classificacao`

Aplicar a regra hierarquica de casos cinza. O conteudo recebido pode
ser destinado a:

```text
1. skill autonoma
2. modo interno de skill existente
3. asset transversal em _shared/assets
4. template em skill especifica ou em _shared/templates
5. schema em skill especifica ou em _shared/schemas
6. script em skill especifica ou em _shared/scripts
7. reference em skill especifica ou em _shared/references
8. example em skill especifica ou em _shared/examples
9. config em skill especifica ou em _shared/config
```

Procedimento:

1. Identificar verbo dominante do conteudo.
2. Verificar se existe skill com verbo compativel.
3. Se existir e o conteudo for procedimento, recomendar modo interno.
4. Se existir e o conteudo for criterio, recomendar asset.
5. Se existir e o conteudo for forma de saida, recomendar template.
6. Se existir e o conteudo for validacao de campos, recomendar schema.
7. Se existir e o conteudo for calculo, recomendar script.
8. Se existir e o conteudo for documentacao longa, recomendar reference.
9. Se existir e o conteudo for calibracao de qualidade, recomendar example.
10. Se existir e o conteudo for parametro, recomendar config.
11. Se nao existir skill compativel, recomendar criacao via modo `criacao`.

Output: `ficha-classificacao.md` com destino e justificativa.

## Modo `divisao`

Procedimento:

1. Rodar `scripts/detectar_verbo_multiplo.py` sobre o SKILL.md alvo.
2. Se houver mais de um verbo dominante com procedimento heterogeneo,
   recomendar divisao em duas ou mais skills.
3. Para cada skill resultante, gerar uma SkillCreationSpec parcial.
4. Indicar como proxima skill: governanca-skills modo `criacao` para
   cada nova skill resultante; migration-manager para mover recursos.

Output: `plano-divisao-skill.md`.

Status: DIVISAO_RECOMENDADA, AUDITORIA_OK quando nao for caso de divisao.

## Modo `fusao`

Procedimento:

1. Comparar verbos dominantes das skills alvo.
2. Se forem coincidentes e os outputs primarios se sobrepuserem,
   recomendar fusao.
3. Indicar qual skill absorve a outra, qual vira modo interno e quais
   recursos migram para `_shared` ou para a skill absorvedora.
4. Indicar como proxima skill: migration-manager.

Output: `plano-fusao-skills.md`.

Status: FUSAO_RECOMENDADA, AUDITORIA_OK quando nao for caso de fusao.

## Modo `auditar-self`

Auto-auditoria leve da propria governanca-skills. Nao substitui
healthcheck-biblioteca. Diferenca de competencia:

```text
auditar-self: confere presenca de arquivos e campos minimos da propria
governanca-skills, no nivel estrutural mais raso.

healthcheck-biblioteca: confere integridade da biblioteca inteira,
inclusive coerencia de _manifest, ausencia de orfaos, conformidade da
politica de arquivos e relacao entre skills.
```

Procedimento:

1. Rodar `scripts/self_audit.py`.
2. Conferir que SKILL.md existe e tem cinco modos mais auditar-self.
3. Conferir que assets, templates, schemas, scripts, references, examples
   e config existem.
4. Conferir que a SkillCreationSpec da propria skill esta presente.
5. Emitir `relatorio-self-audit.md`.
6. Encerrar indicando healthcheck-biblioteca como proxima etapa para
   auditoria de integridade da biblioteca.

Status: SELF_AUDIT_OK, SELF_AUDIT_COM_ALERTAS.

# Procedimento operacional obrigatorio (qualquer modo)

1. Identificar o tipo de pedido. Se ambiguo, perguntar a usuaria antes
   de prosseguir.
2. Selecionar o modo correspondente.
3. Carregar apenas os recursos necessarios ao modo. Lazy loading.
4. Executar o procedimento do modo.
5. Validar o output com o schema correspondente.
6. Emitir status fechado.
7. Indicar proxima skill permitida ou lacuna impeditiva.
8. Nao escrever nenhum arquivo na biblioteca. Outputs ficam em pasta
   propria de saida, nunca dentro de `.claude/skills/` salvo via
   skill-creator-bridge.

# Outputs

Saida primaria depende do modo:

```text
criacao        skill-creation-spec.yaml
auditoria      relatorio-auditoria-skill.md
classificacao  ficha-classificacao.md
divisao        plano-divisao-skill.md
fusao          plano-fusao-skills.md
auditar-self   relatorio-self-audit.md
```

Toda saida termina com bloco padronizado:

```text
Status:
Output produzido:
Lacunas:
Proxima acao:
Proxima skill permitida:
Bloqueios:
```

# Limites

Nao escreve arquivos da biblioteca. Nao aciona skill-creator nativo
diretamente. Nao altera `_manifest`. Nao executa migracao. Nao revisa
merito. Nao redige peca. Nao gera docx. Nao faz auditoria profunda.
Nao decide questoes substantivas alheias a estrutura.

# Erros a evitar

1. Acionar skill-creator antes de spec aprovada.
2. Permitir caso cinza sem aplicar a regra hierarquica.
3. Inflar SKILL.md com teoria que pertence a `assets` ou `references`.
4. Misturar auditoria leve com auditoria substantiva.
5. Duplicar logica de healthcheck-biblioteca em auditar-self.
6. Escrever em `.claude/skills/` por conta propria.
7. Aceitar SkillCreationSpec sem campos minimos.
8. Decidir o que vira skill com base apenas em proximidade semantica.
9. Criar skill nova quando o conteudo couber em modo interno de
   skill-pai existente.
10. Encerrar execucao sem status, sem proxima acao e sem indicar
    proxima skill.
