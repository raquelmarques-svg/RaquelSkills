# NTEP — Pares CNAE x CID mais frequentes na pratica do escritorio

Fonte: Decreto 3.048/1999, Anexo II (Lista A — Relacao de Agentes Patogenicos).
Data de referencia: 2026-05-12. Verificar atualizacoes no e-SociaL / INSS quando CID ou CNAE
nao constar desta tabela.

## Como usar

1. Localizar o CNAE de 7 digitos do empregador (CTPS, CNIS, PPP ou contrato social)
2. Localizar o CID-10 principal da doenca (laudo, CAT, beneficio)
3. Verificar se o par consta abaixo
4. Se constar: `ntep_aplicavel: true` — presuncao de nexo opera de pleno direito (art. 21-A Lei 8.213/91)
5. Se nao constar nesta tabela: consultar a Lista A completa antes de declarar `ntep_aplicavel: false`

---

## Grupo M — Doencas osteomusculares (as mais frequentes na acidentaria)

| CID | Descricao | CNAEs que ativam NTEP |
|---|---|---|
| M54.5 | Dor lombar baixa | 2910701, 2920600, 2930102, 3101200 (metalurgia/montagem) |
| M51.1 | Degeneracao de disco intervertebral com radiculopatia | 2910701, 2920600, 4930202 (motoristas) |
| M75.1 | Sindrome do manguito rotador | 2910701, 1013901 (abate/frigorifico) |
| M65.3 | Dedo em gatilho | 1013901, 1051100, 1061901 (frigorifico/laticinios) |
| M77.1 | Epicondilite lateral (cotovelo de tenista) | 2910701, 1013901, 3299001 |
| M77.0 | Epicondilite medial | 1013901, 2910701 |
| M70.0 | Sinovite crepitante do punho e mao | 2910701, 1013901 |
| M79.2 | Nevralgia e neurite | 2910701, 4930202 |

## Grupo G — Doencas do sistema nervoso

| CID | Descricao | CNAEs que ativam NTEP |
|---|---|---|
| G56.0 | Sindrome do tunel do carpo | 2910701, 1013901, 1051100, 3299001 |
| G54.2 | Lesao da raiz cervical | 2910701, 4930202 |
| G54.4 | Lesao da raiz lombossacra | 2910701, 4930202 |

## Grupo F — Transtornos mentais (crescente na pratica)

| CID | Descricao | CNAEs que ativam NTEP |
|---|---|---|
| F32.0-F32.9 | Episodio depressivo | 8411600 (administracao publica), 6422100 (banco) |
| F41.2 | Transtorno misto ansioso-depressivo | 8411600, 6422100 |
| F43.2 | Transtorno de adaptacao | 8411600 |

## Grupo J — Doencas respiratorias

| CID | Descricao | CNAEs que ativam NTEP |
|---|---|---|
| J45.0 | Asma predominantemente alergica | 2399101 (mineracao nao-metalica) |
| J60 | Pneumoconiose dos mineiros de carvao | 0610600 |
| J61 | Pneumoconiose por amianto/asbesto | 2399101, 2319200 |

---

## Nota sobre o processo de verificacao

A Lista A completa tem mais de 400 pares. Esta tabela cobre os casos mais frequentes. Para CNAEs
ou CIDs nao listados, verificar o Decreto 3.048 Anexo II disponivel em:
https://www.planalto.gov.br/ccivil_03/decreto/d3048.htm

Se o par nao consta da Lista A, o nexo pode ainda ser estabelecido por:
(a) nexo clinico individual comprovado por laudo medico
(b) nexo tecnico por analogia com condicoes laborativas similares
(c) concausa (art. 21 §1o Lei 8.213/91) — trabalho como fator contribuinte
