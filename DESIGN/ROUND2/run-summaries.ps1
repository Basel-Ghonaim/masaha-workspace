# Waits for all 40 review reports, then runs the six part summaries at once, waits for them, then the
# summary across all. Run it in its own PowerShell window and leave it open.
# Usage:  & "D:\masahaWorkspace\DESIGN\ROUND2\run-summaries.ps1"
# Each wait gives up after -MaxMinutes (default 360 for the reviews, then 90 per summary step).
param([int]$MaxMinutes = 360)

$root  = 'D:\masahaWorkspace\DESIGN\ROUND2'
$repo  = 'C:\Users\basel\masaha-design'
$logs  = Join-Path $root 'LOGS'
$parts = 'AU', 'PU', 'AD', 'OW', 'DK', 'SH'
New-Item -ItemType Directory -Force $logs | Out-Null

function Wait-Files([string[]]$paths, [int]$minutes, [string]$what) {
  $deadline = (Get-Date).AddMinutes($minutes)
  while ($true) {
    $missing = @($paths | Where-Object { -not (Test-Path $_) })
    if ($missing.Count -eq 0) { return }
    if ((Get-Date) -gt $deadline) {
      Write-Warning "$what not finished after $minutes minutes; missing: $($missing | ForEach-Object { Split-Path $_ -Leaf })"
      exit 1
    }
    Write-Host ("{0:HH:mm}  {1}: {2} file(s) missing - next check in 1 minute" -f (Get-Date), $what, $missing.Count)
    Start-Sleep -Seconds 60
  }
}

function Start-Prompt([string]$id) {
  $prompt = Join-Path $root "PROMPT\$id.md"
  $log    = Join-Path $logs "$id.log"
  $msg    = "Read $prompt whole and follow it."
  $cmd    = "`$host.UI.RawUI.WindowTitle = '$id'; [Console]::OutputEncoding = [Text.Encoding]::UTF8; opencode run --dir '$repo' --auto --title '$id' '$msg' 2>&1 | Tee-Object -FilePath '$log'"
  Start-Process powershell -ArgumentList '-NoExit', '-Command', $cmd
  Write-Host "start $id  (log: $log)"
  Start-Sleep -Seconds 3
}

# 1. The 40 reviews: every review prompt's report.
$reviews = Get-ChildItem (Join-Path $root 'PROMPT') -Filter 'R2-*-*.md' |
  Where-Object { $_.BaseName -notmatch 'SUMMARY' } |
  ForEach-Object { Join-Path $root "REPORT\$($_.BaseName)_REPORT.md" }
Write-Host "Waiting for $($reviews.Count) review reports."
Wait-Files $reviews $MaxMinutes 'reviews'

# 2. The six part summaries, together (no browser, no server).
$partOut = $parts | ForEach-Object { Join-Path $root "SUMMARY\R2-$($_)_SUMMARY.md" }
foreach ($p in $parts) {
  if (Test-Path (Join-Path $root "SUMMARY\R2-$($p)_SUMMARY.md")) { Write-Host "skip  R2-$p-SUMMARY (exists)"; continue }
  Start-Prompt "R2-$p-SUMMARY"
}
Wait-Files $partOut 90 'part summaries'

# 3. The summary across all.
$allOut = Join-Path $root 'SUMMARY\R2-ALL_SUMMARY.md'
if (-not (Test-Path $allOut)) { Start-Prompt 'R2-ALL-SUMMARY' }
Wait-Files @($allOut) 90 'the summary across all'
Write-Host ("{0:HH:mm}  done: {1}" -f (Get-Date), $allOut)
