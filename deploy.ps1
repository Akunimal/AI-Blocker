$ErrorActionPreference = "Stop"

.\.venv\Scripts\python.exe -m PyInstaller `
    --onefile `
    --windowed `
    --uac-admin `
    --add-data "translations.json;." `
    --add-data "icon.ico;." `
    --add-data "icon_green.ico;." `
    --add-data "icon_red.ico;." `
    --name "AI-Router-Blocker-AiO" `
    --clean `
    ai_blocker.py

Copy-Item "dist\AI-Router-Blocker-AiO.exe" "AI-Router-Blocker-AiO.exe" -Force

Write-Host "Windows build complete: AI-Router-Blocker-AiO.exe"
Write-Host "Publish cross-platform releases from GitHub by creating a versioned release tag, for example v1.2.1."
