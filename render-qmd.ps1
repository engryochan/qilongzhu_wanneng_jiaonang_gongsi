param()
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $files = @(Get-ChildItem -LiteralPath $PSScriptRoot -Recurse -File -Filter '*.qmd' |
        Where-Object { $_.FullName -notmatch '[\\/](\.git|\.quarto|node_modules)[\\/]' })
    foreach ($file in $files) {
        Write-Host "Rendering $($file.FullName)"
        & quarto render $file.FullName --to html
        if ($LASTEXITCODE -ne 0) { throw "Render failed: $($file.FullName)" }
    }
    Write-Host "Rendered $($files.Count) QMD files successfully."
} finally {
    Pop-Location
}
