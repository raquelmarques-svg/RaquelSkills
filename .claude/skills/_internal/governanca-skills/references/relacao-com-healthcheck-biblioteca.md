# Relacao com healthcheck-biblioteca

Documentacao tecnica sobre a fronteira de competencia entre o modo
`auditar-self` da governanca-skills e a skill interna
healthcheck-biblioteca. Esta reference resolve a duvida de bootstrap
recursivo registrada como decisao do projeto: auto-auditoria embutida
e auditoria externalizada coexistem com responsabilidades distintas.

## Por que duas auditorias

A governanca-skills pode auditar-se. A healthcheck-biblioteca audita a
biblioteca inteira. Sem essa distincao, ou a governanca-skills nunca se
audita (e a biblioteca tem ponto cego), ou a governanca-skills duplica
a logica da healthcheck (e a biblioteca tem competencia sobreposta).

A solucao adotada e:

```text
auditar-self           confere apenas a propria estrutura interna,
                       em nivel raso, sem julgar a biblioteca em volta.

healthcheck-biblioteca confere a biblioteca como sistema, em nivel
                       profundo, inclusive a propria governanca-skills
                       e a coerencia entre todas as skills.
```

Auditar-self previne degradacao silenciosa da governanca-skills entre
healthchecks completos. Healthcheck-biblioteca previne ilusao de saude
quando cada skill se auto-aprova mas a biblioteca esta incoerente.

## Tabela de competencia

| Aspecto | auditar-self | healthcheck-biblioteca |
|---------|--------------|------------------------|
| Objeto | governanca-skills | biblioteca inteira |
| Nivel | raso, estrutural | profundo, sistemico |
| Frequencia | a qualquer execucao | em marcos e antes de commits |
| Output | relatorio-self-audit.md | relatorio de saude da biblioteca |
| Decide alteracao? | nao | nao |
| Pode bloquear commit? | nao | sim, via version-control |
| Detecta orfaos? | nao | sim |
| Detecta duplicidade entre skills? | nao | sim |
| Verifica _manifest? | nao | sim |
| Verifica politica de arquivos? | nao | sim |
| Verifica fluxo de chamadas? | nao | sim |
| Verifica presenca de SKILL.md? | sim, na propria | sim, em todas |
| Verifica presenca de pastas obrigatorias? | sim, nas proprias | sim, em todas |
| Verifica modos declarados em SKILL.md? | sim, na propria | sim, em todas |
| Verifica recursos citados que nao existem? | parcial | sim |
| Verifica versao? | nao | sim |
| Verifica relacao entre skills? | nao | sim |

## O que auditar-self faz, em detalhe

```text
1. confere existencia de SKILL.md, README.md, SKILL_CREATION_SPEC.yaml;
2. confere existencia de assets, templates, schemas, scripts, references,
   examples e config;
3. confere se os cinco modos mais auditar-self estao declarados em SKILL.md;
4. confere presenca dos templates citados no SKILL.md;
5. confere presenca dos schemas citados no SKILL.md;
6. confere presenca dos scripts citados no SKILL.md;
7. emite relatorio-self-audit.md com status SELF_AUDIT_OK ou
   SELF_AUDIT_COM_ALERTAS.
```

Auditar-self nao aciona nenhum recurso externo. Nao consulta `_manifest`.
Nao executa cross-check com outras skills. Nao verifica conformidade da
SkillCreationSpec contra o schema (essa verificacao pertence ao modo
`criacao` da governanca-skills e e feita uma vez na criacao, nao a cada
self-audit).

## O que healthcheck-biblioteca faz, em detalhe

```text
1. lista todas as skills da biblioteca;
2. confere existencia, presenca de pastas e SKILL.md em cada uma;
3. confere coerencia entre `_manifest/biblioteca.yaml` e o sistema de
   arquivos;
4. detecta orfaos (recurso citado em SKILL.md que nao existe; arquivo
   no disco que nao e citado por nenhuma skill);
5. detecta duplicidade entre skills (verbos dominantes coincidentes,
   outputs sobrepostos);
6. verifica `_manifest/aliases.yaml` para conflitos;
7. verifica `_manifest/precedencia.yaml` para regras contraditorias;
8. verifica `_manifest/bloqueios.yaml` para coerencia recíproca;
9. verifica `_manifest/chamadas-permitidas.yaml` para ciclos;
10. verifica conformidade da politica de arquivos
    (`_shared/config/permissoes-arquivo.yaml`);
11. verifica que nenhuma skill viola o bloqueio de exclusao definitiva
    e de sobrescrita;
12. verifica versao da biblioteca contra `_manifest/biblioteca.yaml`;
13. emite relatorio com status SAUDAVEL, FUNCIONAL_COM_ALERTAS,
    INSTAVEL ou CRITICA.
```

Esses passos exigem leitura ampla, comparacao cruzada e logica de grafo.
Por isso, nao cabem dentro do auditar-self.

## Quando chamar qual

```text
auditar-self
- apos qualquer alteracao na propria governanca-skills;
- antes de marcos da onda 0;
- como sanity check rapido.

healthcheck-biblioteca
- apos criacao de qualquer skill;
- antes de commits relevantes;
- antes de fechar uma onda de implementacao;
- antes de promover skill de optional para nuclear;
- ao detectar comportamento errático de ativacao.
```

## Encaminhamento canonico

```text
auditar-self
  └─ se SELF_AUDIT_COM_ALERTAS, listar lacunas
     └─ proxima skill: governanca-skills modo `auditoria` para
        verificar a propria estrutura em maior detalhe
        └─ proxima skill: healthcheck-biblioteca para auditar
           a biblioteca inteira
```

```text
healthcheck-biblioteca
  └─ se SAUDAVEL, liberar version-control
  └─ se FUNCIONAL_COM_ALERTAS, listar pendencias
  └─ se INSTAVEL, bloquear commit e exigir correcao
  └─ se CRITICA, bloquear toda alteracao ate restauracao
```

## Risco de duplicacao

Sintomas de que auditar-self esta invadindo escopo da healthcheck:

```text
- auditar-self esta lendo `_manifest`;
- auditar-self esta listando outras skills;
- auditar-self esta detectando duplicidade entre skills;
- auditar-self esta emitindo INSTAVEL ou CRITICA;
- auditar-self esta bloqueando commit.
```

Em qualquer desses sintomas, retornar a auditar-self ao escopo raso e
mover a logica para healthcheck-biblioteca.

## Risco simetrico

Sintomas de que healthcheck-biblioteca esta delegando demais a
auditar-self:

```text
- healthcheck pula a verificacao da governanca-skills supondo que o
  self-audit ja basta;
- healthcheck ignora SKILL.md da governanca-skills.
```

Healthcheck audita todas as skills, inclusive a governanca-skills.
Auditar-self complementa, nao substitui.

## Limite

Esta reference descreve a fronteira. Nao a executa. A execucao depende
de scripts/self_audit.py para auditar-self, e depende de scripts da
healthcheck-biblioteca, que sera criada em onda subsequente.
