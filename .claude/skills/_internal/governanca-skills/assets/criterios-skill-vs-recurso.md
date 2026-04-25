# Criterios skill versus recurso

Este asset orienta o modo `classificacao` da governanca-skills. Define os
testes para destinar um conteudo recebido a skill autonoma, modo interno
de skill existente, ou um dos sete tipos de recurso (asset, template,
schema, script, reference, example, config).

## Teste 1: o conteudo realiza transformacao propria?

Skill exige a triade fixa: input bruto ou intermediario, operacao
cognitiva ou tecnica, output utilizavel. Se o conteudo nao tiver os tres,
nao e skill.

```text
Tem input proprio?              Sim/Nao
Tem operacao propria?            Sim/Nao
Tem output proprio e utilizavel? Sim/Nao
```

Tres "sim" sao requisito necessario, nao suficiente, para virar skill.

## Teste 2: existe skill-pai com verbo dominante compativel?

Aplicar a regra hierarquica fixada como decisao do projeto:

```text
Se existe skill-pai com verbo dominante compativel
   e o conteudo descreve procedimento ou suboperacao
=> destino: modo interno da skill-pai
```

```text
Se nao existe skill-pai com verbo dominante compativel
   e o conteudo passa no Teste 1
=> destino: skill autonoma, via modo `criacao`
```

## Teste 3: o conteudo e criterio?

Se o conteudo descreve o que e bom, o que e ruim, como decidir, como
distinguir, como diagnosticar, ele e criterio. Criterio nao executa,
orienta. Destino:

```text
Aplica-se a uma skill so   => skill_alvo/assets/
Aplica-se a varias skills  => _shared/assets/
```

## Teste 4: o conteudo e forma de saida?

Se o conteudo descreve estrutura visual ou textual fixa que sera
preenchida, e template. Destino:

```text
Forma especifica da skill   => skill_alvo/templates/
Forma reutilizada           => _shared/templates/
```

Template nao raciocina. Se o material contiver decisao condicional,
nao e template; e procedimento e deve virar SKILL.md ou modo interno.

## Teste 5: o conteudo e validacao de campos obrigatorios?

Se o conteudo descreve campos esperados, tipos, enumeracoes, formatos
e regras de presenca, e schema. Destino:

```text
Schema de uma skill so      => skill_alvo/schemas/
Schema reutilizado          => _shared/schemas/
```

## Teste 6: o conteudo executa precisao mecanica?

Se o conteudo precisa de execucao deterministica (calcular, validar,
extrair, normalizar, converter, gerar arquivo), e script. Destino:

```text
Script de uma skill so      => skill_alvo/scripts/
Script reutilizado          => _shared/scripts/
```

Script nao decide tese. Script nao argumenta. Script nao interpreta norma.

## Teste 7: o conteudo e documentacao longa de metodo?

Se o conteudo e exposicao tecnica ou metodologica densa, sem ser
procedimento operacional, e reference. Destino:

```text
Reference de uma skill so   => skill_alvo/references/
Reference reutilizada       => _shared/references/
```

Reference nao deve estar dentro do SKILL.md. SKILL.md deve apontar para a
reference quando for necessario carregar a documentacao longa.

## Teste 8: o conteudo calibra qualidade?

Se o conteudo e exemplo de saida boa, saida ruim ou comparacao para
ajustar padrao, e example. Destino:

```text
Example de uma skill so     => skill_alvo/examples/
Example reutilizado         => _shared/examples/
```

## Teste 9: o conteudo e parametro?

Se o conteudo e enumeracao de valores, caminhos, limites, padroes ou
permissoes, e config. Destino:

```text
Config de uma skill so      => skill_alvo/config/
Config reutilizado          => _shared/config/
```

## Decisao final

Aplicar os testes em ordem. O primeiro teste positivo determina o destino,
salvo Teste 2, que tem precedencia sobre o Teste 1 quando aciona regra
hierarquica para modo interno.

Em caso de duvida persistente, marcar como SPEC_COM_LACUNAS e devolver a
usuaria com matriz de criterios e destinos possiveis. Esta e a postura
fixada para casos cinza, conforme decisao do projeto.

## Casos limites recorrentes

Material que parece skill mas e criterio: destino = asset.
Material que parece skill mas e forma: destino = template.
Material que parece skill mas e parametro: destino = config.
Material que parece skill mas e exemplo: destino = example.
Material que parece skill mas e calculo isolado: destino = script.
Material que parece reference mas e procedimento operacional: destino =
SKILL.md ou modo interno.
