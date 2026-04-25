# Checklist de skill operacional (auditoria leve)

Esta checklist e usada pelo modo `auditoria` da governanca-skills. Ela
cobre apenas o que pode ser conferido em nivel estrutural raso.
Auditoria substantiva, profunda ou de qualidade redacional pertence a
healthcheck-biblioteca.

## Itens estruturais do SKILL.md

```text
[ ] frontmatter contem name, description, version, layer, activation;
[ ] description e curta, declara quando ativar e o que a skill faz;
[ ] secao Finalidade declara para que serve;
[ ] secao Transformacao declara input, operacao e output;
[ ] secao Gatilhos lista palavras de ativacao;
[ ] secao Bloqueios lista o que a skill NAO faz;
[ ] secao Entrada minima declara o que precisa ter para nao falhar;
[ ] secao Procedimento operacional obrigatorio existe e tem passos
    numerados;
[ ] secao Outputs declara saida primaria e formatos;
[ ] secao Limites lista fronteiras com outras skills;
[ ] SKILL.md tem entre 30 e 500 linhas.
```

## Itens estruturais das pastas

```text
[ ] assets/ existe;
[ ] templates/ existe;
[ ] schemas/ existe;
[ ] scripts/ existe;
[ ] references/ existe;
[ ] examples/ existe;
[ ] config/ existe.
```

Pasta vazia gera alerta, nao reprovacao, salvo se SKILL.md citar arquivo
inexistente.

## Itens estruturais do output

```text
[ ] toda execucao termina com Status;
[ ] toda execucao declara Output produzido;
[ ] toda execucao declara Lacunas;
[ ] toda execucao declara Proxima acao;
[ ] toda execucao declara Proxima skill permitida;
[ ] toda execucao declara Bloqueios.
```

## Status emitidos pela auditoria leve

```text
AUDITORIA_OK             todos os itens presentes;
AUDITORIA_COM_ALERTAS    presentes, mas com pasta vazia citada em SKILL.md;
AUDITORIA_REPROVADA      ao menos um item obrigatorio ausente.
```

## Limite expresso

A auditoria leve nao verifica:

```text
qualidade do verbo dominante;
adequacao do output ao input;
duplicidade entre skills;
coerencia com _manifest;
fluxo de chamadas;
qualidade redacional;
correcao juridica;
adequacao da SkillCreationSpec correspondente.
```

Esses pontos pertencem a healthcheck-biblioteca, e a auditoria leve deve
indica-la como proxima skill quando o pedido envolver substancia.
