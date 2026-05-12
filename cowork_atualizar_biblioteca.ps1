#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Atualização da biblioteca Almeida Marques Skills — Sprint de conformidade V4+ITIL/COBIT
    Versão: 1.0.0 | Data: 2026-05-11
.DESCRIPTION
    Executa em sequência: publicação Git pendente, deprecação de analise-calculo-renda-bpc,
    criação de _compartilhados/, instalação de skills geradas na sessão web,
    Govern das skills existentes, criação do _inventario.md e commit final.
.NOTES
    PRÉ-REQUISITOS:
    1. Rodar no Cowork com permissão explícita de escrita em C:\RaquelSkills\
    2. Arquivos baixados da sessão web em $env:USERPROFILE\Downloads\:
       - skill-creator-am.skill
       - mod4.skill
       - pericia-previdenciaria.skill (pericia-previdenciaria-v4\SKILL.md)
       - replica.skill
    3. Git configurado com identidade raquelmarques@artemis.org.br
    EXECUÇÃO:
    pwsh -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1
    SEGURANÇA:
    - Nenhum arquivo é deletado — tudo vai para _APAGAR/ ou _backups/
    - Cada passo pode ser executado individualmente via -Passo N
#>
param(
    [int]$Passo = 0,  # 0 = todos; 1-10 = passo específico
    [switch]$DryRun   # Simula sem executar
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
# ── CONFIGURAÇÃO ────────────────────────────────────────────────────────────
$ROOT     = "C:\RaquelSkills"
$SKILLS   = "$ROOT\skills"
$SHARED   = "$ROOT\_compartilhados"
$APAGAR   = "$ROOT\_APAGAR"
$BACKUPS  = "$ROOT\_backups"
$DOWNLOADS = "$env:USERPROFILE\Downloads"
$TS       = Get-Date -Format "yyyyMMdd-HHmmss"
# ── UTILITÁRIOS ─────────────────────────────────────────────────────────────
function Log($msg) { Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $msg" -ForegroundColor Cyan }
function Ok($msg)  { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Warn($msg){ Write-Host "  ⚠ $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "  ✗ $msg" -ForegroundColor Red; throw $msg }
function Backup-Skill($nome) {
    $src = "$SKILLS\$nome"
    $dst = "$BACKUPS\$nome\$nome-$TS"
    if (Test-Path $src) {
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item -Recurse -Force "$src\*" $dst
        Ok "Backup R3: $dst"
    }
}
function Install-Skill($arquivo, $nome) {
    $zip = "$DOWNLOADS\$arquivo"
    if (-not (Test-Path $zip)) { Warn "Arquivo não encontrado: $zip — pulando"; return $false }
    Backup-Skill $nome
    New-Item -ItemType Directory -Force -Path "$SKILLS\$nome" | Out-Null
    Expand-Archive -Path $zip -DestinationPath $SKILLS -Force
    Ok "Instalado: $nome"
    return $true
}
function Git-Commit($msg) {
    if ($DryRun) { Warn "[DryRun] git commit: $msg"; return }
    Push-Location $ROOT
    try {
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        git add -A
        $status = git status --porcelain
        if ($status) {
            git commit -m $msg --author="Raquel de Almeida Marques <raquelmarques@artemis.org.br>"
            Ok "Commit: $msg"
        } else {
            Warn "Nada a commitar para: $msg"
        }
    } finally { Pop-Location }
}
function Ensure-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}
# ── VALIDAÇÃO INICIAL ────────────────────────────────────────────────────────
Log "Validando ambiente..."
if (-not (Test-Path $ROOT))   { Err "C:\RaquelSkills não encontrado" }
if (-not (Test-Path $SKILLS)) { Err "C:\RaquelSkills\skills não encontrado" }
Push-Location $ROOT
$gitOk = (git status 2>&1) -match "On branch"
Pop-Location
if (-not $gitOk) { Err "Git não inicializado em $ROOT" }
Ok "Ambiente validado"
# ════════════════════════════════════════════════════════════════════════════
# PASSO 1 — Publicar commits pendentes
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 1) {
    Log "PASSO 1 — Publicar commits pendentes no GitHub"
    if ($DryRun) { Warn "[DryRun] git push"; }
    else {
        Push-Location $ROOT
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        $ahead = git status 2>&1 | Select-String "ahead"
        if ($ahead) {
            git push --set-upstream origin main 2>&1 | Out-Host
            Ok "Push concluído"
        } else {
            Warn "Repositório já está sincronizado"
        }
        Pop-Location
    }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 2 — Deprecar analise-calculo-renda-bpc
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 2) {
    Log "PASSO 2 — Deprecar analise-calculo-renda-bpc (V8 reprovada: 3 camadas)"
    $src = "$SKILLS\analise-calculo-renda-bpc"
    $dst = "$APAGAR\analise-calculo-renda-bpc-$TS"
    if (Test-Path $src) {
        Backup-Skill "analise-calculo-renda-bpc"
        New-Item -ItemType Directory -Force -Path $APAGAR | Out-Null
        Move-Item $src $dst
        Ok "Movido para _APAGAR\: $dst"
        @"
# DEPRECADO — analise-calculo-renda-bpc
Data: $TS
Motivo: V8 reprovada — funções em C3+C4+C0 simultâneas (SRP violado)
Substituído por:
  - analise-renda-bpc (C4, F1) — análise de renda BPC
  - widget-visual (C0, transversal) — geração de PNG
  - recorte-pdf (C3, transversal) — recorte de PDF por âncora
"@ | Out-File "$dst\DEPRECACAO.md" -Encoding utf8
    } else {
        Warn "analise-calculo-renda-bpc não encontrada — já removida"
    }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 3 — Criar estrutura _compartilhados/
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 3) {
    Log "PASSO 3 — Criar _compartilhados/"
    $dirs = @(
        "$SHARED\scripts",
        "$SHARED\ASSETS",
        "$SHARED\SCHEMAS\input",
        "$SHARED\SCHEMAS\output",
        "$SHARED\ASSETS\projetos"
    )
    foreach ($d in $dirs) { Ensure-Dir $d }
    $origem = "$APAGAR\analise-calculo-renda-bpc-$TS\scripts"
    if (Test-Path "$origem\html_blocos_para_png.py") {
        Copy-Item "$origem\html_blocos_para_png.py" "$SHARED\scripts\html_para_png.py"
        Ok "html_para_png.py → _compartilhados/scripts/"
    }
    if (Test-Path "$origem\pdf_recorte_por_texto.py") {
        Copy-Item "$origem\pdf_recorte_por_texto.py" "$SHARED\scripts\pdf_recorte.py"
        Ok "pdf_recorte.py → _compartilhados/scripts/"
    }
    $assets_origem = "$APAGAR\analise-calculo-renda-bpc-$TS\ASSETS"
    foreach ($asset in @("sm_historico.md", "normas_bpc.md")) {
        if (Test-Path "$assets_origem\$asset") {
            Copy-Item "$assets_origem\$asset" "$SHARED\ASSETS\$asset"
            Ok "$asset → _compartilhados/ASSETS/"
        }
    }
    @"
# Inventário da Biblioteca Almeida Marques Skills
# CMDB — Configuration Management Database
# Atualizado: $TS
| Skill | Versão | Camada | Frente | Status | chains_to |
|---|---|---|---|---|---|
| skill-creator-am | 1.4.0 | C0 | transversal | ativo | autorrevisao-skill |
| mod4 | 4.1.0 | C7 | transversal | ativo | present_files |
| pericia-acidentaria | 2.0.0 | C4 | F1 | ativo | replica |
| pericia-previdenciaria | 2.0.0 | C4 | F1 | ativo | replica,mod4 |
| replica | 2.1.0 | C5 | F1 | ativo | revisao-juridica,mod4 |
| juridir | 2.0.0 | C2 | transversal | govern-pendente | - |
| artigo-juridico | 2.0.0 | C5 | F2 | govern-pendente | revisao-juridica,mod4 |
| analise-precedente | 2.0.0 | C4 | transversal | govern-pendente | - |
| analise-calculo-renda-bpc | 1.0.0 | - | - | DEPRECIADO | - |
| analise-renda-bpc | 1.0.0 | C4 | F1 | draft | widget-visual,mod4 |
| widget-visual | 1.0.0 | C0 | transversal | draft | mod4 |
| recorte-pdf | 1.0.0 | C3 | transversal | draft | mod4 |
## Legenda
- ativo: conforme V4+ITIL, em uso
- draft: criada, sem examples/ completos ou sem contrato
- govern-pendente: pré-V4, aguarda modo Govern
- DEPRECIADO: movida para _APAGAR/
"@ | Out-File "$SHARED\_inventario.md" -Encoding utf8
    Ok "_inventario.md criado em _compartilhados/"
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 4 — Instalar skills geradas na sessão web
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 4) {
    Log "PASSO 4 — Instalar skills da sessão web"
    $installs = @(
        @{ arquivo="skill-creator-am.skill"; nome="skill-creator-am" },
        @{ arquivo="mod4.skill";             nome="mod4"             },
        @{ arquivo="replica.skill";          nome="replica"          }
    )
    foreach ($i in $installs) { Install-Skill $i.arquivo $i.nome | Out-Null }
    $ppv4 = "$DOWNLOADS\pericia-previdenciaria-v4"
    if (Test-Path $ppv4) {
        Backup-Skill "pericia-previdenciaria"
        Ensure-Dir "$SKILLS\pericia-previdenciaria"
        Copy-Item -Recurse -Force "$ppv4\*" "$SKILLS\pericia-previdenciaria\"
        Ok "pericia-previdenciaria v2.0.0 instalada"
    } else {
        Warn "pericia-previdenciaria-v4/ não encontrada em Downloads — verificar"
    }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 5 — Govern: analise-precedente
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 5) {
    Log "PASSO 5 — Govern analise-precedente: remover hardcode NT3"
    $skill_path = "$SKILLS\analise-precedente\SKILL.md"
    if (Test-Path $skill_path) {
        Backup-Skill "analise-precedente"
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        $nt3_content = @"
# Contexto NT3 — Projeto Matria/Artemis
# Extraído de analise-precedente em $TS
## Objetivo no projeto NT3
Analisar decisões judiciais para verificar se sustentam, contradizem ou são neutras
em relação às conclusões da NT3/2025/PFDC/MPF (banheiros, vestiários, espaços segregados).
## Contexto
O STF cancelou a repercussão geral do RE 845.779/SC sem fixar tese de mérito.
Matéria submetida às ADPFs 1169-1173, ainda sem julgamento.
## Perguntas específicas para precedentes NT3
1. O que a decisão efetivamente decide — e o que não decide?
2. A decisão resolve fato individual ou norma constitucional?
3. A NT3 pode invocar este precedente legitimamente?
"@
        Ensure-Dir "$SHARED\ASSETS\projetos"
        $nt3_content | Out-File "$SHARED\ASSETS\projetos\matria-nt3.md" -Encoding utf8
        Ok "Contexto NT3 salvo em _compartilhados/ASSETS/projetos/matria-nt3.md"
        if ($content -notmatch "^camada:") {
            $v4_header = @"
camada: C4
nucleo: N2
frente: transversal
project: Proj02
categoria: capability
version: 2.0.0
verificado_em: $(Get-Date -Format 'yyyy-MM-dd')
chains_to:
  - mod4
depends_on:
  - dossie-caso
sla:
  tempo_resposta: "1 turno"
  output_garantido: "análise norma-fato-conclusão do precedente"
  condicoes_de_falha: "decisão não fornecida ou ilegível"
"@
            $content = $content -replace "(---\s*\n)", "`$1$v4_header`n"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "analise-precedente: NT3 removido, frontmatter V4 adicionado"
        }
    } else { Warn "analise-precedente não encontrada" }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 6 — Govern: pericia-acidentaria
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 6) {
    Log "PASSO 6 — Govern pericia-acidentaria: chains_to + SLA + frontmatter V4"
    $skill_path = "$SKILLS\pericia-acidentaria\SKILL.md"
    if (Test-Path $skill_path) {
        Backup-Skill "pericia-acidentaria"
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -notmatch "^camada:") {
            $v4_block = @"
camada: C4
nucleo: N6
frente: F1
project: Proj02
categoria: capability
version: 2.0.0
verificado_em: $(Get-Date -Format 'yyyy-MM-dd')
chains_to:
  - replica
  - mod4
depends_on:
  - dossie-caso
  - levanta-fatos
sla:
  tempo_resposta: "2 turnos"
  output_garantido: "análise do laudo + JSON analise_pericial.v1 + quesitos"
  condicoes_de_falha: "laudo não fornecido; PDF ilegível"
  fallback: "listar o que falta e prosseguir com o disponível"
"@
            $content = $content -replace "(---\s*\n)", "`$1$v4_block`n"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "pericia-acidentaria: frontmatter V4 + chains_to + SLA adicionados"
        } else { Warn "pericia-acidentaria: já tem camada — verificar manualmente" }
    } else { Warn "pericia-acidentaria não encontrada" }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 7 — Govern: juridir
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 7) {
    Log "PASSO 7 — Govern juridir: frontmatter V4 mínimo"
    $skill_path = "$SKILLS\juridir\SKILL.md"
    if (Test-Path $skill_path) {
        Backup-Skill "juridir"
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -notmatch "^camada:") {
            $v4_block = @"
camada: C2
nucleo: N5
frente: transversal
project: Proj02
categoria: capability
version: 2.0.0
verificado_em: $(Get-Date -Format 'yyyy-MM-dd')
chains_to:
  - dossie-caso
  - mod4
depends_on: []
sla:
  tempo_resposta: "pipeline automático"
  output_garantido: "pasta organizada + RESUMO.DOCX + ACESSOS.TXT"
  condicoes_de_falha: "pasta vazia; sem permissão de escrita"
"@
            $content = $content -replace "(---\s*\n)", "`$1$v4_block`n"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "juridir: frontmatter V4 adicionado"
        } else { Warn "juridir: já tem camada declarada" }
    } else { Warn "juridir não encontrada" }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 8 — Govern: artigo-juridico
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 8) {
    Log "PASSO 8 — Govern artigo-juridico: frontmatter V4 mínimo"
    $skill_path = "$SKILLS\artigo-juridico\SKILL.md"
    if (Test-Path $skill_path) {
        Backup-Skill "artigo-juridico"
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -notmatch "^camada:") {
            $v4_block = @"
camada: C5
nucleo: N2
frente: F2
project: Proj02
categoria: capability
version: 2.0.0
verificado_em: $(Get-Date -Format 'yyyy-MM-dd')
chains_to:
  - revisao-juridica
  - mod4
depends_on: []
sla:
  tempo_resposta: "sessão dedicada"
  output_garantido: "artigo revisado conforme normas do periódico-alvo"
  condicoes_de_falha: "periódico-alvo não informado; sem acesso ao guia de submissão"
"@
            $content = $content -replace "(---\s*\n)", "`$1$v4_block`n"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "artigo-juridico: frontmatter V4 adicionado"
        } else { Warn "artigo-juridico: já tem camada declarada" }
    } else { Warn "artigo-juridico não encontrada" }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 9 — Govern: replica
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 9) {
    Log "PASSO 9 — Govern replica: frontmatter V4 + nota de delegação de laudo"
    $skill_path = "$SKILLS\replica\SKILL.md"
    if (Test-Path $skill_path) {
        Backup-Skill "replica"
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -notmatch "^camada:") {
            $v4_block = @"
camada: C5
nucleo: N3
frente: F1
project: Proj02
categoria: capability
version: 2.1.0
verificado_em: $(Get-Date -Format 'yyyy-MM-dd')
chains_to:
  - revisao-juridica
  - mod4
depends_on:
  - pericia-acidentaria
  - dossie-caso
sla:
  tempo_resposta: "1-2 turnos"
  output_garantido: "réplica estruturada com seções pertinentes ao caso"
  condicoes_de_falha: "contestação não fornecida"
  fallback: "solicitar contestação antes de prosseguir"
"@
            $content = $content -replace "(---\s*\n)", "`$1$v4_block`n"
        }
        $nota_laudo = @"
> **DELEGAÇÃO (V8 — SRP):** A análise técnica do laudo pericial pertence a
> ``pericia-acidentaria`` (C4). Esta skill (C5) recebe o output de ``pericia-acidentaria``
> via ``analise_pericial.v1.schema.json`` e incorpora a impugnação na réplica.
> Não reanalisar o laudo aqui — consumir o JSON já produzido.
"@
        $content = $content -replace "(## 6\. Impugnação ao laudo pericial)", "$nota_laudo`$1"
        $content | Out-File $skill_path -Encoding utf8 -NoNewline
        Ok "replica: frontmatter V4 + nota de delegação adicionados"
    } else { Warn "replica não encontrada" }
}
# ════════════════════════════════════════════════════════════════════════════
# PASSO 10 — Commit e push final
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 10) {
    Log "PASSO 10 — Commit e push final"
    if (-not $DryRun) {
        Push-Location $ROOT
        Copy-Item "$SHARED\_inventario.md" "$ROOT\_inventario.md" -Force
        git add -A
        $msg = @"
chore(biblioteca): sprint conformidade V4+ITIL/COBIT — $TS
- depreca analise-calculo-renda-bpc (V8: 3 camadas)
- cria _compartilhados/ (scripts, ASSETS, SCHEMAS, inventario)
- instala skill-creator-am v1.4.0, mod4 v4.1.0, replica v2.1.0, pericia-previdenciaria v2.0.0
- govern analise-precedente, pericia-acidentaria, juridir, artigo-juridico, replica
"@
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        git commit -m $msg --author="Raquel de Almeida Marques <raquelmarques@artemis.org.br>"
        git push
        Ok "Push concluído"
        Pop-Location
    } else { Warn "[DryRun] Commit e push simulados" }
}
# ════════════════════════════════════════════════════════════════════════════
# RELATÓRIO FINAL
# ════════════════════════════════════════════════════════════════════════════
Log ""
Log "═══════════════════════════════════════════════"
Log "SPRINT DE CONFORMIDADE CONCLUÍDO"
Log "═══════════════════════════════════════════════"
Log ""
Log "PENDÊNCIAS PARA SESSÃO SEPARADA:"
Write-Host "  → Criar analise-renda-bpc (C4, F1)" -ForegroundColor Yellow
Write-Host "  → Criar widget-visual (C0, transversal)" -ForegroundColor Yellow
Write-Host "  → Criar recorte-pdf (C3, transversal)" -ForegroundColor Yellow
Write-Host "  → Criar revisao-previa-mod4 (gate do mod4)" -ForegroundColor Yellow
Write-Host "  → Criar schemas canônicos em _compartilhados/SCHEMAS/" -ForegroundColor Yellow
Write-Host "  → Govern replica: separar pipelines acidentário/previdenciário" -ForegroundColor Yellow
Log ""
Log "VERIFICAÇÃO:"
Write-Host "  cd C:\RaquelSkills" -ForegroundColor Gray
Write-Host "  git log --oneline -5" -ForegroundColor Gray
Write-Host "  git status" -ForegroundColor Gray
