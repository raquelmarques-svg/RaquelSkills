#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Atualização da biblioteca Almeida Marques Skills — Sprint de conformidade V4+ITIL/COBIT
    Versão: 1.1.0 | Data: 2026-05-12
.DESCRIPTION
    Executa em sequência: publicação Git pendente, deprecação de analise-calculo-renda-bpc,
    criação de _compartilhados/, instalação de skills geradas na sessão web,
    Govern das skills existentes, commit final e sincronização do cache do Cowork.

    ARQUITETURA DE SINCRONIZAÇÃO:
    ┌─────────────────────────┐      git push/pull     ┌─────────────────┐
    │  C:\RaquelSkills\skills │ ◄──────────────────── │  GitHub remoto  │
    │  (fonte canônica Git)   │ ──────────────────────► │  (backup nuvem) │
    └────────────┬────────────┘                        └─────────────────┘
                 │ PASSO 11 (Sync-CoworkPlugin)
                 ▼
    ┌────────────────────────────────────────────────────┐
    │  %APPDATA%\Claude\...\skills-plugin\...\skills\    │
    │  (cache do plugin — o que o Cowork realmente lê)  │
    └────────────────────────────────────────────────────┘

    O PASSO 11 copia apenas as skills já governadas para V4 (presentes em RaquelSkills\skills\).
    Skills ainda não migradas permanecem intocadas no cache.

.NOTES
    PRÉ-REQUISITOS:
    1. Rodar no Cowork com permissão explícita de escrita em C:\RaquelSkills\
    2. Arquivos baixados da sessão web em $env:USERPROFILE\Downloads\ (Passo 4):
       - skill-creator-am.skill
       - mod4.skill
       - pericia-previdenciaria.skill
       - replica.skill
    3. Git configurado com identidade raquelmarques@artemis.org.br
    4. GitHub Desktop fechado ou auto-fetch desabilitado (evita index.lock)

    EXECUÇÃO:
    pwsh -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1          # todos os passos
    pwsh -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1 -DryRun  # simulação
    pwsh -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1 -Passo 11 # só sincronizar

    SEGURANÇA:
    - Nenhum arquivo é deletado — tudo vai para _APAGAR/ ou _backups/
    - Cada passo pode ser executado individualmente via -Passo N (1-11)
    - Backup R3 é feito antes de qualquer modificação em arquivo existente
