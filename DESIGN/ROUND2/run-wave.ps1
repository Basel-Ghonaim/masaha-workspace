# Starts one wave of round-2 reviews: one OpenCode window per review, each running its prompt alone.
# Usage (PowerShell):  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-wave.ps1" -Wave 2
# Add -DryRun to see what would start, without starting anything.
param(
  [Parameter(Mandatory = $true)][ValidateRange(1, 4)][int]$Wave,
  [switch]$DryRun
)

$root    = 'C:\dev\masaha\workspace\DESIGN\ROUND2'
$repo    = 'C:\dev\masaha\design'
$logs    = Join-Path $root 'LOGS'
$sheet   = Get-Content (Join-Path $root 'RUN_SHEET.md') -Encoding UTF8
New-Item -ItemType Directory -Force $logs | Out-Null

# Read the wave's table from the run sheet: the IDs under "## Wave N", up to the next heading.
$inWave = $false; $ids = @()
foreach ($line in $sheet) {
  if ($line -match '^## Wave (\d+)') { $inWave = ([int]$Matches[1] -eq $Wave); continue }
  if ($inWave -and $line -match '^## ') { break }
  if ($inWave -and $line -match '^\|\s*(R2-[A-Z]{2}-[A-Z]{2})\s*\|') { $ids += $Matches[1] }
}
if ($ids.Count -eq 0) { Write-Error "No reviews found for wave $Wave in RUN_SHEET.md"; exit 1 }

# Skip any review whose report already exists (a rerun starts only what is missing).
foreach ($id in $ids) {
  $report = Join-Path $root "REPORT\$($id)_REPORT.md"
  if (Test-Path $report) { Write-Host "skip  $id (report exists)"; continue }
  $prompt = Join-Path $root "PROMPT\$id.md"
  $log    = Join-Path $logs "$id.log"
  $msg    = "Read $prompt whole and follow it."
  # OpenCode writes its progress to stderr, which PowerShell 5.1 paints red: harmless.
  $cmd    = "`$host.UI.RawUI.WindowTitle = '$id'; [Console]::OutputEncoding = [Text.Encoding]::UTF8; opencode run --dir '$repo' --auto --title '$id' '$msg' 2>&1 | Tee-Object -FilePath '$log'"
  if ($DryRun) { Write-Host "would start  $id"; continue }
  Start-Process powershell -ArgumentList '-NoExit', '-Command', $cmd
  Write-Host "start $id  (log: $log)"
  Start-Sleep -Seconds 3   # stagger the starts so ten servers and browsers do not spin up at once
}
