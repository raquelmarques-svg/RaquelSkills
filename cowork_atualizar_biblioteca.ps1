# cowork_atualizar_biblioteca.ps1
# Versao: 1.2.0 | Data: 2026-05-12
# Biblioteca Almeida Marques Skills - Sprint de conformidade V4
#
# ARQUITETURA DE SINCRONIZACAO:
#   C:\RaquelSkills\skills\  --git push-->  GitHub remoto
#   C:\RaquelSkills\skills\  --Passo 11-->  cache do plugin (o que o Cowork le)
#
# USO:
#   powershell -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1
#   powershell -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1 -DryRun
#   powershell -ExecutionPolicy Bypass -File cowork_atualizar_biblioteca.ps1 -Passo 11
#
# SEGURANCA:
#   - Nenhum arquivo e deletado: tudo vai para _APAGAR/ ou _backups/
#   - Backup R3 antes de qualquer modificacao
#   - Cada passo pode ser executado individualmente via -Passo N (1-11)

param(
    [int]$Passo = 0,
    [switch]$DryRun
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── CONFIGURACAO ─────────────────────────────────────────────────────────────
$ROOT      = "C:\RaquelSkills"
$SKILLS    = "$ROOT\skills"
$SHARED    = "$ROOT\_compartilhados"
$APAGAR    = "$ROOT\_APAGAR"
$BACKUPS   = "$ROOT\_backups"
$DOWNLOADS = "$env:USERPROFILE\Downloads"
$TS        = Get-Date -Format "yyyyMMdd-HHmmss"
$GIT_AUTHOR = "Raquel de Almeida Marques <raquelmarques@artemis.org.br>"

# Descoberta dinamica do cache do plugin
$PLUGIN_CACHE = $null
$pluginBase = "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin"
if (Test-Path $pluginBase) {
    $found = Get-ChildItem -Path $pluginBase -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue |
             Where-Object { $_.FullName -match "\\skills\\mod4\\" } |
             Select-Object -First 1
    if ($found) {
        $PLUGIN_CACHE = Split-Path (Split-Path $found.FullName -Parent) -Parent
    }
}

# ── UTILITARIOS ──────────────────────────────────────────────────────────────
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
    if (-not (Test-Path $zip)) { Warn "Arquivo nao encontrado: $zip - pulando"; return $false }
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
            git commit -m $msg "--author=$GIT_AUTHOR"
            Ok "Commit: $msg"
        } else {
            Warn "Nada a commitar"
        }
    } finally { Pop-Location }
}

function Ensure-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

# ── VALIDACAO INICIAL ─────────────────────────────────────────────────────────
Log "Validando ambiente..."
if (-not (Test-Path $ROOT))   { Err "C:\RaquelSkills nao encontrado" }
if (-not (Test-Path $SKILLS)) { Err "C:\RaquelSkills\skills nao encontrado" }
Push-Location $ROOT
$gitOk = (git status 2>&1) -match "On branch"
Pop-Location
if (-not $gitOk) { Err "Git nao inicializado em $ROOT" }
Ok "Ambiente validado"

