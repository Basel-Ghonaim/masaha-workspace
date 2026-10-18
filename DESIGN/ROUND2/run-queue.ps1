# Runs every review whose report is missing, at most -Parallel at a time, then the six part summaries
# and the summary across all. When a model answers "Rate limit exceeded", the queue moves to the next
# model in -Models and starts that run again (a rate limit is not counted as a try).
# A run that ends or passes -RunMinutes without its report is retried, up to -MaxTries.
# Usage:  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-queue.ps1" -Models opencode/big-pickle,opencode/step-5-preview-free
#         (list the models with: opencode models)
param(
  [string[]]$Models = @('opencode/step-5-preview-free', 'opencode/nemotron-3-ultra-free', 'opencode/longcat-2.5-preview-free', 'opencode/big-pickle'),
  [int]$Parallel = 3,
  [int]$RunMinutes = 45,
  [int]$MaxTries = 3
)

$root = 'C:\dev\masaha\workspace\DESIGN\ROUND2'
$repo = 'C:\dev\masaha\design'
$logs = Join-Path $root 'LOGS'
$exe  = Join-Path $env:APPDATA 'npm\node_modules\opencode-ai\bin\opencode.exe'
New-Item -ItemType Directory -Force $logs | Out-Null
$script:modelIndex = 0

function Out-Of([string]$id) {
  if ($id -match '^R2-(ALL|[A-Z]{2})-SUMMARY$') { return Join-Path $root "SUMMARY\R2-$($Matches[1])_SUMMARY.md" }
  return Join-Path $root "REPORT\$($id)_REPORT.md"
}

# OpenCode writes a refused call to its own log, not to the run's output: look there for this model's
# "Rate limit" since the run started (the log's times are UTC).
$ocLog = Join-Path $env:USERPROFILE '.local\share\opencode\log\opencode.log'
function Hit-Limit($run) {
  if (-not (Test-Path $ocLog)) { return $false }
  $short = $run.Model.Split('/')[-1]
  $since = $run.Start.ToUniversalTime()
  foreach ($m in (Select-String -Path $ocLog -Pattern 'Rate limit|rate_limit|Too Many Requests' | Select-Object -Last 50)) {
    $line = $m.Line
    if ($line -notmatch "modelID=$([regex]::Escape($short))(\s|$)") { continue }
    if ($line -match 'timestamp=(\S+)' -and ([datetime]::Parse($Matches[1]).ToUniversalTime() -gt $since)) { return $true }
  }
  return $false
}

function Next-Model([string]$exhausted) {
  # Move on only if the exhausted model is still the current one (several runs may report it).
  if ($Models[$script:modelIndex] -ne $exhausted) { return }
  if ($script:modelIndex + 1 -ge $Models.Count) {
    Write-Warning "Every model in -Models hit its limit. Stopping; run the script again later (it resumes)."
    exit 2
  }
  $script:modelIndex++
  Write-Host ("{0:HH:mm}  model {1} hit its limit -> switching to {2}" -f (Get-Date), $exhausted, $Models[$script:modelIndex])
}

function Run-Batch([string[]]$ids, [string]$label) {
  $queue = New-Object System.Collections.Queue
  $ids | Where-Object { -not (Test-Path (Out-Of $_)) } | ForEach-Object { $queue.Enqueue($_) }
  $tries = @{}; $running = @{}; $n = 0
  Write-Host ("{0:HH:mm}  {1}: {2} to run, {3} at a time, model {4}" -f (Get-Date), $label, $queue.Count, $Parallel, $Models[$script:modelIndex])
  while ($queue.Count -gt 0 -or $running.Count -gt 0) {
    foreach ($id in @($running.Keys)) {
      $r = $running[$id]
      if (Test-Path (Out-Of $id)) {
        if (-not $r.Proc.HasExited) { $r.Proc.WaitForExit(120000) | Out-Null }
        $running.Remove($id); Write-Host ("{0:HH:mm}  done  {1}" -f (Get-Date), $id); continue
      }
      if (Hit-Limit $r) {
        Stop-Process -Id $r.Proc.Id -Force -ErrorAction SilentlyContinue
        $running.Remove($id); $tries[$id]--          # a rate limit is not the run's fault
        Next-Model $r.Model
        $queue.Enqueue($id); continue
      }
      $done = $r.Proc.HasExited
      $late = ((Get-Date) - $r.Start).TotalMinutes -gt $RunMinutes
      if (-not ($done -or $late)) { continue }
      if (-not $done) { Stop-Process -Id $r.Proc.Id -Force -ErrorAction SilentlyContinue }
      $running.Remove($id)
      if ($tries[$id] -lt $MaxTries) {
        Write-Host ("{0:HH:mm}  retry {1} (no output after try {2})" -f (Get-Date), $id, $tries[$id])
        $queue.Enqueue($id)
      } else { Write-Warning "$id gave no output after $MaxTries tries; skipped" }
    }
    while ($running.Count -lt $Parallel -and $queue.Count -gt 0) {
      $id = $queue.Dequeue()
      $tries[$id] = 1 + [int]$tries[$id]; $n++
      $model = $Models[$script:modelIndex]
      $msg = "Read $(Join-Path $root "PROMPT\$id.md") whole and follow it."
      $log = Join-Path $logs ("{0}.{1:HHmmss}.log" -f $id, (Get-Date))
      $argv = @('run', '--dir', $repo, '--auto', '--title', $id, '-m', $model, "`"$msg`"")
      $p = Start-Process $exe -ArgumentList $argv -RedirectStandardOutput $log -RedirectStandardError "$log.err" `
             -WindowStyle Minimized -PassThru
      $running[$id] = @{ Proc = $p; Start = Get-Date; Log = $log; Model = $model }
      Write-Host ("{0:HH:mm}  start {1} (try {2}, {3})" -f (Get-Date), $id, $tries[$id], $model)
      Start-Sleep -Seconds 20
    }
    Start-Sleep -Seconds 30
  }
}

$reviews = Get-ChildItem (Join-Path $root 'PROMPT') -Filter 'R2-*-*.md' |
  Where-Object { $_.BaseName -notmatch 'SUMMARY' } | ForEach-Object { $_.BaseName } | Sort-Object
Run-Batch $reviews 'reviews'
Run-Batch @('R2-AU-SUMMARY', 'R2-PU-SUMMARY', 'R2-AD-SUMMARY', 'R2-OW-SUMMARY', 'R2-DK-SUMMARY', 'R2-SH-SUMMARY') 'part summaries'
Run-Batch @('R2-ALL-SUMMARY') 'summary across all'

$missing = @($reviews + 'R2-ALL-SUMMARY' | Where-Object { -not (Test-Path (Out-Of $_)) })
if ($missing.Count) { Write-Warning "Finished with outputs missing: $($missing -join ', ')" }
else { Write-Host ("{0:HH:mm}  all done: {1}" -f (Get-Date), (Out-Of 'R2-ALL-SUMMARY')) }
