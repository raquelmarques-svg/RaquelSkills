# Exemplo: CREATE — Criar nova skill

## Cenário

Você quer criar uma skill que **analisa precedentes judiciais** para extrair:
- Principais teses jurídicas
- Votação e placar
- Referências a outras decisões
- Impacto no caso da cliente

## Diálogo com skill-creator-am

### Passo 1: Proposta inicial

**Usuária:**
```
Quero criar uma skill que analisa precedentes judiciais (STF, STJ, TRF).
Objetivo: extrair teses, placar, referências cruzadas.
Categoria: análise de jurisprudência.
Exemplos de entrada: URL de acórdão, texto de ementa.
```

### Passo 2: Validação pela skill (R6 + R10)

**skill-creator-am:**
```
✅ Proposta válida. Feedback:

1. DISCORDÂNCIA ÚTIL (R10):
   - Você quer "extrair teses" — como lidar com votações divergentes?
   - Sugestão: criar campo "teses_concorrentes" para votos vencidos
   
2. ADAPTAÇÃO (R6):
   - "Referências cruzadas" é amplo — limitar a:
     a) Referências diretas (essa decisão cita X)
     b) Referências indiretas (essa decisão é citada por X)
   - Qual dos dois (ou ambos)?

3. ECONOMIA (R11):
   - Análise de URLs exige OCR + parsing — custoso
   - Proposta: aceitar texto de ementa já extraído; OCR fica em skill separada
   - OK para você?
```

### Passo 3: Feedback da usuária

**Usuária:**
```
Ótimo feedback. Respostas:

1. Sim, incluir teses concorrentes (votos vencidos)
2. Incluir ambos os tipos de referência cruzada
3. Começar com texto de ementa; OCR fica para Tier 3
```

### Passo 4: Geração da skill

**skill-creator-am gera:**

```
✅ Skill criada: C:\RaquelSkills\skills\analise-precedente\

Estrutura:
  SKILL.md
    ---
    title: analise-precedente
    description: "Extrai teses, placar, referências cruzadas de precedentes judiciais (STF/STJ/TRF)"
    version: 1.0.0
    category: capability
    núcleo: N2              (análise)
    frente: transversal     (aplicável a todos)
    camada: C4              (depende de jurisprudência, precedentes em Drive)
    projeto: Proj02
    author: Raquel de Almeida Marques
    verified_in: 2026-05-11
    ---
    
    [Instruções da skill...]

  README.md
    - Documentação completa
    - Exemplos de entrada/saída
    
  examples/
    - exemplo-stf-recurso-extraordinario.md
    - exemplo-stj-previdenciario.md
    - exemplo-trf-trabalhista.md
    
  templates/
    - template-analise-precedente.md
    
  schemas/
    - precedente.schema.json


Status: ✅ Pronta para implementação

Próximos passos:
1. Você implementa lógica em SKILL.md
2. Testa com exemplos/
3. Registramos em _inventario.md com status "ativa"
4. Primeira auditoria em 2026-06-11
```

### Passo 5: Registro em _inventario.md

**Entrada adicionada:**

```yaml
| analise-precedente | capability | Proj02 | N2 | transversal | C4 | 1.0.0 | ativa | 2026-05-11 |
```

### Passo 6: Registro em _log-auditoria.md

**Entrada adicionada:**

```yaml
| 2026-05-11 | 10:35 | CREATE | analise-precedente | v1.0.0 | ativa | Criada skill para análise de jurisprudência; inclui teses, placar, referências cruzadas |
```

---

## Resultado final

A skill está criada e pronta para implementação. Você pode:

1. **Editar SKILL.md** para adicionar lógica detalhada
2. **Preencheer examples/** com casos reais
3. **Criar templates/** para documentos padrão
4. **Testar** com `auditar_skill_completo.py --skill analise-precedente`

Se precisar fazer mudanças, use **EDIT** (não DELETE + CREATE).
