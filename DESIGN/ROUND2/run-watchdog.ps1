# A plain watchdog (no AI): runs run-queue.ps1, and keeps it going until every report and summary
# exists. If the queue stops with outputs missing (every model at its limit, a crash), it waits
# -PauseMinutes and starts it again (the queue resumes: it runs only what is missing). If nothing new
# appears for -StallMinutes while the queue runs, it stops the queue and its OpenCode runs, and starts
# again. It gives up after -MaxHours.
# Usage:  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-watchdog.ps1"
param(
  [int]$PauseMinutes = 30,
  [int]$StallMinutes = 90,
  [int]$MaxHours = 12
)

$root  = 'C:\dev\masaha\workspace\DESIGN\ROUND2'
$queue = Join-Path $root 'run-queue.ps1'
$end   = (Get-Date).AddHours($MaxHours)

function Count-Outputs { (Get-ChildItem (Join-Path $root 'REPORT') -File -EA SilentlyContinue).Count + (Get-ChildItem (Join-Path $root 'SUMMARY') -File -EA SilentlyContinue).Count }
function All-Done { Test-Path (Join-Path $root 'SUMMARY\R2-ALL_SUMMARY.md') }
function Stop-Runs { Get-Process opencode -EA SilentlyContinue | Stop-Process -Force -EA SilentlyContinue }

$round = 0
while (-not (All-Done) -and (Get-Date) -lt $end) {
  $round++
  Write-Host ("{0:HH:mm}  watchdog: starting the queue (round {1}), {2} outputs so far" -f (Get-Date), $round, (Count-Outputs))
  $p = Start-Process powershell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$queue`"") -PassThru
  $last = Count-Outputs; $lastChange = Get-Date
  while (-not $p.HasExited) {
    Start-Sleep -Seconds 60
    $now = Count-Outputs
    if ($now -ne $last) { $last = $now; $lastChange = Get-Date; Write-Host ("{0:HH:mm}  watchdog: {1} outputs" -f (Get-Date), $now) }
    elseif (((Get-Date) - $lastChange).TotalMinutes -gt $StallMinutes) {
      Write-Warning ("{0:HH:mm}  watchdog: nothing new for {1} minutes; restarting the queue" -f (Get-Date), $StallMinutes)
      Stop-Process -Id $p.Id -Force -EA SilentlyContinue; Stop-Runs; break
    }
    if ((Get-Date) -gt $end) { break }
  }
  if (All-Done) { break }
  Write-Host ("{0:HH:mm}  watchdog: the queue stopped with outputs missing; pausing {1} minutes (model limits reset)" -f (Get-Date), $PauseMinutes)
  Start-Sleep -Seconds ($PauseMinutes * 60)
}
if (All-Done) { Write-Host ("{0:HH:mm}  watchdog: all done." -f (Get-Date)) }
else { Write-Warning ("{0:HH:mm}  watchdog: gave up after {1} hours; {2} outputs. Run it again to resume." -f (Get-Date), $MaxHours, (Count-Outputs)) }