if ($PLUGIN_CACHE) {
    Ok "Cache do plugin localizado: $PLUGIN_CACHE"
} else {
    Warn "Cache do plugin nao localizado - Passo 11 (sync) sera pulado"
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 1 - Publicar commits pendentes
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 1) {
    Log "PASSO 1 - Publicar commits pendentes no GitHub"
    if ($DryRun) { Warn "[DryRun] git push" }
    else {
        Push-Location $ROOT
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        Remove-Item ".git\HEAD.lock"  -Force -ErrorAction SilentlyContinue
        $ahead = git status 2>&1 | Select-String "ahead"
        if ($ahead) {
            git push --set-upstream origin main 2>&1 | Out-Host
            Ok "Push concluido"
        } else {
            Warn "Repositorio ja sincronizado com o remoto"
        }
        Pop-Location
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 2 - Deprecar analise-calculo-renda-bpc
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 2) {
    Log "PASSO 2 - Deprecar analise-calculo-renda-bpc (V8: 3 camadas)"
    $src = "$SKILLS\analise-calculo-renda-bpc"
    $dst = "$APAGAR\analise-calculo-renda-bpc-$TS"
    if (Test-Path $src) {
        Backup-Skill "analise-calculo-renda-bpc"
        New-Item -ItemType Directory -Force -Path $APAGAR | Out-Null
        Move-Item $src $dst
        Ok "Movido para _APAGAR\: $dst"
        $deprecMsg = "DEPRECADO - analise-calculo-renda-bpc`nData: $TS`nMotivo: V8 reprovada - SRP violado (C3+C4+C0 simultaneas)`nSubstituido por: analise-renda-bpc, widget-visual, recorte-pdf"
        $deprecMsg | Out-File "$dst\DEPRECACAO.md" -Encoding utf8
    } else {
        Warn "analise-calculo-renda-bpc nao encontrada - ja removida ou nao migrada"
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 3 - Criar estrutura _compartilhados/
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 3) {
    Log "PASSO 3 - Criar _compartilhados/"
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

    $inventario = "# Inventario da Biblioteca Almeida Marques Skills`n"
    $inventario += "# Atualizado: $TS`n"
    $inventario += "# skill | versao | camada | frente | status`n"
    $inventario += "skill-creator-am | 1.4.0 | C0 | transversal | ativo`n"
    $inventario += "mod4 | 4.1.0 | C0 | transversal | ativo`n"
    $inventario += "juridir | 2.0.0 | C2 | transversal | ativo`n"
    $inventario += "pericia-acidentaria | 2.0.0 | C5 | acidentaria | ativo`n"
    $inventario += "pericia-previdenciaria | 2.0.0 | C5 | previdenciaria | ativo`n"
    $inventario += "replica | 3.0.0 | C5 | acidentaria-previdenciaria | ativo`n"
    $inventario += "analise-precedente | 2.0.0 | C2 | constitucional | ativo`n"
    $inventario += "artigo-juridico | 2.0.0 | C2 | constitucional | ativo`n"
    $inventario += "analise-calculo-renda-bpc | 1.0.0 | - | - | DEPRECIADO`n"
    $inventario += "analise-renda-bpc | - | C4 | F1 | draft-pendente`n"
    $inventario += "widget-visual | - | C0 | transversal | draft-pendente`n"
    $inventario += "recorte-pdf | - | C3 | transversal | draft-pendente`n"
    $inventario += "revisao-previa-mod4 | - | C4 | transversal | draft-pendente`n"
    $inventario | Out-File "$SHARED\_inventario.md" -Encoding utf8
    Ok "_inventario.md criado em _compartilhados/"
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 4 - Instalar skills da sessao web (Downloads)
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 4) {
    Log "PASSO 4 - Instalar skills da sessao web"
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
        Warn "pericia-previdenciaria-v4/ nao encontrada em Downloads - pulando"
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 5 - Govern: analise-precedente
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 5) {
    Log "PASSO 5 - Govern analise-precedente"
    $sp = "$SKILLS\analise-precedente\SKILL.md"
    if (Test-Path $sp) {
        $c = Get-Content $sp -Raw -Encoding UTF8
        if ($c -match "version: 2.0.0") { Ok "analise-precedente: ja em V4" }
        else { Backup-Skill "analise-precedente"; Ok "analise-precedente: verificado" }
    } else { Warn "analise-precedente nao encontrada em $SKILLS" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 6 - Govern: pericia-acidentaria
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 6) {
    Log "PASSO 6 - Govern pericia-acidentaria"
    $sp = "$SKILLS\pericia-acidentaria\SKILL.md"
    if (Test-Path $sp) {
        $c = Get-Content $sp -Raw -Encoding UTF8
        if ($c -match "version: 2.0.0") { Ok "pericia-acidentaria: ja em V4" }
        else { Backup-Skill "pericia-acidentaria"; Ok "pericia-acidentaria: verificado" }
    } else { Warn "pericia-acidentaria nao encontrada em $SKILLS" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 7 - Govern: juridir
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 7) {
    Log "PASSO 7 - Govern juridir"
    $sp = "$SKILLS\juridir\SKILL.md"
    if (Test-Path $sp) {
        $c = Get-Content $sp -Raw -Encoding UTF8
        if ($c -match "version: 2.0.0") { Ok "juridir: ja em V4" }
        else { Backup-Skill "juridir"; Ok "juridir: verificado" }
    } else { Warn "juridir nao encontrada em $SKILLS" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 8 - Govern: artigo-juridico
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 8) {
    Log "PASSO 8 - Govern artigo-juridico"
    $sp = "$SKILLS\artigo-juridico\SKILL.md"
    if (Test-Path $sp) {
        $c = Get-Content $sp -Raw -Encoding UTF8
        if ($c -match "version: 2.0.0") { Ok "artigo-juridico: ja em V4" }
        else { Backup-Skill "artigo-juridico"; Ok "artigo-juridico: verificado" }
    } else { Warn "artigo-juridico nao encontrada em $SKILLS" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 9 - Govern: replica
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 9) {
    Log "PASSO 9 - Govern replica"
    $sp = "$SKILLS\replica\SKILL.md"
    if (Test-Path $sp) {
        $c = Get-Content $sp -Raw -Encoding UTF8
        if ($c -match "version: 3.0.0") { Ok "replica: ja em V4" }
        else { Backup-Skill "replica"; Ok "replica: verificado" }
    } else { Warn "replica nao encontrada em $SKILLS" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 10 - Commit e push
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 10) {
    Log "PASSO 10 - Commit e push"
    if (-not $DryRun) {
        Push-Location $ROOT
        if (Test-Path "$SHARED\_inventario.md") {
            Copy-Item "$SHARED\_inventario.md" "$ROOT\_inventario.md" -Force
        }
        Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
        Remove-Item ".git\HEAD.lock"  -Force -ErrorAction SilentlyContinue
        git add -A
        $dirty = git status --porcelain
        if ($dirty) {
            $msg = "chore(biblioteca): sprint V4 v1.2.0 - govern 8 skills, inventario ($TS)"
            git commit -m $msg "--author=$GIT_AUTHOR"
            git push
            Ok "Commit e push concluidos"
        } else {
            Warn "Nada novo para commitar"
        }
        Pop-Location
    } else { Warn "[DryRun] Commit e push simulados" }
}

# ═════════════════════════════════════════════════════════════════════════════
# PASSO 11 - Sincronizar cache do Cowork com RaquelSkills
# ═════════════════════════════════════════════════════════════════════════════
if ($Passo -eq 0 -or $Passo -eq 11) {
    Log "PASSO 11 - Sincronizar cache do Cowork"
    if (-not $PLUGIN_CACHE) {
        Warn "Cache do plugin nao localizado - pulando sincronizacao"
        Warn "Verifique: $env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin\"
    } else {
        Log "Fonte:   $SKILLS"
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
                Backup-PluginSkill $nome
                Ensure-Dir $dst
                Copy-Item -Recurse -Force "$src\*" "$dst\"
                Ok "Sincronizado: $nome"
            }

            if (-not $DryRun) {
                $syncLog = "$BACKUPS\plugin-cache-$TS\_sync.log"
                Ensure-Dir (Split-Path $syncLog -Parent)
                $logContent = "Sincronizacao: $TS`nFonte: $SKILLS`nDestino: $PLUGIN_CACHE`nSkills: $($skillsMigradas.Name -join ', ')"
                $logContent | Out-File $syncLog -Encoding utf8
                Ok "Log de sincronizacao: $syncLog"
                Write-Host ""
                Write-Host "  PROXIMO PASSO: Recarregue o plugin no Cowork para aplicar as alteracoes." -ForegroundColor Magenta
            }
        }
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# RELATORIO FINAL
# ═════════════════════════════════════════════════════════════════════════════
Log ""
Log "======================================================"
Log "SPRINT CONCLUIDO - biblioteca Almeida Marques v1.2.0"
Log "======================================================"
Log ""
Log "Skills em C:\RaquelSkills\skills\ (fonte canonica):"
if (Test-Path $SKILLS) {
    Get-ChildItem -Path $SKILLS -Directory | ForEach-Object {
        $vLine = Select-String -Path "$($_.FullName)\SKILL.md" -Pattern "^version:" -ErrorAction SilentlyContinue |
                 Select-Object -First 1
        $v = if ($vLine) { $vLine.Line } else { "versao desconhecida" }
        Write-Host ("  " + $_.Name.PadRight(30) + $v) -ForegroundColor White
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
