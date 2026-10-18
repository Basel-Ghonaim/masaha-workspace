# Waits for a wave's reports, then starts the next wave, and so on.
# Usage (PowerShell):  & "D:\masahaWorkspace\DESIGN\ROUND2\run-chain.ps1" -After 2 -Until 4
# = wait until wave 2's ten reports exist, start wave 3; wait for wave 3's, start wave 4. Then stop.
# Each wait gives up after -MaxMinutes (default 120) and stops the chain, saying which reports are missing.
param(
  [Parameter(Mandatory = $true)][ValidateRange(1, 3)][int]$After,
  [ValidateRange(2, 4)][int]$Until = 4,
  [int]$MaxMinutes = 120
)

$root  = 'D:\masahaWorkspace\DESIGN\ROUND2'
$sheet = Get-Content (Join-Path $root 'RUN_SHEET.md') -Encoding UTF8

function Get-WaveIds([int]$wave) {
  $in = $false; $ids = @()
  foreach ($line in $sheet) {
    if ($line -match '^## Wave (\d+)') { $in = ([int]$Matches[1] -eq $wave); continue }
    if ($in -and $line -match '^## ') { break }
    if ($in -and $line -match '^\|\s*(R2-[A-Z]{2}-[A-Z]{2})\s*\|') { $ids += $Matches[1] }
  }
  return $ids
}

function Get-Missing([int]$wave) {
  return @(Get-WaveIds $wave | Where-Object { -not (Test-Path (Join-Path $root "REPORT\$($_)_REPORT.md")) })
}

for ($wave = $After; $wave -lt $Until; $wave++) {
  $deadline = (Get-Date).AddMinutes($MaxMinutes)
  while ($true) {
    $missing = Get-Missing $wave
    if ($missing.Count -eq 0) { break }
    if ((Get-Date) -gt $deadline) {
      Write-Warning "Wave $wave not finished after $MaxMinutes minutes; still missing: $($missing -join ', '). Chain stopped."
      exit 1
    }
    Write-Host ("{0:HH:mm}  wave {1}: {2} report(s) missing - next check in 1 minute" -f (Get-Date), $wave, $missing.Count)
    Start-Sleep -Seconds 60
  }
  Write-Host ("{0:HH:mm}  wave {1} complete. Starting wave {2}." -f (Get-Date), $wave, ($wave + 1))
  Start-Sleep -Seconds 30   # let the finished windows release their browsers and ports
  & (Join-Path $root 'run-wave.ps1') -Wave ($wave + 1)
}
Write-Host ("{0:HH:mm}  chain done: wave {1} started." -f (Get-Date), $Until)
