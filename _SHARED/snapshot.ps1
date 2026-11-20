# Commits and pushes the changes of C:\dev\masaha\workspace to its private GitHub repository.
# Run by the Windows task "masaha-workspace-snapshot" at 08:00 and 17:30, or at the first chance after
# either when the machine was off; safe to run by hand at any time.
# Commits nothing when nothing changed, and pushes any commit an earlier run could not push.
# A failed commit or push is logged as FAILED and exits 1, so the task retries it.
$ErrorActionPreference = 'Stop'
Set-Location 'C:\dev\masaha\workspace'
$log = Join-Path $PSScriptRoot 'snapshot.log'
function Write-SnapshotLog([string]$text) {
  Add-Content -Path $log -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm') $text" -Encoding utf8
}

git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  git commit -q -m "snapshot $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
  if ($LASTEXITCODE -ne 0) { Write-SnapshotLog 'commit FAILED'; exit 1 }
}

$ahead = [int](git rev-list --count origin/main..HEAD)
if ($ahead -eq 0) { Write-SnapshotLog 'nothing to commit or push'; exit 0 }

git push -q origin main
if ($LASTEXITCODE -ne 0) {
  Write-SnapshotLog "push FAILED ($ahead commit(s) waiting; the next run retries)"
  exit 1
}
Write-SnapshotLog "committed and pushed $(git rev-parse --short HEAD) ($ahead commit(s))"
