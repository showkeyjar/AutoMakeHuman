param(
    [string]$Target = $env:MAKEHUMAN_PLUGIN_DIR
)

if (-not $Target) {
    Write-Error "Provide -Target or set MAKEHUMAN_PLUGIN_DIR."
    exit 1
}

python "$PSScriptRoot/install.py" --target $Target