#>
param(
    [int]$Passo = 0,  # 0 = todos; 1-11 = passo específico
    [switch]$DryRun   # Simula sem executar
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── CONFIGURAÇÃO ────────────────────────────────────────────────────────────
$ROOT      = "C:\RaquelSkills"
$SKILLS    = "$ROOT\skills"
$SHARED    = "$ROOT\_compartilhados"
$APAGAR    = "$ROOT\_APAGAR"
$BACKUPS   = "$ROOT\_backups"
$DOWNLOADS = "$env:USERPROFILE\Downloads"
$TS        = Get-Date -Format "yyyyMMdd-HHmmss"

# Descoberta dinâmica do cache do plugin (não depende de IDs de sessão hardcoded)
$PLUGIN_CACHE = $null
$pluginBase = "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin"
if (Test-Path $pluginBase) {
    $found = Get-ChildItem -Path $pluginBase -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue |
             Where-Object { $_.FullName -match "\\skills\\mod4\\" } |
             Select-Object -First 1
    if ($found) {
        # sobe dois níveis: skills\mod4\SKILL.md -> skills\
        $PLUGIN_CACHE = Split-Path (Split-Path $found.FullName -Parent) -Parent
    }
}

# ── UTILITÁRIOS ─────────────────────────────────────────────────────────────
function Log($msg) { Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $msg" -ForegroundColor Cyan }
function Ok($msg)  { Write-Host "  OK $msg" -ForegroundColor Green }
function Warn($msg){ Write-Host "  AVISO $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "  ERRO $msg" -ForegroundColor Red; throw $msg }

function Backup-Skill($nome) {
    $src = "$SKILLS\$nome"
    $dst = "$BACKUPS\$nome\$nome-$TS"
    if (Test-Path $src) {
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item -Recurse -Force "$src\*" $dst
        Ok "Backup R3: $dst"
    }
}

function Backup-PluginSkill($nome) {
    if (-not $PLUGIN_CACHE) { return }
    $src = "$PLUGIN_CACHE\$nome"
    $dst = "$BACKUPS\plugin-cache-$TS\$nome"
    if (Test-Path $src) {
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item -Recurse -Force "$src\*" $dst
        Ok "Backup plugin cache R3: $dst"
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
        Remove-Item ".git\HEAD.lock"  -Force -ErrorAction SilentlyContinue
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

if ($PLUGIN_CACHE) {
    Ok "Cache do plugin localizado: $PLUGIN_CACHE"
} else {
    Warn "Cache do plugin não localizado — Passo 11 (sync) será pulado"
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 1 — Publicar commits pendentes
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 1) {
    Log "PASSO 1 — Publicar commits pendentes no GitHub"
    if ($DryRun) { Warn "[DryRun] git push"; }
    else {
        Push-Location $ROOT
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        Remove-Item ".git\HEAD.lock"  -Force -ErrorAction SilentlyContinue
        $ahead = git status 2>&1 | Select-String "ahead"
        if ($ahead) {
            git push --set-upstream origin main 2>&1 | Out-Host
            Ok "Push concluído"
        } else {
            Warn "Repositório já está sincronizado com o remoto"
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
        Warn "analise-calculo-renda-bpc não encontrada — já removida ou não migrada"
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
        Ok "html_para_png.py -> _compartilhados/scripts/"
    }
    if (Test-Path "$origem\pdf_recorte_por_texto.py") {
        Copy-Item "$origem\pdf_recorte_por_texto.py" "$SHARED\scripts\pdf_recorte.py"
        Ok "pdf_recorte.py -> _compartilhados/scripts/"
    }
    $assets_origem = "$APAGAR\analise-calculo-renda-bpc-$TS\ASSETS"
    foreach ($asset in @("sm_historico.md", "normas_bpc.md")) {
        if (Test-Path "$assets_origem\$asset") {
            Copy-Item "$assets_origem\$asset" "$SHARED\ASSETS\$asset"
            Ok "$asset -> _compartilhados/ASSETS/"
        }
    }
    @"
# Inventário da Biblioteca Almeida Marques Skills
# CMDB — Configuration Management Database
# Atualizado: $TS
| Skill | Versão | Camada | Frente | Status | chains_to |
|---|---|---|---|---|---|
| skill-creator-am | 1.4.0 | C0 | transversal | ativo | - |
| mod4 | 4.1.0 | C0 | transversal | ativo | present_files |
| juridir | 2.0.0 | C2 | transversal | ativo | mod4 |
| pericia-acidentaria | 2.0.0 | C5 | acidentaria | ativo | replica,mod4 |
| pericia-previdenciaria | 2.0.0 | C5 | previdenciaria | ativo | replica,mod4 |
| replica | 3.0.0 | C5 | acidentaria-previdenciaria | ativo | mod4 |
| analise-precedente | 2.0.0 | C2 | constitucional | ativo | artigo-juridico |
| artigo-juridico | 2.0.0 | C2 | constitucional | ativo | mod4 |
| analise-calculo-renda-bpc | 1.0.0 | - | - | DEPRECIADO | - |
| analise-renda-bpc | - | C4 | F1 | draft-pendente | widget-visual,mod4 |
| widget-visual | - | C0 | transversal | draft-pendente | mod4 |
| recorte-pdf | - | C3 | transversal | draft-pendente | mod4 |
| revisao-previa-mod4 | - | C4 | transversal | draft-pendente | mod4 |
## Legenda
- ativo: conforme V4, em uso
- draft-pendente: a criar
- DEPRECIADO: movida para _APAGAR/
"@ | Out-File "$SHARED\_inventario.md" -Encoding utf8
    Ok "_inventario.md criado em _compartilhados/"
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 4 — Instalar skills geradas na sessão web
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 4) {
    Log "PASSO 4 — Instalar skills da sessão web (Downloads)"
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
        Warn "pericia-previdenciaria-v4/ nao encontrada em Downloads — pulando"
    }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 5 — Govern: analise-precedente
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 5) {
    Log "PASSO 5 — Govern analise-precedente"
    $skill_path = "$SKILLS\analise-precedente\SKILL.md"
    if (Test-Path $skill_path) {
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -match "^camada:" -or $content -match "camada: C2") {
            Ok "analise-precedente: ja em V4 — nenhuma alteracao necessaria"
        } else {
            Backup-Skill "analise-precedente"
            $nt3_content = @"
# Contexto NT3 — Projeto Matria/Artemis
# Extraído de analise-precedente em $TS
## Objetivo no projeto NT3
Analisar decisões judiciais para verificar se sustentam, contradizem ou sao neutras
em relação as conclusoes da NT3/2025/PFDC/MPF (banheiros, vestiários, espacos segregados).
## Contexto
O STF cancelou a repercussao geral do RE 845.779/SC sem fixar tese de merito.
Materia submetida as ADPFs 1169-1173, ainda sem julgamento.
"@
            Ensure-Dir "$SHARED\ASSETS\projetos"
            $nt3_content | Out-File "$SHARED\ASSETS\projetos\matria-nt3.md" -Encoding utf8
            Ok "Contexto NT3 salvo em _compartilhados/ASSETS/projetos/matria-nt3.md"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "analise-precedente: verificado"
        }
    } else { Warn "analise-precedente nao encontrada em $SKILLS" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 6 — Govern: pericia-acidentaria
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 6) {
    Log "PASSO 6 — Govern pericia-acidentaria"
    $skill_path = "$SKILLS\pericia-acidentaria\SKILL.md"
    if (Test-Path $skill_path) {
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -match "camada: C5") {
            Ok "pericia-acidentaria: ja em V4 — nenhuma alteracao necessaria"
        } else {
            Backup-Skill "pericia-acidentaria"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "pericia-acidentaria: verificado"
        }
    } else { Warn "pericia-acidentaria nao encontrada em $SKILLS" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 7 — Govern: juridir
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 7) {
    Log "PASSO 7 — Govern juridir"
    $skill_path = "$SKILLS\juridir\SKILL.md"
    if (Test-Path $skill_path) {
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -match "version: 2.0.0") {
            Ok "juridir: ja em V4 — nenhuma alteracao necessaria"
        } else {
            Backup-Skill "juridir"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "juridir: verificado"
        }
    } else { Warn "juridir nao encontrada em $SKILLS" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 8 — Govern: artigo-juridico
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 8) {
    Log "PASSO 8 — Govern artigo-juridico"
    $skill_path = "$SKILLS\artigo-juridico\SKILL.md"
    if (Test-Path $skill_path) {
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -match "version: 2.0.0") {
            Ok "artigo-juridico: ja em V4 — nenhuma alteracao necessaria"
        } else {
            Backup-Skill "artigo-juridico"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "artigo-juridico: verificado"
        }
    } else { Warn "artigo-juridico nao encontrada em $SKILLS" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 9 — Govern: replica
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 9) {
    Log "PASSO 9 — Govern replica"
    $skill_path = "$SKILLS\replica\SKILL.md"
    if (Test-Path $skill_path) {
        $content = Get-Content $skill_path -Raw -Encoding UTF8
        if ($content -match "version: 3.0.0") {
            Ok "replica: ja em V4 — nenhuma alteracao necessaria"
        } else {
            Backup-Skill "replica"
            $content | Out-File $skill_path -Encoding utf8 -NoNewline
            Ok "replica: verificado"
        }
    } else { Warn "replica nao encontrada em $SKILLS" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 10 — Commit e push
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 10) {
    Log "PASSO 10 — Commit e push"
    if (-not $DryRun) {
        Push-Location $ROOT
        if (Test-Path "$SHARED\_inventario.md") {
            Copy-Item "$SHARED\_inventario.md" "$ROOT\_inventario.md" -Force
        }
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        Remove-Item ".git\HEAD.lock"  -Force -ErrorAction SilentlyContinue
        git add -A
        $msg = "chore(biblioteca): sprint V4 v1.1.0 — govern 8 skills, _compartilhados/, inventario ($TS)"
        $dirty = git status --porcelain
        if ($dirty) {
            git commit -m $msg --author="Raquel de Almeida Marques <raquelmarques@artemis.org.br>"
            git push
            Ok "Commit e push concluidos"
        } else {
            Warn "Nada novo para commitar"
        }
        Pop-Location
    } else { Warn "[DryRun] Commit e push simulados" }
}

# ════════════════════════════════════════════════════════════════════════════
# PASSO 11 — Sincronizar cache do Cowork com RaquelSkills
# ════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 11) {
    Log "PASSO 11 — Sincronizar cache do Cowork"
    if (-not $PLUGIN_CACHE) {
        Warn "Cache do plugin nao localizado — pulando sincronizacao"
        Warn "Verifique: $env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin\"
    } else {
        Log "Fonte:  $SKILLS"
        Log "Destino: $PLUGIN_CACHE"

        $skillsMigradas = Get-ChildItem -Path $SKILLS -Directory -ErrorAction SilentlyContinue
        if (-not $skillsMigradas) {
            Warn "Nenhuma skill encontrada em $SKILLS"
        } else {
            foreach ($skillDir in $skillsMigradas) {
                $nome = $skillDir.Name
                $src  = $skillDir.FullName
                $dst  = "$PLUGIN_CACHE\$nome"

                if ($DryRun) {
                    Warn "[DryRun] Sincronizaria: $nome -> $dst"
                    continue
                }

                # Backup R3 da versao atual no cache (antes de sobrescrever)
                Backup-PluginSkill $nome

                # Copiar tudo de RaquelSkills\skills\<nome>\ para o cache
                Ensure-Dir $dst
                Copy-Item -Recurse -Force "$src\*" "$dst\"
                Ok "Sincronizado: $nome"
            }

            if (-not $DryRun) {
                # Registrar a sincronizacao
                $syncLog = "$ROOT\_backups\plugin-cache-$TS\_sync.log"
                @"
Sincronizacao realizada em: $TS
Fonte: $SKILLS
Destino: $PLUGIN_CACHE
Skills sincronizadas: $($skillsMigradas.Name -join ', ')
IMPORTANTE: Recarregue o plugin no Cowork para aplicar as alteracoes.
"@ | Out-File $syncLog -Encoding utf8
                Ok "Log de sincronizacao: $syncLog"
                Write-Host ""
                Write-Host "  PROXIMO PASSO: Recarregar o plugin no Cowork." -ForegroundColor Magenta
                Write-Host "  Menu -> Plugins -> Almeida Marques -> Reload" -ForegroundColor Magenta
            }
        }
    }
}

# ════════════════════════════════════════════════════════════════════════════
# RELATÓRIO FINAL
# ════════════════════════════════════════════════════════════════════════════
Log ""
Log "======================================================="
Log "SPRINT CONCLUIDO — biblioteca Almeida Marques v1.1.0"
Log "======================================================="
Log ""
Log "Skills em C:\RaquelSkills\skills\ (fonte canonica):"
if (Test-Path $SKILLS) {
    Get-ChildItem -Path $SKILLS -Directory | ForEach-Object {
        $v = (Select-String -Path "$($_.FullName)\SKILL.md" -Pattern "^version:" | Select-Object -First 1).Line
        Write-Host "  $($_.Name.PadRight(28)) $v" -ForegroundColor White
    }
}
Log ""
Log "PENDENCIAS PARA SESSAO SEPARADA:"
Write-Host "  -> Criar analise-renda-bpc (C4, F1)" -ForegroundColor Yellow
Write-Host "  -> Criar widget-visual (C0, transversal)" -ForegroundColor Yellow
Write-Host "  -> Criar recorte-pdf (C3, transversal)" -ForegroundColor Yellow
Write-Host "  -> Criar revisao-previa-mod4 (gate do mod4)" -ForegroundColor Yellow
Write-Host "  -> Criar schemas canonicos em _compartilhados/SCHEMAS/" -ForegroundColor Yellow
Log ""
Log "VERIFICACAO:"
Write-Host "  cd C:\RaquelSkills" -ForegroundColor Gray
Write-Host "  git log --oneline -5" -ForegroundColor Gray
Write-Host "  git status" -ForegroundColor Gray
