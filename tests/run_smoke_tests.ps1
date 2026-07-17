$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$fixture = Join-Path $PSScriptRoot 'fixtures'
$out = Join-Path $env:TEMP 'paper-helper-smoke'
New-Item -ItemType Directory -Force -Path $out | Out-Null
python (Join-Path $root 'scripts\reference_ledger.py') (Join-Path $fixture 'references.valid.json') --report (Join-Path $out 'ledger.md')
python (Join-Path $root 'scripts\check_citations.py') (Join-Path $fixture 'manuscript.md') (Join-Path $fixture 'references.valid.json') --report (Join-Path $out 'citations.md')
$oldPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
python (Join-Path $root 'scripts\reference_ledger.py') (Join-Path $fixture 'references.invalid.json') --report (Join-Path $out 'invalid-ledger.md')
$invalidExitCode = $LASTEXITCODE
$ErrorActionPreference = $oldPreference
if ($invalidExitCode -ne 1) { throw "invalid ledger should return 1, got $invalidExitCode" }
if (-not (Test-Path (Join-Path $out 'ledger.md'))) { throw 'ledger report was not created' }
if (-not (Test-Path (Join-Path $out 'citations.md'))) { throw 'citation report was not created' }
if (-not (Test-Path (Join-Path $out 'invalid-ledger.md'))) { throw 'invalid ledger report was not created' }
Write-Host "Smoke tests passed: $out"
