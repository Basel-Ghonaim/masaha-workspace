# Commits and pushes the day's changes of C:\dev\masaha\workspace to its private GitHub repository.
# Run nightly by the Windows task "masaha-workspace-snapshot"; safe to run by hand at any time.
# Writes nothing when nothing changed.
$ErrorActionPreference = 'Stop'
Set-Location 'C:\dev\masaha\workspace'
$log = Join-Path $PSScriptRoot 'snapshot.log'
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'

git add -A
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
  Add-Content -Path $log -Value "$stamp nothing to commit" -Encoding utf8
  exit 0
}
git commit -q -m "snapshot $(Get-Date -Format 'yyyy-MM-dd')"
git push -q origin main
Add-Content -Path $log -Value "$stamp committed and pushed $(git rev-parse --short HEAD)" -Encoding utf8
