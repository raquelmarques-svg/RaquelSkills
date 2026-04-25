# Regra hierarquica para casos cinza

Decisao fixada para o projeto: casos em que um conteudo poderia ser skill
autonoma ou poderia ser modo interno de skill existente serao resolvidos
por regra hierarquica. Se existe skill-pai com verbo dominante
compativel, o conteudo vira modo interno. Se nao existe, vira skill
autonoma.

Esta regra evita dois erros simetricos:

```text
Erro 1: criar skill nova quando ja ha skill-pai apta a abrigar a funcao
        como modo interno. Resultado: ativacao concorrente, sobreposicao,
        manutencao difícil.

Erro 2: empurrar para modo interno funcao que tem verbo dominante
        proprio e produz output proprio. Resultado: skill-pai inchada e
        violacao do principio de um verbo dominante por skill.
```

## Procedimento

1. Identificar verbo dominante do conteudo recebido.
2. Procurar skill existente com verbo dominante igual ou imediatamente
   adjacente.
3. Se houver skill-pai compativel:
   3a. O conteudo descreve uma suboperacao da skill-pai? Se sim, e modo
       interno.
   3b. O conteudo tem output primario distinto da skill-pai? Se sim,
       reavaliar; pode ser skill autonoma mesmo havendo skill-pai
       proxima.
   3c. O conteudo introduz risco operacional novo (acesso a arquivo,
       integracao externa, calculo financeiro)? Se sim, ponderar skill
       autonoma para manter bloqueios proprios.
4. Se nao houver skill-pai compativel:
   4a. Aplicar os testes do asset criterios-skill-vs-recurso.md.
   4b. Se passar nos tres testes da triade input-operacao-output, e
       skill autonoma.
   4c. Se nao passar, e recurso.

## Tabela de compatibilidade verbal

```text
Verbos dominantes compativeis (mesma familia)
redigir/elaborar/minutar      => peticao-processual
revisar/criticar              => revisao-juridica
formatar/gerar docx           => mod4
protocolar/anexar             => peticionamento-eletronico
extrair/levantar/cronologia   => levanta-fatos
classificar/auditar estrutura => governanca-skills
calcular/precificar           => honorarios
sintetizar/dossiar            => dossie-caso
monitorar/acompanhar          => monitor-publicacoes
comunicar/explicar para leigo => comunicacao-cliente
organizar pasta/renomear      => organizar-pasta-cliente
governar arquivo/permissao    => file-safety
```

## Quando aplicar a postura de devolucao

Se o conteudo recebido apresentar:

```text
verbo dominante ambiguo
output primario indeterminavel
sobreposicao parcial com mais de uma skill-pai
risco operacional desconhecido
```

Devolver a usuaria com matriz, conforme postura fixada. Nao decidir por
inferencia silenciosa.

## Exemplos resolvidos

```text
"Modelo de checklist de pedidos."
=> verbo dominante: nenhum proprio (apenas estrutura). Destino: asset.
   skill-pai possivel: peticao-processual.
   destino final: peticao-processual/assets/ ou _shared/assets/.

"Rotina para nomear arquivos antes do protocolo."
=> verbo dominante: organizar/normalizar. Skill-pai: peticionamento-eletronico.
   destino: peticionamento-eletronico/scripts/ ou _shared/scripts/.

"Procedimento para detectar verbo dominante em SKILL.md."
=> verbo dominante: detectar/auditar estrutura.
   skill-pai: governanca-skills.
   destino: modo interno ou script local.

"Metodologia para conduzir entrevista factual com cliente."
=> verbo dominante: extrair/levantar.
   skill-pai: levanta-fatos.
   destino: modo interno ou reference.
```

## Limite

A regra hierarquica nao substitui a decisao da usuaria. Em caso de duvida,
o modo `classificacao` deve devolver a matriz de criterios e os destinos
possiveis para escolha consciente.
