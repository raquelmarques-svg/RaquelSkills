# Integracao com skill-creator-bridge

Documentacao tecnica longa sobre o ponto de juncao entre governanca-skills
e skill-creator-bridge. Esta reference nao deve ser carregada em execucao
normal; o SKILL.md aponta para ela quando houver duvida sobre o limite
de competencia entre as duas skills.

## Por que existem as duas

A criacao de skill envolve duas decisoes distintas:

```text
1. decisao arquitetural: o que esta capacidade deve ser?
   (skill, modo, asset, template, schema, script, reference, example,
   config?)
2. decisao fisica: quais arquivos existem, em que pastas, com que
   conteudo inicial?
```

Misturar essas decisoes recria o problema original do projeto. A
governanca-skills toma a decisao 1. A skill-creator-bridge executa a
decisao 2, sob autorizacao de file-safety.

## Fluxo canonico

```text
governanca-skills modo `criacao`
  └─ produz: SkillCreationSpec.yaml
     └─ entrega para: skill-creator-bridge
        └─ produz: plano-criacao-skill.md
           └─ entrega para: file-safety
              └─ autoriza ou bloqueia
                 └─ se autorizado, skill-creator-bridge gera estrutura
                    └─ governanca-skills audita o resultado em modo `auditoria`
                       └─ healthcheck-biblioteca valida integridade
                          └─ version-control prepara commit
```

## Contratos de saida e entrada

Saida da governanca-skills modo `criacao`:

```yaml
SkillCreationSpec:
  id:
  layer:
  family:
  dominant_verb:
  transformation: { input_state, operation, output_state }
  activation: { mode, aliases }
  input: { minimum, ideal }
  output: { primary, formats, status_enum }
  file_access: { permission, may_delete: false }
  manifest: { aliases, blocks, allowed_next }
  acceptance_criteria: []
```

Entrada da skill-creator-bridge: o documento acima, validado.
Sem validacao previa, a bridge deve emitir BLOQUEADO_SEM_SPEC.

## Bloqueios reciprocos

governanca-skills nao pode:

```text
- chamar skill-creator nativo diretamente;
- escrever arquivos da biblioteca;
- inventar nomes de arquivo.
```

skill-creator-bridge nao pode:

```text
- decidir verbo dominante;
- decidir camada;
- decidir entre skill, modo ou recurso;
- alterar SkillCreationSpec recebida.
```

Toda violacao desses bloqueios e sintoma de regressao do projeto a um
desenho centrado em prompts isolados.

## Casos especiais

### Bootstrap

A primeira execucao da biblioteca enfrenta paradoxo: a propria
governanca-skills precisa nascer sem que governanca-skills exista. A
solucao adotada e a usuaria mais Claude atuar como governanca-skills
provisoria, gerar a SkillCreationSpec da governanca-skills e auditar a
si proprios manualmente, ate a skill estar fisicamente instalada e
auto-auditavel via modo `auditar-self`.

### Auditoria pos-criacao

Apos a skill-creator-bridge gerar uma estrutura, governanca-skills entra
novamente, em modo `auditoria`, para checar se o que existe corresponde
ao que a SkillCreationSpec previa. Isso e auditoria leve, nao
substantiva. Auditoria substantiva pertence a healthcheck-biblioteca.

### Quando algo falhou no meio

Se file-safety bloquear escrita, o ciclo deve voltar a governanca-skills
em modo `auditoria` para identificar lacunas, em vez de ser empurrado a
forca via skill-creator nativo. Forcar gera arquivos sem governanca.

## Referencias internas

Asset relacionado: criterios-skill-vs-recurso.md.
Asset relacionado: regra-hierarquica-casos-cinza.md.
Asset relacionado: verbo-dominante.md.
Schema: skill-creation-spec.schema.json.
Script: validar_skill_creation_spec.py.
