








# Lições L22–L27 — append em _compartilhados/informacoes/licoes-aprendidas.md
# Extraídas do processo de criação da skill embargos-declaracao (2026-05-18)
# Instruções: appender este bloco ao final de licoes-aprendidas.md

---

## L22 — Pesquisa de domínio é gate, não premissa informal

**skill_afetada:** skill-creator-am (Fase -1)
**categoria:** gate
**como_descoberto:** processo de criação de embargos-declaracao — impossível responder os 6 campos do §0 com precisão sem antes mapear art. 1.022 CPC, art. 897-A CLT, Súmulas 98/297, Temas e zonas cinzentas de cabimento

**Descrição:** O §0 do skill-creator-am coloca as 6 perguntas como primeiro passo, mas skills de domínio jurídico (frente C5 + categoria capability) exigem pesquisa substantiva anterior. Sem mapear norma primária + jurisprudência vinculante + zonas cinzentas, os campos de scope, ASSETS, examples e chains_to ficam preenchidos com suposições que passam em A1-A21 mas produzem skill funcionalmente deficiente. A1-A21 verifica forma, não profundidade de conteúdo.

**Providência:** Fase -1 adicionada ao §0 de skill-creator-am v1.7.0. Gate: antes das 6 perguntas, verificar se criador consegue responder (a) norma primária, (b) jurisprudência vinculante, (c) zonas cinzentas.

---

## L23 — Planejamento de pastas antes do SKILL.md revela complexidade oculta

**skill_afetada:** skill-creator-am (passo 3.5)
**categoria:** gate + output
**como_descoberto:** processo de criação de embargos-declaracao — o planejamento antecipado de ASSETS/MODELOS/SCHEMAS revelou 6+ arquivos de assets, 5+ modelos, 1 schema com 12+ campos, alterando estimativa de volume e design

**Descrição:** O pipeline Create trata o planejamento de pastas de conteúdo como etapas posteriores (passos 6-11 na versão anterior). Na prática, esse planejamento revela complexidade que pode alterar as 4 dimensões, chains_to e depends_on. Descoberto após o SKILL.md, o custo de retrabalho é alto. O passo 3.5 antecipa o planejamento como gate de viabilidade antes de gerar o SKILL.md.

**Providência:** Passo 3.5 adicionado ao pipeline Create de skill-creator-am v1.7.0. Inclui limiar: se volume > 4 ASSETS + 3 MODELOS + 12 campos schema → reavaliar split via V8.

---

## L24 — Decisão de omitir artefato deve ser documentada, não implícita

**skill_afetada:** skill-creator-am (§14 decisoes_omitidas)
**categoria:** frontmatter + output
**como_descoberto:** processo de criação de embargos-declaracao — R11 levou à decisão de omitir scripts/ na v1.0, mas essa decisão ficou verbal, sem registro no SKILL.md

**Descrição:** O SKILL.md não tinha campo para registrar decisões de design negativas (o que foi deliberadamente excluído e por quê). Auditoria R9 não consegue distinguir "scripts/ foi esquecido" de "scripts/ foi omitido por R11 com condição de inclusão em v1.1". Também afeta mantenedor futuro que ao criar v1.1 não sabe se deve incluir scripts/ ou não.

**Providência:** Subseção `decisoes_omitidas` adicionada ao §14 de skill-creator-am v1.7.0. Formato: `[artefato]: [razão] → [condição de inclusão na próxima versão]`.

---

## L25 — Zonas cinzentas de cabimento merecem ASSET dedicado, não apenas examples negativos

**skill_afetada:** skill-creator-am (§4-C) + padrão de examples/
**categoria:** output
**como_descoberto:** processo de criação de embargos-declaracao — a tabela de zonas cinzentas de EDcl (obscuridade vs. discordância de mérito, omissão vs. apreciação insuficiente, dúvida objetiva vs. dúvida da parte) tem valor operacional superior a exemplos isolados porque generaliza o raciocínio para casos novos

**Descrição:** O padrão "3 positivos + 2 negativos" em examples/ captura casos extremos mas não captura o raciocínio decisório nos casos intermediários. Para skills jurídicas com zonas cinzentas reconhecidas, a tabela decisória (vício, sintoma, zona cinzenta, critério de resolução) é o único instrumento que permite ao operador tomar decisões autônomas em casos novos não previstos nos exemplos.

**Providência:** §4-C de skill-creator-am v1.7.0 inclui instrução explícita: para skills com zonas cinzentas de cabimento, criar ASSET dedicado com tabela decisória.

---

## L26 — Múltiplos regimes normativos com workflow análogo: critério V8 explícito

**skill_afetada:** skill-creator-am (§4-I V8 + §4-B MODELOS)
**categoria:** gate
**como_descoberto:** processo de criação de embargos-declaracao — EDcl trabalhista (CLT art. 897-A) e EDcl cível/previdenciário (CPC art. 1.022) têm bases normativas distintas mas workflow análogo; a decisão de unificar em uma skill com variantes MODELOS/ foi tomada por intuição, sem critério documentado

**Descrição:** O V8 perguntava "scope misto?" mas não tinha critério para o caso de múltiplos regimes normativos com workflow análogo. A ausência de critério levou a decisões intuitivas que podem ser inconsistentes entre skills. O critério agora codificado: se o workflow operacional é análogo (mesmos passos, mesma lógica) e apenas as normas diferem → unificar com variantes em MODELOS/; se o workflow diverge estruturalmente → split obrigatório via protocolo V8.

**Providência:** Dimensão adicional adicionada ao V8 em skill-creator-am v1.7.0 (§4-I) e nota correspondente em §4-B.

---

## L27 — O processo real de criação tem 3 fases; o pipeline formal reconhecia 2

**skill_afetada:** skill-creator-am (arquitetura geral) + governanca-skills (A22, A23)
**categoria:** gate + output
**como_descoberto:** processo de criação de embargos-declaracao — foram necessárias 2 sessões de pesquisa (substantiva de domínio + análise de governança) antes de sequer chegar às 6 perguntas do §0

**Descrição:** O skill-creator-am dividia o trabalho em pré-criação e pós-criação. Na prática, skills jurídicas complexas têm uma fase anterior não formalizada: pesquisa substantiva de domínio. Sem essa fase, o criador preenche os campos com suposições plausíveis. O problema não é detectável por A1-A21 porque esses critérios verificam forma, não profundidade de conteúdo. MODELOS/ com cabeçalhos vazios e ASSETS/ com listas sem conteúdo passam em A1-A21 mas falham funcionalmente. A22 e A23 foram criados em governanca-skills v1.1.0 para cobrir especificamente essa lacuna de profundidade.

**Providência:** Fase -1 adicionada em skill-creator-am v1.7.0. A22 (MODELOS/ qualidade) e A23 (ASSETS/ autossuficiência) adicionados em governanca-skills v1.1.0.

