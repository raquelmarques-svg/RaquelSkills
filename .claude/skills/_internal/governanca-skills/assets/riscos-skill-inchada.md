# Riscos de skill inchada

Skill inchada e aquela que cresceu alem do escopo de seu verbo dominante.
Ela acumula procedimentos heterogeneos, outputs de naturezas distintas,
gatilhos concorrentes e bloqueios contra si mesma.

## Sintomas estruturais

```text
SKILL.md acima de 500 linhas;
mais de cinco modos internos;
mais de um Procedimento operacional obrigatorio;
outputs primarios de tipos distintos;
gatilhos cobrindo familias semanticas distintas;
bloqueios internos descrevendo "este modo nao pode invadir aquele";
listas de aliases enormes, com vocabulario disputado por outras skills.
```

## Sintomas operacionais

```text
a skill responde com latencia perceptivel;
respostas variam conforme o leitor humano interpreta o input;
duas execucoes do mesmo input geram outputs estruturalmente diferentes;
o output final precisa ser editado para virar entregavel.
```

## Sintomas arquiteturais

```text
a skill repete conteudo presente em _shared;
a skill duplica scripts de outra skill;
a skill consulta arquivos de varias outras skills durante execucao;
a skill nao indica proxima skill, porque "ja faz tudo".
```

## Tratamento

Modo `divisao`. Procedimento:

1. Listar todos os verbos identificados no SKILL.md.
2. Para cada verbo, verificar se ha procedimento proprio, output proprio
   e bloqueios proprios.
3. Cada bloco com triade completa vira candidato a skill autonoma.
4. Procedimentos que sobram, sem triade, viram modo interno da skill
   resultante mais proxima.
5. Recursos compartilhados entre os blocos migram para `_shared` via
   migration-manager.
6. Atualizar `_manifest` via manifest-manager para refletir a divisao.

## Risco de divisao excessiva

Dividir demais cria fragmentos sem sentido. Sintomas:

```text
skills com SKILL.md menor que 30 linhas;
skills cujos gatilhos exigem outra skill para fazer sentido;
skills sem output primario claro;
skills cujo unico papel e chamar outra skill.
```

Nestes casos, o conteudo provavelmente deveria ser modo interno, asset,
template, schema ou config, nao skill autonoma.

## Limite

Divisao recomendada por governanca-skills nao executa, por si, a divisao.
Execucao depende de manifest-manager (atualizar aliases, precedencia,
bloqueios), migration-manager (preservar conteudo redistribuido),
file-safety (autorizar criacao e edicao) e skill-creator-bridge (montar
estrutura fisica).
